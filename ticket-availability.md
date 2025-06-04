# Ticketing Site Database Availability Logic

## Overview

This document explains how the QRTick availability system works at the database level for implementation in the customer-facing ticketing site. The ticketing site should query Supabase directly to determine ticket availability using the logic outlined below.

## Database Schema

### Primary Table: `ticket_types`

The availability rules are stored in the `ticket_types` table with these key fields:

```sql
CREATE TABLE ticket_types (
    id UUID PRIMARY KEY,
    event_id UUID REFERENCES events(id),
    name VARCHAR NOT NULL,
    price DECIMAL(10,2),
    max_quantity INTEGER,

    -- Availability Rule Fields
    sales_start_date TIMESTAMPTZ,           -- Absolute start date/time
    sales_end_date TIMESTAMPTZ,             -- Absolute end date/time
    sales_start_offset_days INTEGER,        -- Days before event to start sales
    sales_end_offset_days INTEGER,          -- Days before event to end sales
    is_available_override BOOLEAN,          -- Manual override (null = follow rules)

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Related Table: `events`

```sql
CREATE TABLE events (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    start_date TIMESTAMPTZ,                 -- Event start date/time
    organization_id UUID,
    is_published BOOLEAN DEFAULT false,
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Availability Logic Implementation

### Core SQL Function

```sql
CREATE OR REPLACE FUNCTION check_ticket_availability(
    p_ticket_type_id UUID,
    p_check_time TIMESTAMPTZ DEFAULT NOW()
)
RETURNS TABLE (
    is_available BOOLEAN,
    reason TEXT,
    starts_at TIMESTAMPTZ,
    ends_at TIMESTAMPTZ
) AS $$
DECLARE
    ticket_record RECORD;
    event_start TIMESTAMPTZ;
    calculated_start TIMESTAMPTZ;
    calculated_end TIMESTAMPTZ;
BEGIN
    -- Get ticket type and event data
    SELECT tt.*, e.start_date as event_start_date
    INTO ticket_record
    FROM ticket_types tt
    JOIN events e ON tt.event_id = e.id
    WHERE tt.id = p_ticket_type_id;

    IF NOT FOUND THEN
        RETURN QUERY SELECT false, 'Ticket type not found'::TEXT, NULL::TIMESTAMPTZ, NULL::TIMESTAMPTZ;
        RETURN;
    END IF;

    event_start := ticket_record.event_start_date;

    -- Priority 1: Manual Override
    IF ticket_record.is_available_override IS NOT NULL THEN
        IF ticket_record.is_available_override THEN
            RETURN QUERY SELECT true, 'Manual override: Available'::TEXT, NULL::TIMESTAMPTZ, NULL::TIMESTAMPTZ;
        ELSE
            RETURN QUERY SELECT false, 'Manual override: Disabled'::TEXT, NULL::TIMESTAMPTZ, NULL::TIMESTAMPTZ;
        END IF;
        RETURN;
    END IF;

    -- Calculate effective start and end times
    calculated_start := COALESCE(
        ticket_record.sales_start_date,
        CASE
            WHEN ticket_record.sales_start_offset_days IS NOT NULL
            THEN event_start - (ticket_record.sales_start_offset_days || ' days')::INTERVAL
            ELSE NULL
        END
    );

    calculated_end := COALESCE(
        ticket_record.sales_end_date,
        CASE
            WHEN ticket_record.sales_end_offset_days IS NOT NULL
            THEN event_start - (ticket_record.sales_end_offset_days || ' days')::INTERVAL
            ELSE event_start
        END,
        event_start
    );

    -- Priority 2: Check if before start time
    IF calculated_start IS NOT NULL AND p_check_time < calculated_start THEN
        RETURN QUERY SELECT
            false,
            'Sales start on ' || TO_CHAR(calculated_start AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI:SS UTC'),
            calculated_start,
            calculated_end;
        RETURN;
    END IF;

    -- Priority 3: Check if after end time
    IF p_check_time > calculated_end THEN
        RETURN QUERY SELECT
            false,
            'Sales ended on ' || TO_CHAR(calculated_end AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI:SS UTC'),
            calculated_start,
            calculated_end;
        RETURN;
    END IF;

    -- Available
    RETURN QUERY SELECT
        true,
        'Currently available for purchase'::TEXT,
        calculated_start,
        calculated_end;
END;
$$ LANGUAGE plpgsql;
```

### Simple SQL Query for Direct Implementation

If you prefer not to use a stored function, here's the equivalent SQL query:

```sql
WITH availability_check AS (
    SELECT
        tt.id,
        tt.name,
        tt.price,
        e.start_date as event_start,
        tt.is_available_override,

        -- Calculate effective start time
        COALESCE(
            tt.sales_start_date,
            CASE
                WHEN tt.sales_start_offset_days IS NOT NULL
                THEN e.start_date - (tt.sales_start_offset_days || ' days')::INTERVAL
                ELSE NULL
            END
        ) as effective_start,

        -- Calculate effective end time
        COALESCE(
            tt.sales_end_date,
            CASE
                WHEN tt.sales_end_offset_days IS NOT NULL
                THEN e.start_date - (tt.sales_end_offset_days || ' days')::INTERVAL
                ELSE e.start_date
            END,
            e.start_date
        ) as effective_end

    FROM ticket_types tt
    JOIN events e ON tt.event_id = e.id
    WHERE tt.id = $1  -- ticket_type_id parameter
)
SELECT
    *,
    CASE
        -- Manual override takes precedence
        WHEN is_available_override = true THEN true
        WHEN is_available_override = false THEN false

        -- Check time boundaries
        WHEN NOW() < effective_start THEN false
        WHEN NOW() > effective_end THEN false

        -- Available
        ELSE true
    END as is_available,

    CASE
        WHEN is_available_override = true THEN 'Manual override: Available'
        WHEN is_available_override = false THEN 'Manual override: Disabled'
        WHEN NOW() < effective_start THEN 'Sales start on ' || TO_CHAR(effective_start, 'YYYY-MM-DD HH24:MI:SS UTC')
        WHEN NOW() > effective_end THEN 'Sales ended on ' || TO_CHAR(effective_end, 'YYYY-MM-DD HH24:MI:SS UTC')
        ELSE 'Currently available for purchase'
    END as reason

FROM availability_check;
```

## Implementation Examples

### 1. Check Single Ticket Type Availability

```sql
-- Using the function
SELECT * FROM check_ticket_availability('ticket-type-uuid-here');

-- Using direct query
SELECT
    tt.id,
    tt.name,
    CASE
        WHEN tt.is_available_override = true THEN true
        WHEN tt.is_available_override = false THEN false
        WHEN NOW() < COALESCE(tt.sales_start_date, e.start_date - (tt.sales_start_offset_days || ' days')::INTERVAL) THEN false
        WHEN NOW() > COALESCE(tt.sales_end_date, e.start_date - (tt.sales_end_offset_days || ' days')::INTERVAL, e.start_date) THEN false
        ELSE true
    END as is_available
FROM ticket_types tt
JOIN events e ON tt.event_id = e.id
WHERE tt.id = 'ticket-type-uuid-here';
```

### 2. Get All Available Ticket Types for an Event

```sql
SELECT
    tt.id,
    tt.name,
    tt.price,
    tt.max_quantity,
    CASE
        WHEN tt.is_available_override = true THEN true
        WHEN tt.is_available_override = false THEN false
        WHEN NOW() < COALESCE(
            tt.sales_start_date,
            e.start_date - (tt.sales_start_offset_days || ' days')::INTERVAL
        ) THEN false
        WHEN NOW() > COALESCE(
            tt.sales_end_date,
            e.start_date - (tt.sales_end_offset_days || ' days')::INTERVAL,
            e.start_date
        ) THEN false
        ELSE true
    END as is_available
FROM ticket_types tt
JOIN events e ON tt.event_id = e.id
WHERE e.id = 'event-uuid-here'
  AND e.is_published = true
  AND e.is_public = true
  AND CASE
        WHEN tt.is_available_override = true THEN true
        WHEN tt.is_available_override = false THEN false
        WHEN NOW() < COALESCE(
            tt.sales_start_date,
            e.start_date - (tt.sales_start_offset_days || ' days')::INTERVAL
        ) THEN false
        WHEN NOW() > COALESCE(
            tt.sales_end_date,
            e.start_date - (tt.sales_end_offset_days || ' days')::INTERVAL,
            e.start_date
        ) THEN false
        ELSE true
      END = true;
```

### 3. Batch Availability Check for Cart Validation

```sql
SELECT
    tt.id,
    CASE
        WHEN tt.is_available_override = true THEN true
        WHEN tt.is_available_override = false THEN false
        WHEN NOW() < COALESCE(
            tt.sales_start_date,
            e.start_date - (tt.sales_start_offset_days || ' days')::INTERVAL
        ) THEN false
        WHEN NOW() > COALESCE(
            tt.sales_end_date,
            e.start_date - (tt.sales_end_offset_days || ' days')::INTERVAL,
            e.start_date
        ) THEN false
        ELSE true
    END as is_available,
    CASE
        WHEN tt.is_available_override = true THEN 'Available'
        WHEN tt.is_available_override = false THEN 'Disabled by organizer'
        WHEN NOW() < COALESCE(
            tt.sales_start_date,
            e.start_date - (tt.sales_start_offset_days || ' days')::INTERVAL
        ) THEN 'Sales not yet started'
        WHEN NOW() > COALESCE(
            tt.sales_end_date,
            e.start_date - (tt.sales_end_offset_days || ' days')::INTERVAL,
            e.start_date
        ) THEN 'Sales have ended'
        ELSE 'Available'
    END as status_message
FROM ticket_types tt
JOIN events e ON tt.event_id = e.id
WHERE tt.id = ANY($1);  -- Array of ticket type IDs
```

## Key Database Considerations

### 1. Timezone Handling
- All timestamps are stored in UTC (`TIMESTAMPTZ`)
- Convert to user's local timezone for display only
- Always perform availability calculations in UTC

### 2. Null Value Handling
- `sales_start_date = NULL`: No absolute start constraint
- `sales_end_date = NULL`: Sales end at event start time
- `sales_start_offset_days = NULL`: No offset-based start
- `sales_end_offset_days = NULL`: No offset-based end
- `is_available_override = NULL`: Follow automatic rules

### 3. Performance Optimization
- Index on `ticket_types.event_id`
- Index on `events.is_published, events.is_public`
- Consider materialized view for complex availability queries

### 4. Validation Rules (Enforced in Admin, Check in Ticketing Site)
- `sales_start_date < sales_end_date` (if both set)
- `sales_end_date <= event.start_date` (if set)
- `sales_start_offset_days > sales_end_offset_days` (if both set)
- Offset days must be non-negative

## Common Queries for Ticketing Site

### Event List with Availability Status
```sql
SELECT
    e.id,
    e.name,
    e.start_date,
    e.location,
    COUNT(tt.id) as total_ticket_types,
    COUNT(CASE WHEN [availability_logic] THEN 1 END) as available_ticket_types
FROM events e
LEFT JOIN ticket_types tt ON e.id = tt.event_id
WHERE e.is_published = true AND e.is_public = true
GROUP BY e.id, e.name, e.start_date, e.location
HAVING COUNT(CASE WHEN [availability_logic] THEN 1 END) > 0;
```

### Upcoming Sales Start Times
```sql
SELECT
    tt.id,
    tt.name,
    e.name as event_name,
    COALESCE(
        tt.sales_start_date,
        e.start_date - (tt.sales_start_offset_days || ' days')::INTERVAL
    ) as sales_start_time
FROM ticket_types tt
JOIN events e ON tt.event_id = e.id
WHERE COALESCE(
    tt.sales_start_date,
    e.start_date - (tt.sales_start_offset_days || ' days')::INTERVAL
) > NOW()
ORDER BY sales_start_time ASC;
```

## Error Handling

When availability checks fail, return structured data:

```json
{
  "available": false,
  "reason": "sales_not_started",
  "message": "Sales start on 2024-06-01 at 10:00 AM UTC",
  "starts_at": "2024-06-01T10:00:00Z",
  "ends_at": "2024-06-15T17:00:00Z"
}
```

## Integration Notes

1. **Real-time Updates**: Query availability on every page load and before purchase
2. **Caching**: Cache for maximum 30-60 seconds due to time-sensitive nature
3. **Cart Validation**: Re-validate all items before payment processing
4. **Status Display**: Show countdown timers for upcoming sales start/end times
