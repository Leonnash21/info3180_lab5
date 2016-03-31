from . import db  
from werkzeug import generate_password_hash, check_password_hash


class Myprofile(db.Model):     
    id = db.Column(db.Integer, primary_key=True)     
    first_name = db.Column(db.String(80))     
    last_name = db.Column(db.String(80)) 
    nickname = db.Column(db.String(80), unique=True)    
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(54)) 
    image= db.Column(db.LargeBinary)

    query = db.Query("Myprofile")
    
    
    
    
    def __init__(self, id, first_name, last_name, nickname, email, password, image):
        self.id = id
        self.first_name=first_name.title()
        self.last_name=last_name.title()
        self.nickname=nickname
        self.email=email.lower()
        self.password = password
        self.image=image
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.nickname)