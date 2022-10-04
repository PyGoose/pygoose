import os
import logging

import frontmatter
import markdown
from slugify import slugify
from jinja2 import Environment, FileSystemLoader

from .config import Config
from .lib.static_files import copy_static_files
from .lib.render_pages import render_template

logging.basicConfig(level=logging.DEBUG)

# Grab all of the data files from the content dir
content_dir_pages = f"{Config.CONTENT_DIR}/pages"
content_dir_posts = f"{Config.CONTENT_DIR}/posts"

posts = [
    files for files in os.listdir(content_dir_posts) if os.path.isfile(os.path.join(content_dir_posts, files))
]
pages = [
    pages for pages in os.listdir(content_dir_pages) if os.path.isfile(os.path.join(content_dir_pages, pages))
]


def main():
    """
    Read Frontmatter and Text From Files
    """
    logging.info("Reading files")
    post_data = []
    for post in posts:
        with open(f"{content_dir_posts}/{post}", "r") as file:
            file_data = frontmatter.load(file)
            metadata = file_data.metadata
            metadata['slug'] = slugify(metadata['title'])
            metadata['type'] = 'post'
            metadata['content'] = markdown.markdown(file_data.content)
            post_data.append({"metadata": metadata})
            
    page_data = []
    for page in pages:
        with open(f"{content_dir_pages}/{page}", "r") as file:
            file_data = frontmatter.load(file)
            metadata = file_data.metadata
            metadata['slug'] = slugify(metadata['title'])
            metadata['type'] = 'page'
            metadata['content'] = markdown.markdown(file_data.content)
            page_data.append({"metadata": metadata})

    # Render the home page and save it in the dist directory
    logging.info("Reading index page")
    env = Environment(loader=FileSystemLoader(Config.LAYOUT_DIR))
    template = env.get_template('/_default/list.html')
    
    all_data = post_data + page_data
    all_metadata = [data["metadata"] for data in all_data]
    all_metadata.sort(key=lambda x: x["date"], reverse=True)
    # Default values for index page
    page_name = Config.SITE_NAME
    page_description = Config.SITE_DESCRIPTION
    page_details = {
        'page_name':page_name,
        'page_description':page_description
    }
    rendered_template = template.render(data=all_metadata,page_details =page_details)
    
    
    try:
        os.makedirs("dist", exist_ok=True)
        file = open('dist/index.html', 'w')
        file.write(rendered_template)
    except Exception as Err:
        logging.error(Err)
    
    try:
        logging.info("Rendering Files")   
        render_template(all_data,template,env)
        logging.info("Copying Static Folder")   
        copy_static_files(Config.STATIC_SRC_PATH,Config.DIST_SRC_PATH)
    except Exception as Err:
        raise Err
 
 
if __name__ == '__main__':
    logging.info("Starting Build...")
    main()
    logging.info("Successfully Build!")
         
    