from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

blog_posts = [
    {'id': 1, 'author': 'John Doe', 'title': 'First Post',
     'content': 'This is my first post.'},
    {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post',
     'content': 'This is another post.'},
    # More blog posts can go here...
]

@app.route('/')
def hello_world():
    ##  return 'Hello, World!'
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page
    pass


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
    # Update the post in the JSON file
    # Redirect back to index
        pass

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5001/')
    app.run(host="0.0.0.0", port=5001, debug=True)
