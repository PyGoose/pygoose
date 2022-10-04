from flask import Flask

app = Flask(__name__)

def get_file(path):
    file_path = f'dist/{path}'
    return open(file_path,'r').read()
    
@app.route('/')
def goose_index():
    return get_file('index.html')
    
@app.route('/pages/<page>')
def goose_pages(page):
    return get_file(f'pages/{page}')
    
@app.route('/posts/<post>')
def goose_posts(post):
    return get_file(f'posts/{post}')
    
@app.errorhandler(404)
def error_page(error):
    return get_file(f'404.html')
    
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000)