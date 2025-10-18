#!/usr/bin/env python3
"""
QRTick Blog Generator - AI Optimized Edition

Enhanced blog generator with AI optimization features:
- Jamaica-specific meta tags
- Structured data (JSON-LD)
- Enhanced local SEO
- AI crawler optimization
"""

import os
import re
import markdown
import yaml
import shutil
from datetime import datetime
from pathlib import Path

class AIOptimizedBlogGenerator:
    def __init__(self, blog_dir="blog", output_dir="blog_html"):
        self.blog_dir = Path(blog_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # QRTick brand colors and styling
        self.template_vars = {
            'bg_color': '#FFFFFF',
            'header_bg': '#FFFFFF',
            'accent_color': '#FDC230',
            'text_color': '#2D2D2D',
            'meta_color': '#666666',
            'border_color': '#E5E5E5'
        }
    
    def generate_ai_optimized_meta_tags(self, post_data):
        """Generate AI-optimized meta tags for blog posts"""
        title = post_data.get('title', '')
        excerpt = post_data.get('excerpt', '')
        tags = post_data.get('tags', [])
        
        # Jamaica-specific keywords
        jamaica_keywords = ['Jamaican events', 'Kingston event planning', 'Montego Bay events', 
                           'stress-free organizing', 'QRTick Jamaica', 'local event management']
        
        # Combine post tags with Jamaica keywords
        all_keywords = tags + jamaica_keywords
        keywords_str = ', '.join(all_keywords)
        
        # Enhanced description with local context
        enhanced_description = f"Jamaica's leading event management blog: {excerpt} Stress-free event planning for Jamaican organizers."
        
        return f"""
    <meta name="description" content="{enhanced_description}">
    <meta name="keywords" content="{keywords_str}">
    <meta name="author" content="QRTick Jamaica - Leading Event Technology Platform">
    <meta name="publisher" content="QRTick Jamaica">
    <meta name="geo.region" content="JM">
    <meta name="geo.placename" content="Jamaica">
    <meta name="language" content="en-JM">
    <meta name="geo.country" content="JM">
    <meta name="geo.position" content="18.0179;-76.8099">
    <meta name="last-modified" content="{datetime.now().strftime('%Y-%m-%d')}">
    <meta name="revisit-after" content="1 week">
    
    <!-- Open Graph for Social Media -->
    <meta property="og:title" content="{title} - QRTick Jamaica Blog">
    <meta property="og:description" content="{enhanced_description}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="QRTick Jamaica">
    <meta property="og:locale" content="en_JM">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} - QRTick Jamaica Blog">
    <meta name="twitter:description" content="{enhanced_description}">
    <meta name="twitter:site" content="@QRTickJamaica">
    <meta name="twitter:creator" content="@QRTickJamaica">
    """
    
    def generate_structured_data(self, post_data):
        """Generate JSON-LD structured data for blog posts"""
        title = post_data.get('title', '')
        excerpt = post_data.get('excerpt', '')
        date = post_data.get('date', '')
        slug = post_data.get('slug', '')
        tags = post_data.get('tags', [])
        
        # Parse date for structured data
        try:
            if date:
                parsed_date = datetime.strptime(date, "%B %Y")
                iso_date = parsed_date.strftime("%Y-%m-%d")
            else:
                iso_date = datetime.now().strftime("%Y-%m-%d")
        except:
            iso_date = datetime.now().strftime("%Y-%m-%d")
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": title,
            "description": f"Jamaica's leading event management blog: {excerpt}",
            "author": {
                "@type": "Organization",
                "name": "QRTick Jamaica",
                "url": "https://qrtick.com",
                "description": "Jamaica's leading event technology platform",
                "address": {
                    "@type": "PostalAddress",
                    "addressCountry": "JM",
                    "addressRegion": "Kingston"
                }
            },
            "publisher": {
                "@type": "Organization",
                "name": "QRTick Jamaica",
                "url": "https://qrtick.com",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://qrtick.com/logo.png"
                }
            },
            "datePublished": iso_date,
            "dateModified": iso_date,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://qrtick.com/blog/{slug}"
            },
            "about": {
                "@type": "Thing",
                "name": "Event Management in Jamaica"
            },
            "keywords": tags,
            "inLanguage": "en-JM",
            "isPartOf": {
                "@type": "Blog",
                "name": "The QR Code - QRTick Jamaica Blog",
                "url": "https://qrtick.com/blog"
            }
        }
        
        return f"""
    <script type="application/ld+json">
    {yaml.dump(structured_data, default_flow_style=False, sort_keys=False)}
    </script>
    """
    
    def generate_ai_optimized_template(self, post_data):
        """Generate AI-optimized HTML template"""
        title = post_data.get('title', '')
        excerpt = post_data.get('excerpt', '')
        content = post_data.get('content', '')
        date = post_data.get('date', '')
        author = post_data.get('author', 'QRTick Team')
        tags = post_data.get('tags', [])
        slug = post_data.get('slug', '')
        
        # Generate AI-optimized meta tags
        meta_tags = self.generate_ai_optimized_meta_tags(post_data)
        
        # Generate structured data
        structured_data = self.generate_structured_data(post_data)
        
        # Generate tags HTML
        tags_html = ""
        if tags:
            tags_html = f"""
        <div class="tags">
            <h4>Tags:</h4>
            <div class="tag-list">
                {''.join([f'<span class="tag">{tag}</span>' for tag in tags])}
            </div>
        </div>
        """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - QRTick Jamaica Blog</title>
    {meta_tags}
    <link rel="canonical" href="https://qrtick.com/blog/{slug}">
    <link rel="icon" type="image/png" sizes="32x32" href="https://qrtick.com/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="https://qrtick.com/favicon-192x192.png">
    <link rel="apple-touch-icon" sizes="180x180" href="https://qrtick.com/favicon-180x180.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    {structured_data}
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #FFFFFF;
            color: #2D2D2D;
            line-height: 1.7;
            font-size: 16px;
        }}
        
        .header {{
            background: #FFFFFF;
            border-bottom: 1px solid #E5E5E5;
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 1rem 0;
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #2D2D2D;
            text-decoration: none;
        }}
        
        .nav {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav a {{
            color: #666666;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}
        
        .nav a:hover {{
            color: #FDC230;
        }}
        
        .cta-button {{
            background: #FDC230;
            color: #2D2D2D;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            transition: background 0.2s;
        }}
        
        .cta-button:hover {{
            background: #E6B800;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .post-header {{
            margin-bottom: 3rem;
        }}
        
        .post-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #2D2D2D;
            margin-bottom: 1rem;
            line-height: 1.2;
        }}
        
        .post-meta {{
            color: #666666;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }}
        
        .post-content {{
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        .post-content h1, .post-content h2, .post-content h3 {{
            margin: 2rem 0 1rem 0;
            color: #2D2D2D;
        }}
        
        .post-content h2 {{
            font-size: 1.8rem;
            font-weight: 600;
        }}
        
        .post-content h3 {{
            font-size: 1.4rem;
            font-weight: 600;
        }}
        
        .post-content p {{
            margin-bottom: 1.5rem;
        }}
        
        .post-content ul, .post-content ol {{
            margin: 1.5rem 0;
            padding-left: 2rem;
        }}
        
        .post-content li {{
            margin-bottom: 0.5rem;
        }}
        
        .post-content strong {{
            font-weight: 600;
            color: #2D2D2D;
        }}
        
        .post-content em {{
            font-style: italic;
            color: #666666;
        }}
        
        .tags {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #E5E5E5;
        }}
        
        .tags h4 {{
            margin-bottom: 1rem;
            color: #2D2D2D;
        }}
        
        .tag-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        .tag {{
            background: #F8F9FA;
            color: #666666;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .footer {{
            background: #F8F9FA;
            padding: 2rem 0;
            margin-top: 4rem;
            text-align: center;
        }}
        
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .footer p {{
            color: #666666;
            margin-bottom: 1rem;
        }}
        
        .footer a {{
            color: #FDC230;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .header-content {{
                padding: 0 1rem;
            }}
            
            .nav {{
                gap: 1rem;
            }}
            
            .container {{
                padding: 1rem;
            }}
            
            .post-title {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="https://qrtick.com" class="logo">QRTick Jamaica</a>
            <nav class="nav">
                <a href="https://qrtick.com/blog">Blog</a>
                <a href="https://qrtick.com/support">Support</a>
                <a href="https://qrtick.com">Events</a>
                <a href="https://qrtick.com" class="cta-button">Try QRTick</a>
            </nav>
        </div>
    </header>
    
    <main class="container">
        <article class="post-header">
            <h1 class="post-title">{title}</h1>
            <div class="post-meta">
                <span>By {author}</span> • <span>{date}</span>
            </div>
        </article>
        
        <div class="post-content">
            {content}
        </div>
        
        {tags_html}
    </main>
    
    <footer class="footer">
        <div class="footer-content">
            <p>Part of <a href="https://qrtick.com">QRTick Jamaica</a> - Jamaica's leading event technology platform</p>
            <p>Making event management stress-free for organizers across Jamaica</p>
        </div>
    </footer>
</body>
</html>"""

    def generate_blog_index(self, posts):
        """Generate AI-optimized blog index page"""
        # Sort posts by date (newest first)
        sorted_posts = sorted(posts, key=lambda x: self.parse_date(x.get('date', '')), reverse=True)
        
        # Generate post cards HTML
        post_cards = ""
        for post in sorted_posts:
            title = post.get('title', '')
            excerpt = post.get('excerpt', '')
            date = post.get('date', '')
            slug = post.get('slug', '')
            tags = post.get('tags', [])
            featured = post.get('featured', False)
            pinned = post.get('pinned', False)
            
            # Calculate reading time (approximate)
            content = post.get('content', '')
            word_count = len(content.split())
            reading_time = max(1, word_count // 200)
            
            # Generate tags HTML
            tags_html = ""
            if tags:
                tags_html = f"""
                <div class="post-tags">
                    {''.join([f'<span class="tag">{tag}</span>' for tag in tags[:3]])}
                </div>
                """
            
            # Featured post styling
            card_class = "post-card"
            if featured or pinned:
                card_class += " featured-post"
            
            post_cards += f"""
            <article class="{card_class}">
                <div class="post-content">
                    <h2 class="post-title">
                        <a href="{slug}.html">{title}</a>
                    </h2>
                    <p class="post-excerpt">{excerpt}</p>
                    {tags_html}
                </div>
                <div class="post-meta">
                    <span class="post-date">{date}</span>
                    <span class="reading-time">{reading_time} min read</span>
                </div>
            </article>
            """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The QR Code - QRTick Jamaica Blog</title>
    <meta name="description" content="Jamaica's leading event management blog. Stress-free event planning, organizer support, and practical solutions for Jamaican event organizers.">
    <meta name="keywords" content="Jamaican events, Kingston event planning, Montego Bay events, stress-free organizing, QRTick Jamaica, event management blog">
    <meta name="author" content="QRTick Jamaica - Leading Event Technology Platform">
    <meta name="geo.region" content="JM">
    <meta name="geo.placename" content="Jamaica">
    <link rel="canonical" href="https://qrtick.com/blog">
    <link rel="icon" type="image/png" sizes="32x32" href="https://qrtick.com/favicon-32x32.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "The QR Code - QRTick Jamaica Blog",
        "description": "Jamaica's leading event management blog focused on stress-free event planning",
        "url": "https://qrtick.com/blog",
        "publisher": {{
            "@type": "Organization",
            "name": "QRTick Jamaica",
            "url": "https://qrtick.com"
        }},
        "inLanguage": "en-JM"
    }}
    </script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #FFFFFF;
            color: #2D2D2D;
            line-height: 1.7;
        }}
        
        .header {{
            background: #FFFFFF;
            border-bottom: 1px solid #E5E5E5;
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 1rem 0;
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #2D2D2D;
            text-decoration: none;
        }}
        
        .nav {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav a {{
            color: #666666;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}
        
        .nav a:hover {{
            color: #FDC230;
        }}
        
        .cta-button {{
            background: #FDC230;
            color: #2D2D2D;
            padding: 0.75rem 1.5rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            transition: background 0.2s;
        }}
        
        .cta-button:hover {{
            background: #E6B800;
        }}
        
        .hero {{
            background: linear-gradient(135deg, #FFF9EA 0%, #FFFFFF 100%);
            padding: 4rem 0;
            text-align: center;
        }}
        
        .hero-content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            font-weight: 700;
            color: #2D2D2D;
            margin-bottom: 1rem;
        }}
        
        .hero p {{
            font-size: 1.2rem;
            color: #666666;
            margin-bottom: 2rem;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 4rem 2rem;
        }}
        
        .post-card {{
            border-bottom: 1px solid #E5E5E5;
            padding: 2rem 0;
            transition: transform 0.2s;
        }}
        
        .post-card:hover {{
            transform: translateY(-2px);
        }}
        
        .featured-post {{
            background: linear-gradient(135deg, #FFF9EA 0%, #FFFFFF 100%);
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid #FDC230;
        }}
        
        .post-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        
        .post-title a {{
            color: #2D2D2D;
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .post-title a:hover {{
            color: #FDC230;
        }}
        
        .post-excerpt {{
            color: #666666;
            margin-bottom: 1rem;
        }}
        
        .post-tags {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}
        
        .tag {{
            background: #F8F9FA;
            color: #666666;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }}
        
        .post-meta {{
            display: flex;
            gap: 1rem;
            color: #666666;
            font-size: 0.9rem;
        }}
        
        .footer {{
            background: #F8F9FA;
            padding: 2rem 0;
            margin-top: 4rem;
            text-align: center;
        }}
        
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .footer p {{
            color: #666666;
            margin-bottom: 1rem;
        }}
        
        .footer a {{
            color: #FDC230;
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .container {{
                padding: 2rem 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <a href="https://qrtick.com" class="logo">QRTick Jamaica</a>
            <nav class="nav">
                <a href="https://qrtick.com/blog">Blog</a>
                <a href="https://qrtick.com/support">Support</a>
                <a href="https://qrtick.com">Events</a>
                <a href="https://qrtick.com" class="cta-button">Try QRTick</a>
            </nav>
        </div>
    </header>
    
    <section class="hero">
        <div class="hero-content">
            <h1>The QR Code</h1>
            <p>Making event management stress-free for organizers across Jamaica</p>
        </div>
    </section>
    
    <main class="container">
        {post_cards}
    </main>
    
    <footer class="footer">
        <div class="footer-content">
            <p>Part of <a href="https://qrtick.com">QRTick Jamaica</a> - Jamaica's leading event technology platform</p>
            <p>Making event management stress-free for organizers across Jamaica</p>
        </div>
    </footer>
</body>
</html>"""

    def parse_date(self, date_str):
        """Parse date string in various formats and return a datetime object for sorting"""
        if not date_str:
            return datetime.min
        
        # Remove quotes if present
        date_str = date_str.strip('"\'')
        
        # Try different date formats
        formats = [
            "%B %d, %Y",    # "June 4, 2025"
            "%B %Y",        # "June 2025" 
            "%Y-%m-%d",     # "2025-06-04"
            "%m/%d/%Y",     # "06/04/2025"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # If no format matches, try to extract year and month
        try:
            # Handle formats like "May 2025"
            if re.match(r'^[A-Za-z]+ \d{4}$', date_str):
                # For month-year format, default to first day of month
                return datetime.strptime(date_str, "%B %Y")
        except ValueError:
            pass
        
        # If all else fails, return a very old date so it appears last
        print(f"Warning: Could not parse date '{date_str}', using fallback")
        return datetime.min

    def generate_blog(self):
        """Generate the complete blog with AI optimization"""
        posts = []
        
        # Process all markdown files
        for md_file in self.blog_dir.glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split frontmatter and content
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    markdown_content = parts[2]
                    
                    try:
                        post_data = yaml.safe_load(frontmatter)
                        post_data['content'] = markdown.markdown(markdown_content)
                        posts.append(post_data)
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML in {md_file}: {e}")
                        continue
        
        # Generate individual post pages
        for post in posts:
            slug = post.get('slug', '')
            if slug:
                html_content = self.generate_ai_optimized_template(post)
                output_file = self.output_dir / f"{slug}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"Generated: {output_file}")
        
        # Generate blog index
        index_html = self.generate_blog_index(posts)
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_html)
        print(f"Generated: {index_file}")
        
        print(f"\nBlog generation complete! {len(posts)} posts processed.")
        print("AI optimization features included:")
        print("- Jamaica-specific meta tags")
        print("- Structured data (JSON-LD)")
        print("- Enhanced local SEO")
        print("- AI crawler optimization")

if __name__ == "__main__":
    generator = AIOptimizedBlogGenerator()
    generator.generate_blog()



