from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app import app       
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


#C
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        user_id = connectToMySQL('user_db').query_db(query,data)
        return user_id

#R
    @classmethod
    def get_by_email(cls,email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data ={
            "email":email,
        }
        result = connectToMySQL('user_db').query_db(query,data)
        return result
#U

#D



    @staticmethod
    def validate_inputs(user):
        is_valid = True
        if len(user['first_name']) == 0 or user['first_name'].isdigit():
            flash('First name must contain at least two letters and no numbers')
            is_valid = False
        if len(user['last_name']) == 0 or user['last_name'].isdigit():
            flash('Last name must contain at least two letters and no numbers')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address!')
            is_valid = False
        if user['password'] != request.form['confirm_pw']:
            flash('Passwords must match')
            is_valid = False
        if len(user['password']) < 8:
            flash('Passwords must be atleast 8 characters long')
            is_valid = False
        return is_valid