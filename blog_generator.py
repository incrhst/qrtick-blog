#!/usr/bin/env python3
"""
QRTick Blog Generator - Modern Edition

This script reads markdown files from the blog folder and generates:
1. Individual HTML blog post pages
2. A blog index page listing all entries
3. Modern, clean styling inspired by contemporary blog designs
"""

import os
import re
import markdown
import yaml
import shutil
from datetime import datetime
from pathlib import Path

class BlogGenerator:
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
    
    def get_html_template(self):
        """Modern HTML template inspired by clean blog designs"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - QRTick Blog</title>
    <meta name="description" content="{description}">
    <link rel="icon" type="image/png" sizes="32x32" href="../icon-32x32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="../icon-192x192.png">
    <link rel="apple-touch-icon" sizes="180x180" href="../icon-180x180.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
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
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .header-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            height: 40px;
            width: auto;
        }}
        
        .nav-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav-link {{
            color: #666666;
            text-decoration: none;
            font-weight: 500;
            font-size: 15px;
            transition: color 0.2s;
        }}
        
        .nav-link:hover {{
            color: #2D2D2D;
        }}
        
        .nav-link.primary {{
            background: #2D2D2D;
            color: #FFFFFF;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: background 0.2s;
        }}
        
        .nav-link.primary:hover {{
            background: #1A1A1A;
            color: #FFFFFF;
        }}
        
        .main-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}
        
        .post-header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid #E5E5E5;
        }}
        
        .post-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #2D2D2D;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        
        .post-meta {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            color: #666666;
            font-size: 0.9rem;
            align-items: center;
        }}
        
        .post-meta span {{
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}
        
        .blog-content {{
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        .blog-content h1 {{
            font-size: 2.25rem;
            font-weight: 700;
            color: #2D2D2D;
            margin: 2.5rem 0 1rem 0;
            letter-spacing: -0.02em;
        }}
        
        .blog-content h2 {{
            font-size: 1.75rem;
            font-weight: 600;
            color: #2D2D2D;
            margin: 2rem 0 1rem 0;
            letter-spacing: -0.01em;
        }}
        
        .blog-content h3 {{
            font-size: 1.375rem;
            font-weight: 600;
            color: #2D2D2D;
            margin: 1.5rem 0 0.75rem 0;
        }}
        
        .blog-content p {{
            margin-bottom: 1.5rem;
            color: #2D2D2D;
        }}
        
        .blog-content strong {{
            font-weight: 600;
            color: #1A1A1A;
        }}
        
        .blog-content ul, .blog-content ol {{
            margin: 1.5rem 0;
            padding-left: 1.5rem;
        }}
        
        .blog-content li {{
            margin-bottom: 0.75rem;
            color: #2D2D2D;
        }}
        
        .blog-content blockquote {{
            border-left: 4px solid #FDC230;
            margin: 2rem 0;
            padding: 1.5rem 0 1.5rem 2rem;
            background: #FFF9EA;
            border-radius: 0 8px 8px 0;
            font-style: italic;
            color: #2D2D2D;
        }}
        
        .blog-content code {{
            background: #F5F5F5;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'SF Mono', Monaco, Menlo, Consolas, monospace;
            font-size: 0.9em;
        }}
        
        .blog-content pre {{
            background: #F5F5F5;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5rem 0;
        }}
        
        .blog-content pre code {{
            background: none;
            padding: 0;
        }}
        
        .blog-content img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            margin: 2rem 0;
            display: block;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }}
        
        .back-to-blog {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #666666;
            text-decoration: none;
            font-weight: 500;
            margin-bottom: 2rem;
            padding: 0.75rem 0;
            transition: color 0.2s;
        }}
        
        .back-to-blog:hover {{
            color: #2D2D2D;
        }}
        
        .footer {{
            background: #F8F9FA;
            padding: 3rem 0 2rem 0;
            margin-top: 4rem;
            border-top: 1px solid #E5E5E5;
            text-align: center;
        }}
        
        .footer-content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .footer-logo {{
            height: 32px;
            margin-bottom: 1rem;
        }}
        
        .footer-text {{
            color: #666666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 2rem;
        }}
        
        .footer-link {{
            color: #666666;
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.2s;
        }}
        
        .footer-link:hover {{
            color: #2D2D2D;
        }}
        
        @media (max-width: 768px) {{
            .header-container {{
                padding: 0 1rem;
            }}
            
            .nav-links {{
                gap: 1rem;
            }}
            
            .main-container {{
                padding: 2rem 1rem;
            }}
            
            .post-title {{
                font-size: 2rem;
            }}
            
            .post-meta {{
                flex-direction: column;
                gap: 0.5rem;
            }}
            
            .blog-content {{
                font-size: 1rem;
            }}
            
            .blog-content h1 {{
                font-size: 1.75rem;
            }}
            
            .blog-content h2 {{
                font-size: 1.5rem;
            }}
            
            .footer-links {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-container">
            <a href="https://qrtick.com" target="_blank" rel="noopener noreferrer">
                <img src="qrtick-logo-alt.svg" alt="QRTick" class="logo">
            </a>
            <nav class="nav-links">
                <a href="index.html" class="nav-link">Blog</a>
                <a href="../index.html" class="nav-link">Docs</a>
                <a href="https://qrtick.com" class="nav-link" target="_blank" rel="noopener noreferrer">QRTick.com</a>
                <a href="https://qrtick.com" class="nav-link primary" target="_blank" rel="noopener noreferrer">Try QRTick</a>
            </nav>
        </div>
    </header>
    
    {content}
    
    <footer class="footer">
        <div class="footer-content">
            <img src="qrtick-logo-alt.svg" alt="QRTick" class="footer-logo">
            <p class="footer-text">Making event management stress-free for organizers across Jamaica</p>
            <div class="footer-links">
                <a href="https://qrtick.com" class="footer-link" target="_blank" rel="noopener noreferrer">QRTick.com</a>
                <a href="../index.html" class="footer-link">Documentation</a>
                <a href="index.html" class="footer-link">Blog Home</a>
            </div>
        </div>
    </footer>
</body>
</html>"""

    def get_index_template(self):
        """Template for the blog index page"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The QR Code - QRTick Blog</title>
    <meta name="description" content="Making event management stress-free for organizers across Jamaica. Tips, insights, and solutions for better events.">
    <link rel="icon" type="image/png" sizes="32x32" href="../icon-32x32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="../icon-192x192.png">
    <link rel="apple-touch-icon" sizes="180x180" href="../icon-180x180.png">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
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
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .header-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            height: 40px;
            width: auto;
        }}
        
        .nav-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav-link {{
            color: #666666;
            text-decoration: none;
            font-weight: 500;
            font-size: 15px;
            transition: color 0.2s;
        }}
        
        .nav-link:hover {{
            color: #2D2D2D;
        }}
        
        .nav-link.primary {{
            background: #2D2D2D;
            color: #FFFFFF;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: background 0.2s;
        }}
        
        .nav-link.primary:hover {{
            background: #1A1A1A;
            color: #FFFFFF;
        }}
        
        .hero-section {{
            background: linear-gradient(135deg, #FFF9EA 0%, #FFFFFF 100%);
            padding: 4rem 0 3rem 0;
            text-align: center;
            border-bottom: 1px solid #E5E5E5;
        }}
        
        .hero-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .blog-title {{
            font-size: 3rem;
            font-weight: 700;
            color: #2D2D2D;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }}
        
        .blog-subtitle {{
            font-size: 1.25rem;
            color: #666666;
            font-weight: 400;
            margin-bottom: 0.5rem;
        }}
        
        .blog-tagline {{
            font-size: 1rem;
            color: #888888;
            margin-top: 0.5rem;
        }}
        
        .main-container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}
        
        .featured-post {{
            background: linear-gradient(135deg, #FFF9EA 0%, #FFFFFF 100%);
            border: 1px solid #E5E5E5;
            border-radius: 16px;
            padding: 2.5rem;
            margin-bottom: 3rem;
            position: relative;
            overflow: hidden;
        }}
        
        .featured-badge {{
            position: absolute;
            top: 1.5rem;
            right: 1.5rem;
            background: #FDC230;
            color: #2D2D2D;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .featured-post h2 {{
            font-size: 2rem;
            font-weight: 700;
            color: #2D2D2D;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
            line-height: 1.3;
        }}
        
        .featured-post h2 a {{
            color: #2D2D2D;
            text-decoration: none;
        }}
        
        .featured-post h2 a:hover {{
            color: #1A1A1A;
        }}
        
        .blog-post {{
            border-bottom: 1px solid #E5E5E5;
            padding: 2rem 0;
            transition: transform 0.2s;
        }}
        
        .blog-post:last-child {{
            border-bottom: none;
        }}
        
        .blog-post:hover {{
            transform: translateY(-2px);
        }}
        
        .blog-post h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #2D2D2D;
            margin-bottom: 0.75rem;
            letter-spacing: -0.01em;
            line-height: 1.4;
        }}
        
        .blog-post h2 a {{
            color: #2D2D2D;
            text-decoration: none;
        }}
        
        .blog-post h2 a:hover {{
            color: #1A1A1A;
        }}
        
        .blog-meta {{
            font-size: 0.9rem;
            color: #666666;
            margin-bottom: 1rem;
            display: flex;
            gap: 1rem;
            align-items: center;
        }}
        
        .blog-meta span {{
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}
        
        .blog-excerpt {{
            margin-bottom: 1.5rem;
            line-height: 1.7;
            color: #2D2D2D;
        }}
        
        .read-more {{
            color: #666666;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: color 0.2s;
        }}
        
        .read-more:hover {{
            color: #2D2D2D;
        }}
        
        .read-more::after {{
            content: '→';
            transition: transform 0.2s;
        }}
        
        .read-more:hover::after {{
            transform: translateX(2px);
        }}
        
        .tags {{
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }}
        
        .tag {{
            background: #F5F5F5;
            color: #666666;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            text-decoration: none;
            transition: all 0.2s;
        }}
        
        .tag:hover {{
            background: #E5E5E5;
            color: #2D2D2D;
        }}
        
        .footer {{
            background: #F8F9FA;
            padding: 3rem 0 2rem 0;
            margin-top: 4rem;
            border-top: 1px solid #E5E5E5;
            text-align: center;
        }}
        
        .footer-content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .footer-logo {{
            height: 32px;
            margin-bottom: 1rem;
        }}
        
        .footer-text {{
            color: #666666;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }}
        
        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 2rem;
        }}
        
        .footer-link {{
            color: #666666;
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.2s;
        }}
        
        .footer-link:hover {{
            color: #2D2D2D;
        }}
        
        @media (max-width: 768px) {{
            .header-container {{
                padding: 0 1rem;
            }}
            
            .nav-links {{
                gap: 1rem;
            }}
            
            .blog-title {{
                font-size: 2.25rem;
            }}
            
            .blog-subtitle {{
                font-size: 1.1rem;
            }}
            
            .main-container {{
                padding: 2rem 1rem;
            }}
            
            .featured-post {{
                padding: 2rem;
            }}
            
            .featured-post h2 {{
                font-size: 1.75rem;
            }}
            
            .blog-meta {{
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }}
            
            .footer-links {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-container">
            <a href="https://qrtick.com" target="_blank" rel="noopener noreferrer">
                <img src="qrtick-logo-alt.svg" alt="QRTick" class="logo">
            </a>
            <nav class="nav-links">
                <a href="index.html" class="nav-link">Blog</a>
                <a href="../index.html" class="nav-link">Docs</a>
                <a href="https://qrtick.com" class="nav-link" target="_blank" rel="noopener noreferrer">QRTick.com</a>
                <a href="https://qrtick.com" class="nav-link primary" target="_blank" rel="noopener noreferrer">Try QRTick</a>
            </nav>
        </div>
    </header>
    
    <div class="hero-section">
        <div class="hero-container">
            <h1 class="blog-title">The QR Code</h1>
            <p class="blog-subtitle">Making event management stress-free for organizers across Jamaica</p>
            <p class="blog-tagline">Tips, insights, and solutions for better events</p>
        </div>
    </div>
    
    <main class="main-container">
        {posts}
    </main>
    
    <footer class="footer">
        <div class="footer-content">
            <img src="qrtick-logo-alt.svg" alt="QRTick" class="footer-logo">
            <p class="footer-text">Making event management stress-free for organizers across Jamaica</p>
            <div class="footer-links">
                <a href="https://qrtick.com" class="footer-link" target="_blank" rel="noopener noreferrer">QRTick.com</a>
                <a href="../index.html" class="footer-link">Documentation</a>
                <a href="index.html" class="footer-link">Blog Home</a>
            </div>
        </div>
    </footer>
</body>
</html>"""

    def parse_frontmatter(self, content):
        """Parse YAML frontmatter from markdown content"""
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    markdown_content = parts[2].strip()
                    return frontmatter, markdown_content
            except yaml.YAMLError:
                pass
        return {}, content
    
    def generate_post_html(self, post_data, content_html):
        """Generate HTML for individual blog post"""
        read_time = max(1, len(content_html.split()) // 200)  # Estimate reading time
        
        post_content = f"""
        <main class="main-container">
            <a href="index.html" class="back-to-blog">← Back to Blog</a>
            
            <article>
                <header class="post-header">
                    <h1 class="post-title">{post_data.get('title', 'Untitled')}</h1>
                    <div class="post-meta">
                        <span>📅 {post_data.get('date', 'Unknown Date')}</span>
                        <span>👤 {post_data.get('author', 'QRTick Team')}</span>
                        <span>⏱️ {read_time} min read</span>
                    </div>
                </header>
                
                <div class="blog-content">
                    {content_html}
                </div>
            </article>
        </main>
        """
        
        return self.get_html_template().format(
            title=post_data.get('title', 'Untitled'),
            description=post_data.get('excerpt', 'QRTick Blog Post'),
            content=post_content
        )
    
    def generate_index_html(self, posts):
        """Generate HTML for blog index page"""
        posts_html = ""
        
        # Sort posts: pinned first, then featured, then by date
        sorted_posts = sorted(posts, key=lambda p: (
            not p['data'].get('pinned', False),
            not p['data'].get('featured', False),
            self.parse_date(p['data'].get('date')).timestamp()
        ), reverse=True)
        
        for i, post in enumerate(sorted_posts):
            post_data = post['data']
            tags_html = ""
            
            if post_data.get('tags'):
                tags_html = '<div class="tags">' + ''.join([
                    f'<span class="tag">#{tag}</span>' for tag in post_data['tags'][:4]
                ]) + '</div>'
            
            read_time = max(1, len(post['content'].split()) // 200)
            
            # Featured post gets special treatment
            if i == 0 and (post_data.get('featured') or post_data.get('pinned')):
                posts_html += f"""
                <article class="featured-post">
                    {'<div class="featured-badge">Featured</div>' if post_data.get('featured') else ''}
                    <h2><a href="{post_data.get('slug', 'untitled')}.html">{post_data.get('title', 'Untitled')}</a></h2>
                    <div class="blog-meta">
                        <span>📅 {post_data.get('date', 'Unknown Date')}</span>
                        <span>👤 {post_data.get('author', 'QRTick Team')}</span>
                        <span>⏱️ {read_time} min read</span>
                    </div>
                    <div class="blog-excerpt">{post_data.get('excerpt', 'No excerpt available.')}</div>
                    <a href="{post_data.get('slug', 'untitled')}.html" class="read-more">Read full post</a>
                    {tags_html}
                </article>
                """
            else:
                posts_html += f"""
                <article class="blog-post">
                    <h2><a href="{post_data.get('slug', 'untitled')}.html">{post_data.get('title', 'Untitled')}</a></h2>
                    <div class="blog-meta">
                        <span>📅 {post_data.get('date', 'Unknown Date')}</span>
                        <span>👤 {post_data.get('author', 'QRTick Team')}</span>
                        <span>⏱️ {read_time} min read</span>
                    </div>
                    <div class="blog-excerpt">{post_data.get('excerpt', 'No excerpt available.')}</div>
                    <a href="{post_data.get('slug', 'untitled')}.html" class="read-more">Read full post</a>
                    {tags_html}
                </article>
                """
        
        return self.get_index_template().format(posts=posts_html)
    
    def copy_images(self):
        """Copy images directory to output directory"""
        images_source = Path("images")
        images_dest = self.output_dir / "images"
        
        if images_source.exists():
            # Remove existing images directory if it exists
            if images_dest.exists():
                shutil.rmtree(images_dest)
            
            # Copy entire images directory
            shutil.copytree(images_source, images_dest)
            print("🖼️  Copied images directory to output")
        else:
            print("⚠️  No images directory found")
    
    def generate_blog(self):
        """Main function to generate the entire blog"""
        print("🚀 Generating QRTick Blog...")
        
        # Ensure logo is copied to output directory
        logo_source = Path("qrtick-logo-alt.svg")
        logo_dest = self.output_dir / "qrtick-logo-alt.svg"
        if logo_source.exists():
            shutil.copy2(logo_source, logo_dest)
            print("📄 Copied logo to output directory")
        
        # Copy images directory
        self.copy_images()
        
        # Process all markdown files
        posts = []
        markdown_processor = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code'
        ])
        
        for md_file in self.blog_dir.glob("*.md"):
            print(f"📝 Processing: {md_file.name}")
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse frontmatter and content
                frontmatter, markdown_content = self.parse_frontmatter(content)
                
                # Convert markdown to HTML
                content_html = markdown_processor.convert(markdown_content)
                
                # Fix image paths - remove ./ prefix since HTML files are in root of blog_html
                content_html = content_html.replace('src="./images/', 'src="images/')
                
                # Generate slug if not provided
                slug = frontmatter.get('slug') or re.sub(r'[^a-zA-Z0-9\-_]', '-', frontmatter.get('title', md_file.stem).lower()).strip('-')
                frontmatter['slug'] = slug
                
                # Generate individual post HTML
                post_html = self.generate_post_html(frontmatter, content_html)
                
                # Write post file
                post_file = self.output_dir / f"{slug}.html"
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(post_html)
                
                # Store post data for index generation
                posts.append({
                    'data': frontmatter,
                    'content': markdown_content
                })
                
                print(f"✅ Generated: {slug}.html")
                
            except Exception as e:
                print(f"❌ Error processing {md_file.name}: {e}")
        
        # Generate index page
        if posts:
            index_html = self.generate_index_html(posts)
            index_file = self.output_dir / "index.html"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_html)
            print(f"🏠 Generated blog index with {len(posts)} posts")
        else:
            print("⚠️ No posts found to generate index")
        
        print(f"🎉 Blog generation complete! View at {self.output_dir}/index.html")

def main():
    """Main function to run the blog generator"""
    import sys
    
    # Check if required libraries are available
    try:
        import markdown
        import yaml
    except ImportError as e:
        print(f"Error: Missing required library: {e}")
        print("Install with: pip install markdown PyYAML")
        sys.exit(1)
    
    generator = BlogGenerator()
    generator.generate_blog()

if __name__ == "__main__":
    main()