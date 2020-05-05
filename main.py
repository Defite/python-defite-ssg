import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

# Define templates
env = Environment(loader=PackageLoader('main', 'templates'))
blog_template = env.get_template('blog.html')
post_template = env.get_template('post.html')

POSTS = {}

# Prepate blog listing
for markdown_post in os.listdir('content'):
  file_path = os.path.join('content', markdown_post)

  with open (file_path, 'r') as file:
    POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])

POSTS_SORTED = sorted(POSTS.items(), key=lambda post: datetime.strptime(POSTS[post[0]].metadata['date'], '%Y-%m-%d'), reverse=True)

posts_metadata = [POSTS[post[0]].metadata for post in POSTS_SORTED]

# Render blog listing
blog_html = blog_template.render(posts=posts_metadata)
blog_index_path = 'build/blog/index.html'

# Build static blog page
os.makedirs(os.path.dirname(blog_index_path), exist_ok=True)
with open(blog_index_path, 'w') as file:
  file.write(blog_html)

# Prepare post data
for post in POSTS_SORTED:
  post_metadata = POSTS[post[0]].metadata

  post_data = {
    'content': POSTS[post[0]],
    'title': post_metadata['title'],
    'date': post_metadata['date'],
  }

  # Render post page
  post_html = post_template.render(post=post_data)

  post_file_path = 'build/{path}/index.html'.format(path=post_metadata['path'])

  # Build post page
  os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
  with open(post_file_path, 'w') as file:
    file.write(post_html)