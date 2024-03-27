from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import re
from flask_app.models import post

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    db = 'bright_ideas_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.amount = None
    
    
    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users WHERE email = %(email)s
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    # @classmethod
    # def get_all_with_creator(cls):
    #     query = """
    #             SELECT * FROM users JOIN posts ON posts.user_id = users.id ORDER BY posts.id DESC;
    #             """
    #     results = connectToMySQL(cls.db).query_db(query)
    #     if len(results) == 0:
    #         return False
    #     print(results)
    #     all_posts = []
    #     if results:
    #         for row in results:
    #             posts = cls(row)
    #             data = {
    #                 'id': row['posts.id'],
    #                 'content': row['content'],
    #                 'likes': row['likes'],
    #                 'created_at': row['posts.created_at'],
    #                 'updated_at': row['posts.updated_at'],
    #                 'user_id': row['user_id']
    #             }
    #             posts.creator = post.Post(data)
    #             all_posts.append(posts)
                
    #     return all_posts
    
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password) Values (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                """
        return connectToMySQL(cls.db).query_db(query, data)
        
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM users WHERE id = %(id)s
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'register')
            is_valid = False
        if len(user['password']) < 5:
            flash("Passowrd must be atleast 5 characters", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'register')
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash('Password should have at least one uppercase letter', 'register')
            is_valid = False
        if not any(char.isdigit() for char in user['password']):
            flash('Password should have at least one numeral', 'register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('password do not match!', 'register')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_email(user):
        is_valid = True # we assume this is true
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'login')
            is_valid = False
        return is_valid
    
    # @classmethod
    # def get_all_with_likes(cls, data):
    #     query = """
    #             SELECT users.id, count(posts.id) FROM users
    #             JOIN posts ON users.id = posts.user_id
    #             where users.id = %(users.id)s
    #             """
            
    #     result = connectToMySQL(cls.db).query_db(query, data)
    #     print(result)
    #     if result:
    #         posts = cls(result[0])
    #         for row in result:
    #             data = {
    #                 'id': row['users.id'],
    #                 'first_name': row['first_name'],
    #                 'last_name': row['last_name'],
    #                 'email': row['email'],
    #                 'password': row['password'],
    #                 'created_at': row['users.created_at'],
    #                 'updated_at': row['users.updated_at']
    #             }
    #             posts.amount.append(post.Post(data))
    #     return posts