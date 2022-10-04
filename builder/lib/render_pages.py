import os
import logging
from builder.config import Config
"""
Render Templates For Posts And Pages
"""
def render_template(all_data,template,env,page_list):
    for data in all_data:
        type = data["metadata"]["type"]
        template = env.get_template(f"./_default/single.html")
        page_name = data["metadata"]["title"]
        
        try:
            page_author = data["metadata"]["author"]
        except:
            page_author = ""
            
        try:
            page_keywords = data["metadata"]["keywords"]
        except:
            page_keywords = ""
            
        try:
            page_description = data["metadata"]["description"]
        except KeyError:
            page_description = ""
            
        site_name = Config.SITE_NAME
        site_description = Config.SITE_DESCRIPTION
        site_keywords = Config.SITE_KEYWORDS
        site_author = Config.SITE_AUTHOR
        page_details = {
        'site_name':site_name,
        'site_description':site_description,
        'page_name':page_name,
        'page_description':page_description,
        'page_keywords':page_keywords,
        'site_keywords':site_keywords,
        'page_author':page_author,
        'site_author':site_author
    }
        rendered_template = template.render(data=data,page_details = page_details,page_list = page_list,type=type)
        os.makedirs(f"dist/{type}s", exist_ok=True)
        with open(f"dist/{type}s/{data['metadata']['slug']}.html", "w") as file:
            file.write(rendered_template)