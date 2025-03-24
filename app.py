from flask import Flask, render_template, request, jsonify, redirect, url_for
import webbrowser
import time
from functools import wraps
import handle_json

app = Flask(__name__)


@app.route('/')
def blog():
    """
    Renders the index.html template with the blog posts
    """
    return render_template('index.html',
                           posts=handle_json.load_posts_from_json())


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
    blog_posts = handle_json.load_posts_from_json()

    if request.method == 'POST':
        ids = [post['id'] for post in blog_posts if 'id' in post]

        try:
            new_post = {
                'id': max(ids) + 1 if ids else 1,
                'author': request.form['author'],
                'title': request.form['title'],
                'content': request.form['content']
            }
            blog_posts.append(new_post)

            handle_json.save_posts_to_json(blog_posts)
            return render_template('success_message.html', status='added')

        except TypeError as e:
            return f"Invalid post data, some posts do not have an ID: {e}"

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    blog_posts_before = handle_json.load_posts_from_json()
    post_count_before = len(blog_posts_before)

    if post_count_before < 1:
        return "There are no posts to delete."

    blog_posts_after = [post for post in blog_posts_before if post.get('id') != post_id]
    post_count_after = len(blog_posts_after)

    handle_json.save_posts_to_json(blog_posts_after)

    if post_count_after < post_count_before:
        # Post was successfully deleted
        return render_template('success_message.html', status='deleted')
    else:
        return jsonify({'error': 'Post not found or could not be deleted.'}), 404



"""
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
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
