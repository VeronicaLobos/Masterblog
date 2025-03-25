"""
A Flask web blog.


"""

from flask import Flask, render_template, request
import webbrowser
import datetime
import os
from storage.handle_json import HandleJson

app = Flask(__name__)


@app.route('/')
def blog():
    """
    Renders the index.html template with the blog posts.

    Loads the blog posts from the JSON file and passes
    them to the template.
    """
    return render_template('index.html',
                           posts=database.load_posts_from_json())


@app.route('/like/<int:post_id>')
def like_post(post_id):
    """
    Adds a like to a blog post.

    Receives the id from the post to be liked.
    Loads the data from the database (a list of dicts),
    and a count of the posts stored.

    If there are no post in the list, returns a render
    of the 'error_message.html' template.

    Iterates through the list until it finds a dictionary
    with attribute 'id' equal to the 'post_id' parameter,
    add adds 1 to the value of it's attribute 'likes'.

    Updates the database with the list and refreshes the page
    by returning a render of the 'index.html' template.
    """
    blog_posts = database.load_posts_from_json()
    for post in blog_posts:
        if post.get('id') == post_id:
            post['likes'] += 1
            break

    database.save_posts_to_json(blog_posts)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """
    Adds a new blog post to the list of blog posts.

    If the request method is 'GET', it returns a render of the
    'add.html' template, which contains a form for creating a
    new blog post.

    If the request method is 'POST', it retrieves the author,
    title, and content from the form data, creates a new post
    dictionary with a unique ID*, appends it to the 'blog_posts'
    list, and displays a success message by returning a render
    of the 'success_message.html' template.

    But if the post was not added, returns a failure message by
    returning a render of the 'error_message.html' template.

    * Unique ID is the highest (or latest) ID in the database plus
    1: In this way, IDs previously deleted will not be assigned to
    new posts, preserving the order of publication.
    """
    blog_posts = database.load_posts_from_json()

    if request.method == 'POST':
        ids = [post['id'] for post in blog_posts if 'id' in post]

        try:
            date = datetime.datetime.now().strftime('%a %b %d, %Y at %H:%M')
            new_post = {
                'id': max(ids) + 1 if ids else 1,
                'author': request.form['author'],
                'title': request.form['title'],
                'content': request.form['content'],
                'date_published': date,
                'date_updated': date,
                'status': 'Published',
                'likes': 0
            }
            blog_posts.append(new_post)

            database.save_posts_to_json(blog_posts)
            return render_template('success_message.html', status='added')

        except TypeError as e:
            return render_template('error_message.html', code=404, message=e)

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    """
    Deletes a blog post from the list of blog posts.

    Receives the id from the post to be deleted.
    Loads the data from the database (a list of dicts),
    and a count of the posts stored.

    If there are no post in the list, returns a render
    of the 'error_message.html' template.

    Makes a new list excluding the post with the specified
    id, and makes a new posts count.

    Updates the database with the new list.

    Checks if there is one less post in the database and
    returns the corresponding render.
    """
    blog_posts = database.load_posts_from_json()
    post_count_before = len(blog_posts)

    if post_count_before < 1:
        return render_template('error_message.html', code=404, message='No posts to delete.')

    blog_posts = [post for post in blog_posts if post.get('id') != post_id]
    database.save_posts_to_json(blog_posts)

    blog_posts = database.load_posts_from_json()
    post_count_after = len(blog_posts)
    if post_count_after < post_count_before:
        return render_template('success_message.html', status='deleted')
    else:
        return render_template('error_message.html', code=404, message='Post not found or could not be deleted.')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    """
    Updates the author, title and/or content of a post.

    Receives the id from the post to be updated.
    Loads the data from the database (a list of dicts),
    and a count of the posts stored.

    If there are no post in the list, returns a render
    of the 'error_message.html' template.

    If the request method is 'GET', it returns a render
    of the 'update.html' template.

    If the request method is 'POST', it iterates through
    the list until it finds a dictionary with attribute
    'id' equal to the 'post_id' parameter, and updates
    it with the data from the form, captures the date
    from when the form is submitted and changes the
    status to 'Updated'.

    Updates the database with the list and refreshes the
    page by returning a render of the 'success_message.html'
    """
    blog_posts = database.load_posts_from_json()
    post_list = [post for post in blog_posts if post.get('id') == int(post_id)]
    post = post_list[0]

    if not post_list:
        return render_template('error_message.html', code=404, message='No posts to delete.')

    if request.method == 'POST':
        for post in blog_posts:
            date = datetime.datetime.now().strftime('%a %b %d, %Y at %H:%M')
            if post.get('id') == int(post_id):
                post['author'] = request.form['author']
                post['title'] = request.form['title']
                post['content'] = request.form['content']
                post['date'] = date
                post['status'] = "Updated"
                break

        database.save_posts_to_json(blog_posts)

        return render_template('success_message.html', status='updated')
    else:
        return render_template('update.html', post=post)


if __name__ == '__main__':
    """
    Instantiates a database object from the class Handle_Json
    with the specified file path.
    
    Runs the Flask app and opens a new browser app.
    """
    file_path = os.path.join('./data', 'blog_posts.json')
    database = HandleJson(file_path)

    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(host="0.0.0.0", port=5000, debug=True)
