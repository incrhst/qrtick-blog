#!/usr/bin/env python3
"""
Generate footer HTML from Jinja2 template for blog use.
This allows the blog to use the same footer as the main site.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from api
sys.path.append(str(Path(__file__).parent.parent))

from jinja2 import Environment, FileSystemLoader
from api.templates.macros.footer import shared_footer

def generate_footer_html():
    """Generate footer HTML from the shared footer macro."""
    
    # Create a simple Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'))
    
    # Create a template that just renders the footer macro
    template_content = """
{% import "api/templates/macros/footer.html" as footer_macros %}
{{ footer_macros.shared_footer() }}
"""
    
    template = env.from_string(template_content)
    
    # Render the footer
    footer_html = template.render()
    
    return footer_html

if __name__ == "__main__":
    footer_html = generate_footer_html()
    print("Generated footer HTML:")
    print(footer_html)



