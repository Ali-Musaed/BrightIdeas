from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
from flask_app.models import user
import datetime


class Post:
    db = 'bright_ideas_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.likes = data['likes']
        self.liked_by = []
        self.creator = None
    @classmethod
    def add_likes(cls, data):
        query = "INSERT INTO likes (post_id, user_id) VALUES(%(post_id)s, %(user_id)s)"
        
        return connectToMySQL(cls.db).query_db(query, data)
    @classmethod
    def add_one(cls, data):
        query = f"UPDATE posts SET likes = likes + 1 WHERE posts.id = %(post_id)s"
        # query = f'SELECT count(likes.post_id) FROM users JOIN likes ON users.id = likes.user_id WHERE likes.post_id = %(post_id)s'
        result = connectToMySQL(cls.db).query_db(query, data)
        
        return result
    
    
    @classmethod
    def likes_db(cls, data):
        query = f"SELECT likes.user_id FROM posts left JOIN likes ON posts.id = likes.post_id WHERE posts.id= %(post_id)s;"
        result= connectToMySQL(cls.db).query_db(query, data)
        for i in result:
            print(i['user_id'])
        return result[0]['user_id']
        # return result[0]['user_id']
    @classmethod
    def get_amount_of_likes(cls,data):
        query = """
                select posts.id, count(posts.id) from posts Join likes ON likes.post_id = posts.id where posts.id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return results
    @classmethod
    def get_post(cls, data):
        query = """
                SELECT * FROM posts WHERE id = %(id)s
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    @classmethod
    def insert(cls, data):
        query = """
                INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s)
                """
        return connectToMySQL(cls.db).query_db(query, data)
    @classmethod
    def get_all_with_posts(cls, data):
        query = """
                SELECT users.id, count(posts.id) FROM posts
                JOIN users ON users.id = posts.user_id
                where user_id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        return result[0]['count(posts.id)']
    @classmethod
    def get_all_with_likes(cls, data):
        query = """
                SELECT users.id, count(likes.user_id) FROM users
                JOIN likes ON users.id = likes.user_id
                where user_id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        if result == 0:
            return 0
        return result[0]['count(likes.user_id)']
    @classmethod
    def delete(cls, data):
        query = """
                DELETE FROM posts where id = %(id)s
                """
        return connectToMySQL(cls.db).query_db(query, data)
    # SELECT * FROM posts Left JOIN users ON posts.user_id = users.id ORDER BY posts.id DESC;
    @classmethod
    def get_all_with_creator(cls):
        query = """
                SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.id DESC;
                """
        results = connectToMySQL(cls.db).query_db(query)
        if len(results) < 1:
            return None
        print(results)
        all_posts = []
        if results:
            for row in results:
                post = cls(row)
                data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                post.creator = user.User(data)
                all_posts.append(post)
                
        return all_posts
    
    @classmethod
    def get_all_with_one(cls, data):
        query = """
                SELECT * FROM posts JOIN likes ON posts.id = likes.post_id  JOIN users ON likes.user_id = users.id WHERE posts.id = %(id)s
                """
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        if result:
            post = cls(result[0])
            for row in result:
                data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                post.liked_by.append(user.User(data))
        return post
    
    @staticmethod
    def validate_content(post):
        is_valid = True # we assume this is tru
        if len(post['content']) == 0:
            flash("content cannot be blank!", 'content')
            is_valid = False
        return is_valid
    