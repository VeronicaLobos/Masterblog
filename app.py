from flask import Flask, render_template, request, jsonify
import webbrowser

app = Flask(__name__)

BLOG_POSTS = [
    {'id': 1, 'author': 'John Doe', 'title': 'First Post',
     'content': 'This is my first post.'},
    {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post',
     'content': 'This is another post.'},
    # More blog posts can go here...
]

@app.route('/')
def blog():
    """
    Renders the index.html template with the blog posts
    """
    return render_template('index.html', posts=BLOG_POSTS)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """
    Adds a new blog post to the list of blog posts.

    If the request method is 'GET', it renders the 'add.html'
    template, which contains a form for creating a new blog post.
    If the request method is 'POST', it retrieves the author, title,
    and content from the form data, creates a new post dictionary
    with a unique ID, appends it to the 'blog_posts' list, and
    returns a success message.

    !!!! Should redirect to index in the future.
    """
    if request.method == 'POST':
        new_post = {
            'id': len(BLOG_POSTS) + 1,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        BLOG_POSTS.append(new_post)
        ##  return jsonify({'message': 'Post added successfully'}), 200
        return (f"Post added successfully:\n"
                f"{BLOG_POSTS[-1]}") ##  temp for testing
        ##  return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    global BLOG_POSTS
    BLOG_POSTS[:] = [post for post in BLOG_POSTS if post.get('id') != post_id]
    ##  return jsonify({'message': 'Post deleted successfully'}), 200
    return (f"Post deleted successfully:\n"
            f"{BLOG_POSTS}")  ##  temp for testing
    ##  return redirect(url_for('index'))

"""
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

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)
"""


if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5001/')
    app.run(host="0.0.0.0", port=5001, debug=True)
