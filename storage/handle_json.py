"""
A simple module for reading and writing in a JSON database.
"""

import json
import os

class HandleJson():
    def __init__(self, file_path):
        self.file_path = file_path


    def load_posts_from_json(self):
        """
        Loads the posts from the database.

        If the file with the designated path doesn't exist,
        it creates one with example data (a list of dicts).

        Loads the data stored in the database and returns it.

        Handles errors like FileNotFoundError and JSONDecodeError
        by returning an empty list.
        """
        example_blog_posts = [
            {'id': 1, 'author': 'John Titor', 'title': 'First Post',
             'content': 'This is my first post.',
             'date_published': 'Jul 29, 1998 at 00:01',
             'date_updated': '00:00', 'status': 'Published',
             'likes': 42}
        ]

        try:
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w', encoding='utf-8') as handle:
                    json.dump(example_blog_posts, handle, indent=4)

            with open(self.file_path, 'r', encoding='utf-8') as handle:
                return json.load(handle)

        except FileNotFoundError as e:
            print(e)
        except json.JSONDecodeError as e:
            print(e)
        return []


    def save_posts_to_json(self, updated_posts):
        """
        Receives a list of dictionaries and saves it to the database.
        """
        with open(self.file_path, 'w', encoding='utf-8') as handle:
            json.dump(updated_posts, handle, indent=4)