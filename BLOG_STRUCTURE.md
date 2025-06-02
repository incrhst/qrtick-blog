# The QR Code Blog Structure Guide

This guide explains how to create and structure blog posts for "The QR Code" - QRTick's event technology blog.

## YAML Frontmatter Structure

Every blog post must start with YAML frontmatter enclosed in triple dashes. Here's the complete structure:

```yaml
---
title: "Your Blog Post Title"
date: "Month Year" or "Month Day, Year"
author: "Author Name"
slug: "url-friendly-slug"
excerpt: "Brief description of the post for previews and SEO"
tags: ["tag1", "tag2", "tag3"]
featured: true/false (optional)
pinned: true/false (optional)
---
```

## Required Fields

### `title`
- **Type**: String (quoted)
- **Purpose**: The main headline of your blog post
- **Example**: `"The Future of Event Technology"`
- **Best Practices**: 
  - Keep under 60 characters for SEO
  - Use title case
  - Be descriptive and engaging

### `date`
- **Type**: String (quoted)
- **Purpose**: Publication date
- **Formats**: 
  - `"January 2025"` (month and year)
  - `"January 15, 2025"` (full date)
- **Example**: `"June 2025"`

### `author`
- **Type**: String (quoted)
- **Purpose**: Who wrote the post
- **Common Values**: 
  - `"QRTick Team"`
  - `"David Brown"`
  - `"Guest Author Name"`

### `slug`
- **Type**: String (quoted)
- **Purpose**: URL-friendly identifier for the post
- **Rules**:
  - Use lowercase letters
  - Replace spaces with hyphens
  - No special characters
  - Keep it descriptive but concise
- **Example**: `"future-of-event-technology-qr-codes"`

### `excerpt`
- **Type**: String (quoted)
- **Purpose**: Brief summary for blog index and SEO
- **Best Practices**:
  - 150-300 characters
  - Compelling and informative
  - Include relevant keywords

### `tags`
- **Type**: Array of strings
- **Purpose**: Categorize content for organization and discovery
- **Format**: `["tag1", "tag2", "tag3"]`
- **Common Tags**:
  - `"qr-codes"`
  - `"event-technology"`
  - `"digital-transformation"`
  - `"event-management"`
  - `"best-practices"`
  - `"updates"`
  - `"analytics"`
  - `"jamaica"`
  - `"case-studies"`

## Optional Fields

### `featured`
- **Type**: Boolean (true/false)
- **Purpose**: Mark important posts for special highlighting
- **Default**: false if not specified

### `pinned`
- **Type**: Boolean (true/false)
- **Purpose**: Keep post at top of blog index
- **Default**: false if not specified

## Content Structure

After the YAML frontmatter, structure your content following these guidelines:

### Main Heading
```markdown
# Your Main Title
## Optional Subtitle

**Brief compelling introduction**
```

### Section Organization
Use H2 (##) for main sections and H3 (###) for subsections:

```markdown
## 🎯 **Main Section Title**

### **Subsection Title**

Content here...

---

## 📱 **Next Main Section**
```

### Visual Elements
- Use emojis in section headers for visual appeal
- Bold important phrases with **text**
- Use horizontal rules (---) to separate major sections
- Include code blocks for technical examples

## File Naming Convention

### Markdown Files
- Use descriptive names with hyphens
- Keep filenames under 50 characters
- Example: `the-future-of-event-technology.md`

### Generated HTML Files
The system automatically generates HTML files based on the `slug` field:
- `slug: "future-of-event-technology-qr-codes"`
- Generates: `future-of-event-technology-qr-codes.html`

## Blog Post Types

### 1. Feature Updates
For QRTick platform updates and new features:

```yaml
---
title: "What's New in QRTick: [Month Year]"
tags: ["updates", "features", "platform"]
---
```

### 2. Technology Deep Dives
For technical education and best practices:

```yaml
---
title: "Understanding [Technology Topic]"
tags: ["qr-codes", "event-technology", "best-practices"]
---
```

### 3. Case Studies
For real-world event examples:

```yaml
---
title: "[Event Name]: A Case Study in [Technology/Approach]"
tags: ["case-studies", "jamaica", "event-management"]
---
```

### 4. Industry Insights
For trend analysis and thought leadership:

```yaml
---
title: "The Future of [Topic]"
tags: ["trends", "industry-insights", "digital-transformation"]
---
```

## SEO Best Practices

### Title Optimization
- Include primary keyword
- Keep under 60 characters
- Make it compelling and clickable

### Excerpt Optimization
- Include relevant keywords naturally
- Provide genuine value preview
- Keep between 150-300 characters

### Tag Strategy
- Use 3-8 tags per post
- Mix broad and specific tags
- Be consistent with tag naming

## Content Guidelines

### Voice and Tone
Following QRTick brand guidelines:
- **Tech-savvy and professional**
- **Solution-focused with technical precision**
- **Understanding of event organizers' challenges**
- **Emphasis on efficiency, security, and data-driven insights**

### Content Standards
- Always include actionable insights
- Back claims with data when possible
- Use Jamaica-specific examples where relevant
- Focus on ROI and practical benefits
- Include specific metrics and numbers

## File Organization

```
qrtick-blog/
├── blog/
│   ├── welcome-to-the-qr-code.md
│   ├── the-future-of-event-technology.md
│   ├── qrtick_updates_june_2025.md
│   └── [new-blog-post].md
├── blog_html/
│   ├── index.html (blog homepage)
│   ├── [slug].html (individual posts)
│   └── ...
├── blog_generator.py
├── requirements.txt
└── BLOG_STRUCTURE.md (this file)
```

## Creating a New Blog Post

1. **Create the markdown file** in the `blog/` directory
2. **Add YAML frontmatter** at the top
3. **Write your content** following the structure guidelines
4. **Run the generator**: `python blog_generator.py`
5. **Check the output** in `blog_html/`

## Example Complete Blog Post

```markdown
---
title: "5 Ways QR Codes Are Transforming Jamaican Events"
date: "February 2025"
author: "QRTick Team"
slug: "qr-codes-transforming-jamaican-events"
excerpt: "Discover how event organizers across Jamaica are using QR codes to streamline operations, enhance attendee experience, and drive better results."
tags: ["qr-codes", "jamaica", "case-studies", "event-management"]
featured: true
---

# 5 Ways QR Codes Are Transforming Jamaican Events
## Real Results from Real Events

**How local event organizers are achieving 85% faster check-ins and happier attendees**

---

## 🎯 **The Transformation in Numbers**

[Your content continues here...]
```

## Questions?

For questions about blog structure or content guidelines, refer to the QRTick Brand Docs or contact the QRTick team.

Remember: Every post should provide immediate value to event organizers while positioning QRTick as the leading event technology solution in Jamaica. 