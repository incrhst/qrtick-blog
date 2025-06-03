#!/usr/bin/env python3
"""
QRTick Blog Generator

This script reads markdown files from the blog folder and generates:
1. Individual HTML blog post pages
2. A blog index page listing all entries
3. Consistent styling matching the QRTick docs design
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
            'bg_color': '#FFF9EA',
            'header_bg': '#3D3939',
            'accent_color': '#FDC230',
            'text_color': '#3D3939',
            'card_bg': '#fff'
        }
    
    def get_html_template(self):
        """Base HTML template matching QRTick docs styling"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - QRTick Blog</title>
    <link rel="icon" type="image/png" sizes="32x32" href="../icon-32x32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="../icon-192x192.png">
    <link rel="apple-touch-icon" sizes="180x180" href="../icon-180x180.png">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Montserrat', 'Roboto', Arial, sans-serif;
            background: #FFF9EA;
            color: #3D3939;
            line-height: 1.6;
        }}
        .header {{
            padding: 2rem 1rem 1rem 1rem;
            text-align: center;
            background-color: #3D3939;
            box-shadow: 0 2px 8px rgba(61, 57, 57, 0.1);
        }}
        .logo {{
            max-width: 180px;
            height: auto;
            margin-bottom: 0.5rem;
        }}
        .nav-links {{
            margin-top: 1rem;
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .nav-link {{
            color: #FDC230;
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: background-color 0.2s;
        }}
        .nav-link:hover {{
            background-color: rgba(253, 194, 48, 0.1);
            text-decoration: underline;
        }}
        .container {{
            max-width: 800px;
            margin: 2rem auto 0 auto;
            padding: 2rem;
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(61, 57, 57, 0.07);
        }}
        .blog-meta {{
            background: #EEEEEE;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            font-size: 0.9rem;
            border-left: 4px solid #FDC230;
        }}
        .blog-content h1 {{
            color: #3D3939;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 0.5rem;
        }}
        .blog-content h2 {{
            color: #3D3939;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #FDC230;
            padding-bottom: 0.5rem;
        }}
        .blog-content h3 {{
            color: #3D3939;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}
        .blog-content p {{
            margin-bottom: 1rem;
        }}
        .blog-content ul, .blog-content ol {{
            margin: 1rem 0;
            padding-left: 2rem;
        }}
        .blog-content li {{
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }}
        .blog-content ul li {{
            list-style-type: disc;
            margin-left: 0;
        }}
        .blog-content ol li {{
            list-style-type: decimal;
            margin-left: 0;
        }}
        .blog-content ul ul li {{
            list-style-type: circle;
        }}
        .blog-content ul ul ul li {{
            list-style-type: square;
        }}
        .blog-content blockquote {{
            border-left: 4px solid #FDC230;
            margin: 1.5rem 0;
            padding-left: 1.5rem;
            font-style: italic;
            background: #FFF9EA;
            padding: 1rem 1rem 1rem 2rem;
            border-radius: 0 8px 8px 0;
        }}
        .blog-content code {{
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
        }}
        .blog-content pre {{
            background: #f4f4f4;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .blog-content pre code {{
            background: none;
            padding: 0;
        }}
        .footer {{
            margin-top: 3rem;
            padding: 2rem 1rem 1rem 1rem;
            background: #3D3939;
            text-align: center;
            color: #EEEEEE;
            font-size: 1rem;
        }}
        .footer-logo {{
            max-width: 120px;
            margin-bottom: 0.5rem;
        }}
        .footer-link {{
            color: #FDC230;
            text-decoration: none;
            font-weight: 600;
        }}
        .footer-link:hover {{
            text-decoration: underline;
        }}
        .back-to-blog {{
            display: inline-block;
            background-color: #FDC230;
            color: #3D3939;
            padding: 0.75rem 1.5rem;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin-bottom: 2rem;
            transition: background-color 0.2s;
        }}
        .back-to-blog:hover {{
            background-color: #e5af2b;
        }}
    </style>
</head>
<body>
    <header class="header">
        <a href="https://qrtick.com" target="_blank" rel="noopener noreferrer">
            <img src="qrtick-logo-alt.svg" alt="QRTick Logo" class="logo">
        </a>
        <div class="nav-links">
            <a href="../index.html" class="nav-link">Docs Home</a>
            <a href="index.html" class="nav-link">Blog</a>
            <a href="https://qrtick.com" class="nav-link" target="_blank" rel="noopener noreferrer">QRTick.com →</a>
        </div>
    </header>
    <main class="container">
        {content}
    </main>
    <footer class="footer">
        <img src="qrtick-logo-alt.svg" alt="QRTick Logo" class="footer-logo">
        <p>&copy; 2025 QRTick. Making events easier to manage and more profitable.</p>
        <p><a href="https://qrtick.com" class="footer-link" target="_blank" rel="noopener noreferrer">Visit QRTick.com</a></p>
    </footer>
</body>
</html>"""

    def get_blog_index_template(self):
        """Template for the blog index page"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The QR Code - QRTick's Event Technology Blog</title>
    <link rel="icon" type="image/png" sizes="32x32" href="../icon-32x32.png">
    <link rel="icon" type="image/png" sizes="192x192" href="../icon-192x192.png">
    <link rel="apple-touch-icon" sizes="180x180" href="../icon-180x180.png">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Montserrat', 'Roboto', Arial, sans-serif;
            background: #FFF9EA;
            color: #3D3939;
        }}
        .header {{
            padding: 2rem 1rem 1rem 1rem;
            text-align: center;
            background-color: #3D3939;
            box-shadow: 0 2px 8px rgba(61, 57, 57, 0.1);
        }}
        .logo {{
            max-width: 180px;
            height: auto;
            margin-bottom: 0.5rem;
        }}
        .nav-links {{
            margin-top: 1rem;
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .nav-link {{
            color: #FDC230;
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: background-color 0.2s;
        }}
        .nav-link:hover {{
            background-color: rgba(253, 194, 48, 0.1);
            text-decoration: underline;
        }}
        .container {{
            max-width: 800px;
            margin: 2rem auto 0 auto;
            padding: 2rem;
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(61, 57, 57, 0.07);
        }}
        .blog-post {{
            background: #FFF9EA;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 1px 4px rgba(61, 57, 57, 0.04);
            border-left: 4px solid #FDC230;
        }}
        .blog-post h2 {{
            margin-top: 0;
            margin-bottom: 0.5rem;
            color: #3D3939;
        }}
        .blog-post h2 a {{
            color: #3D3939;
            text-decoration: none;
        }}
        .blog-post h2 a:hover {{
            color: #1A73E8;
            text-decoration: underline;
        }}
        .blog-meta {{
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 1rem;
        }}
        .blog-excerpt {{
            margin-bottom: 1rem;
            line-height: 1.6;
        }}
        .read-more {{
            display: inline-block;
            background-color: #FDC230;
            color: #3D3939;
            padding: 0.5rem 1rem;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background-color 0.2s;
        }}
        .read-more:hover {{
            background-color: #e5af2b;
        }}
        .footer {{
            margin-top: 3rem;
            padding: 2rem 1rem 1rem 1rem;
            background: #3D3939;
            text-align: center;
            color: #EEEEEE;
            font-size: 1rem;
        }}
        .footer-logo {{
            max-width: 120px;
            margin-bottom: 0.5rem;
        }}
        .footer-link {{
            color: #FDC230;
            text-decoration: none;
            font-weight: 600;
        }}
        .footer-link:hover {{
            text-decoration: underline;
        }}
        h1 {{
            color: #3D3939;
            font-weight: 700;
            letter-spacing: -0.5px;
            text-align: center;
            margin-bottom: 2rem;
        }}
    </style>
</head>
<body>
    <header class="header">
        <a href="https://qrtick.com" target="_blank" rel="noopener noreferrer">
            <img src="qrtick-logo-alt.svg" alt="QRTick Logo" class="logo">
        </a>
        <div class="nav-links">
            <a href="../index.html" class="nav-link">Docs Home</a>
            <a href="index.html" class="nav-link">Blog</a>
            <a href="https://qrtick.com" class="nav-link" target="_blank" rel="noopener noreferrer">QRTick.com →</a>
        </div>
    </header>
    <main class="container">
        <h1>The QR Code</h1>
        <p style="text-align: center; margin-bottom: 3rem; font-size: 1.1rem;">Making event management stress-free for organizers across Jamaica.</p>
        {blog_posts}
    </main>
    <footer class="footer">
        <img src="qrtick-logo-alt.svg" alt="QRTick Logo" class="footer-logo">
        <p>&copy; 2025 QRTick. Making events easier to manage and more profitable.</p>
        <p><a href="https://qrtick.com" class="footer-link" target="_blank" rel="noopener noreferrer">Visit QRTick.com</a></p>
    </footer>
</body>
</html>"""

    def parse_frontmatter(self, content):
        """Parse YAML frontmatter from markdown content"""
        if not content.startswith('---'):
            return {}, content
        
        try:
            # Split content into frontmatter and body
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}, content
            
            frontmatter_text = parts[1].strip()
            body_content = parts[2].strip()
            
            # Parse YAML frontmatter
            frontmatter = yaml.safe_load(frontmatter_text) or {}
            
            return frontmatter, body_content
        except yaml.YAMLError as e:
            print(f"Error parsing YAML frontmatter: {e}")
            return {}, content

    def extract_metadata(self, content):
        """Extract title, date, and excerpt from markdown content with YAML frontmatter support"""
        frontmatter, body_content = self.parse_frontmatter(content)
        
        # Use frontmatter data if available, otherwise extract from content
        title = frontmatter.get('title', 'Blog Post')
        date = frontmatter.get('date', datetime.now().strftime("%B %d, %Y"))
        excerpt = frontmatter.get('excerpt', '')
        author = frontmatter.get('author', 'QRTick Team')
        tags = frontmatter.get('tags', [])
        slug = frontmatter.get('slug', '')
        
        # If no title in frontmatter, extract from first heading
        if title == 'Blog Post':
            lines = body_content.strip().split('\n')
            for line in lines:
                if line.strip().startswith('# '):
                    title = line.strip()[2:].strip()
                    break
        
        # Format date if it's a datetime object
        if isinstance(date, datetime):
            date = date.strftime("%B %d, %Y")
        elif isinstance(date, str):
            # Try to parse common date formats
            date_patterns = [
                r'(\w+ \d{4})',  # "June 2025"
                r'(\w+ \d{1,2}, \d{4})',  # "June 15, 2025"
                r'(\d{4}-\d{2}-\d{2})',  # "2025-06-15"
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, str(date))
                if match:
                    date = match.group(1)
                    break
        
        # Generate excerpt if not provided
        if not excerpt:
            lines = body_content.strip().split('\n')
            content_lines = []
            in_content = False
            for line in lines:
                if line.strip().startswith('#'):
                    in_content = True
                    continue
                if in_content and line.strip() and not line.strip().startswith('*') and not line.strip().startswith('---'):
                    content_lines.append(line.strip())
                    if len(' '.join(content_lines)) > 200:
                        break
            
            if content_lines:
                excerpt = ' '.join(content_lines)[:300]
                if len(excerpt) == 300:
                    excerpt = excerpt.rsplit(' ', 1)[0] + "..."
        
        # Generate slug if not provided
        if not slug:
            slug = re.sub(r'[^a-zA-Z0-9\-_]', '-', title.lower())
            slug = re.sub(r'-+', '-', slug).strip('-')
        
        return {
            'title': title,
            'date': date,
            'excerpt': excerpt,
            'author': author,
            'tags': tags,
            'slug': slug,
            'body_content': body_content
        }

    def markdown_to_html(self, markdown_content):
        """Convert markdown to HTML"""
        # Ensure proper list formatting by preprocessing
        lines = markdown_content.split('\n')
        processed_lines = []
        in_list = False
        
        for i, line in enumerate(lines):
            # Check if this line is a bullet point
            if line.strip().startswith('- '):
                if not in_list:
                    # Add blank line before list if previous line isn't empty
                    if i > 0 and lines[i-1].strip() != '':
                        processed_lines.append('')
                    in_list = True
                processed_lines.append(line)
            else:
                if in_list and line.strip() == '':
                    # Keep empty lines in lists
                    processed_lines.append(line)
                elif in_list and line.strip() != '':
                    # End of list - add blank line after if next line isn't a list item
                    in_list = False
                    processed_lines.append('')
                    processed_lines.append(line)
                else:
                    processed_lines.append(line)
        
        processed_content = '\n'.join(processed_lines)
        
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
        return md.convert(processed_content)

    def generate_blog_post(self, markdown_file):
        """Generate individual blog post HTML"""
        with open(markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata = self.extract_metadata(content)
        html_content = self.markdown_to_html(metadata['body_content'])
        
        # Create blog meta section
        meta_html = f"""
        <a href="index.html" class="back-to-blog">← Back to Blog</a>
        <div class="blog-meta">
            <strong>Published:</strong> {metadata['date']}
        </div>
        <div class="blog-content">
            {html_content}
        </div>
        """
        
        # Generate full HTML
        full_html = self.get_html_template().format(
            title=metadata['title'],
            content=meta_html
        )
        
        # Create output filename
        output_file = self.output_dir / f"{metadata['slug']}.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        return {
            'title': metadata['title'],
            'date': metadata['date'],
            'excerpt': metadata['excerpt'],
            'filename': output_file.name,
            'slug': metadata['slug']
        }

    def generate_blog_index(self, posts):
        """Generate blog index page"""
        blog_posts_html = ""
        
        # Sort posts by date (newest first)
        sorted_posts = sorted(posts, key=lambda x: x['date'], reverse=True)
        
        for post in sorted_posts:
            blog_posts_html += f"""
            <article class="blog-post">
                <h2><a href="{post['filename']}">{post['title']}</a></h2>
                <div class="blog-meta">{post['date']}</div>
                <div class="blog-excerpt">{post['excerpt']}</div>
                <a href="{post['filename']}" class="read-more">Read More →</a>
            </article>
            """
        
        full_html = self.get_blog_index_template().format(
            blog_posts=blog_posts_html
        )
        
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"Generated blog index: {index_file}")

    def copy_static_assets(self):
        """Copy static assets like logo and images to output directory"""
        # Copy logo
        logo_source = Path("qrtick-logo-alt.svg")
        if logo_source.exists():
            logo_dest = self.output_dir / "qrtick-logo-alt.svg"
            shutil.copy2(logo_source, logo_dest)
            print(f"Copied logo: {logo_source} → {logo_dest}")
        else:
            print("Warning: qrtick-logo-alt.svg not found in root directory")
        
        # Copy images directory
        images_source = Path("images")
        if images_source.exists():
            images_dest = self.output_dir / "images"
            if images_dest.exists():
                shutil.rmtree(images_dest)
            shutil.copytree(images_source, images_dest)
            print(f"Copied images: {images_source} → {images_dest}")
        else:
            print("Info: images/ directory not found (create it to include images in blog)")

    def generate_all(self):
        """Generate all blog posts and index"""
        if not self.blog_dir.exists():
            print(f"Blog directory '{self.blog_dir}' not found!")
            return
        
        # Copy static assets first
        self.copy_static_assets()
        
        posts = []
        markdown_files = list(self.blog_dir.glob("*.md"))
        
        if not markdown_files:
            print(f"No markdown files found in '{self.blog_dir}'")
            return
        
        print(f"Found {len(markdown_files)} markdown files")
        
        for md_file in markdown_files:
            print(f"Processing: {md_file.name}")
            try:
                post_data = self.generate_blog_post(md_file)
                posts.append(post_data)
                print(f"Generated: {post_data['filename']}")
            except Exception as e:
                print(f"Error processing {md_file.name}: {e}")
        
        if posts:
            self.generate_blog_index(posts)
            print(f"\nGenerated {len(posts)} blog posts")
            print(f"Blog available at: {self.output_dir}/index.html")
        else:
            print("No blog posts were generated")

def main():
    """Main function to run the blog generator"""
    import sys
    
    # Check if markdown library is available
    try:
        import markdown
    except ImportError:
        print("Error: 'markdown' library not found.")
        print("Install it with: pip install markdown")
        sys.exit(1)
    
    generator = BlogGenerator()
    generator.generate_all()

if __name__ == "__main__":
    main() 