import json
import os

file_name = 'data/blog_posts.json'


def load_posts_from_json():
    """

    """
    blog_posts = [
        {'id': 1, 'author': 'John Doe', 'title': 'First Post',
         'content': 'This is my first post.'},
        {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post',
         'content': 'This is another post.'},
    ]

    try:
        if not os.path.exists(file_name):
            with open(file_name, 'w', encoding='utf-8') as handle:
                json.dump(blog_posts, handle, indent=4)

        with open(file_name, 'r', encoding='utf-8') as handle:
            return json.load(handle)

    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(e)
    return []


def save_posts_to_json(updated_posts):
    """

    """
    with open(file_name, 'w', encoding='utf-8') as handle:
        json.dump(updated_posts, handle, indent=4)