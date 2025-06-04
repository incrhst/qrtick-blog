#!/usr/bin/env python3
"""
Test script to debug markdown processing issues
"""

import markdown

# Test markdown content with lists - CORRECTED VERSION
test_content_fixed = """
### **VIP and Sponsor Tickets Without the Hassle**
**Stop manually managing free tickets.** Our new system handles complimentary tickets automatically while keeping your finances clear.

**Perfect for:**

- **Press and media** - Send professional tickets instantly
- **Sponsors and donors** - Show appreciation with easy comp tickets
- **VIP guests** - Handle special attendees seamlessly
- **Staff and volunteers** - Reward your team without paperwork

**Built-in benefits:**

- **Separate tracking** so you know your real revenue vs. comps
- **Automatic emails** with professional tickets
- **Capacity protection** - comps won't oversell your event
- **Easy reporting** for sponsors and stakeholders
"""

print("Testing corrected markdown with proper spacing:")
print("=" * 50)

# Test with extra extension
md = markdown.Markdown(extensions=['extra'])
result = md.convert(test_content_fixed)
print(result)