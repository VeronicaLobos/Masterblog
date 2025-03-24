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
    """
    Renders the index.html template with the blog posts
    """
    ##  return 'Hello, World!'
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])

def add():
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
            'id': len(blog_posts) + 1,
            'author': request.form['author'],
            'title': request.form['title'],
            'content': request.form['content']
        }
        blog_posts.append(new_post)
        return (f"Post added successfully:\n"
                f"{blog_posts[-1]}") ##  temp for testing
        ##  return redirect(url_for('index'))
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
