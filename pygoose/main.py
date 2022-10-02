import os

import frontmatter
import markdown
from slugify import slugify
from jinja2 import Environment, FileSystemLoader

from pygoose.settings import CONTENT_DIR, LAYOUT_DIR


# Grab all of the data files from the content dir
posts = [
    files for files in os.listdir(f"{CONTENT_DIR}/posts") if os.path.isfile(os.path.join(f"{CONTENT_DIR}/posts", files))
]

pages = [
    pages for pages in os.listdir(f"{CONTENT_DIR}/pages") if os.path.isfile(os.path.join(f"{CONTENT_DIR}/pages", pages))
]


def main():
    # For each file, read the front matter and text
    post_data = []
    for post in posts:
        with open(f"{CONTENT_DIR}/posts/{post}", "r") as file:
            file_data = frontmatter.load(file)
            metadata = file_data.metadata
            metadata['slug'] = slugify(metadata['title'])
            metadata['type'] = 'post'
            content = markdown.markdown(file_data.content)
            post_data.append({"metadata": metadata, "content": content})


    page_data = []
    for page in pages:
        with open(f"{CONTENT_DIR}/pages/{page}", "r") as file:
            file_data = frontmatter.load(file)
            metadata = file_data.metadata
            metadata['slug'] = slugify(metadata['title'])
            metadata['type'] = 'page'
            content = markdown.markdown(file_data.content)
            page_data.append({"metadata": metadata, "content": content})


    # Render the home page and save it in the dist directory
    env = Environment(loader=FileSystemLoader(LAYOUT_DIR))

    template = env.get_template('/_default/list.html')

    all_data = post_data + page_data
    all_metadata = [data["metadata"] for data in all_data]
    all_metadata.sort(key=lambda x: x["date"], reverse=True)

    rendered_template = template.render(data=all_metadata)

    os.makedirs("dist", exist_ok=True)
    with open('dist/index.html', 'w') as file:
        file.write(rendered_template)


    # Loop through each file and render into template
    for data in all_data:
        type = data["metadata"]["type"]
        # template = env.get_template(f"{type}.html")
        template = env.get_template(f"./_default/single.html")
        rendered_template = template.render(data=data)
        os.makedirs(f"dist/{type}s", exist_ok=True)
        with open(f"dist/{type}s/{data['metadata']['slug']}.html", "w") as file:
            file.write(rendered_template)


    # Copy static files
    os.makedirs("dist/static", exist_ok=True)
    for file in os.listdir("static"):
        with open(f"static/{file}", "r") as f:
            with open(f"dist/static/{file}", "w") as f2:
                f2.write(f.read())