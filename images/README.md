# Images Directory Organization

## 📁 Directory Structure

```
images/
├── README.md (this file)
├── blog-posts/          # General blog post images
├── screenshots/         # QRTick platform screenshots
├── ui-examples/         # Before/after interface comparisons
├── logos/              # QRTick and partner logos
└── [post-slug]/        # Specific images for individual posts
```

## 🖼️ How to Use Images in Blog Posts

### **Reference Images in Markdown**

In your blog post markdown files, reference images like this:

```markdown
![Alt text](./images/screenshots/dashboard-overview.png)
```

### **Image Naming Convention**

Use descriptive, lowercase names with hyphens:
- ✅ `digital-programme-mobile.png`
- ✅ `sales-control-dashboard.png`
- ✅ `paypal-checkout-flow.png`
- ❌ `Screenshot 2025-01-15.png`
- ❌ `image1.jpg`

### **Recommended Image Specs**

**Screenshots:**
- Format: PNG for UI screenshots, JPG for photos
- Width: 1200px max (responsive design will scale down)
- File size: Under 500KB for fast loading
- Use 2x density for crisp display on high-DPI screens

**Before/After Comparisons:**
- Same dimensions for both images
- Clear, readable text
- Highlight differences with arrows or boxes

## 📂 Directory Usage

### **blog-posts/**
General images that could be used across multiple posts:
- Event organizer photos (stock)
- General QRTick branding
- Generic event photos

### **screenshots/**
QRTick platform screenshots:
- Dashboard views
- Mobile interfaces
- Admin panels
- Customer-facing screens

### **ui-examples/**
Interface comparisons and examples:
- Before/after redesigns
- Competitor comparisons
- Mobile vs desktop views

### **logos/**
Branding and logo files:
- QRTick logos in different formats
- Partner or event logos
- Social media assets

### **[post-slug]/**
Create a folder named after your blog post slug for post-specific images:
```
images/
└── stop-worrying-about-event-checkin/
    ├── disaster-scenario.jpg
    ├── smooth-checkin.png
    └── volunteer-confidence.jpg
```

## 🔄 Automatic Processing

The blog generator automatically:
- Copies all images to `blog_html/images/`
- Maintains directory structure
- Ensures images are available in generated HTML

## 💡 Best Practices

### **For "What's New" Post Images:**

**Recommended Structure:**
```
images/
└── qrtick-platform-updates-june-2025/
    ├── digital-programme-mobile.png
    ├── digital-programme-desktop.png
    ├── sales-control-dashboard.png
    ├── sales-closed-customer-view.png
    ├── paypal-checkout-options.png
    ├── before-after-interface.png
    ├── comp-ticket-management.png
    ├── revenue-analytics-dashboard.png
    └── real-time-event-insights.png
```

### **Image Optimization:**
- Use tools like TinyPNG to compress images
- Consider using WebP format for modern browsers
- Include alt text that describes the benefit, not just the image

### **Accessibility:**
- Alt text should describe what the image shows
- Focus on the benefit or outcome
- Example: `"Clean mobile interface showing 3-second check-in process"`

## 🎯 Focus on Organizer Benefits

When choosing/creating images:
- Show the outcome, not just the feature
- Include emotional context (relief, confidence, success)
- Use real-world scenarios Jamaica organizers face
- Highlight stress reduction and simplicity

## Questions?

For questions about image requirements or optimization, refer to the main README.md or BLOG_STRUCTURE.md files. 