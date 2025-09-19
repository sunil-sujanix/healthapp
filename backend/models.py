from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



db=SQLAlchemy()




class User(db.Model):
    
    
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(255),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)
    

class Dependent(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"))
    name=db.Column(db.String(255),nullable=False)
    relationship=db.Column(db.String,default="self")
    
    
class Record(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'))
    dependent_id=db.Column(db.Integer,db.ForeignKey('dependent.id',ondelete='CASCADE'))
    kind=db.Column(db.String(255),nullable=False)
    systolic=db.Column(db.Integer)
    diastolic=db.Column(db.Integer)
    sugar_mg_dl=db.Column(db.Numeric)
    taken_at=db.Column(db.DateTime,default=datetime.utcnow)
    
    
    
    
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    dependent_id = db.Column(db.Integer, db.ForeignKey('dependent.id', ondelete='CASCADE'))
    record_id = db.Column(db.Integer, db.ForeignKey('record.id', ondelete='SET NULL'))
    filename = db.Column(db.String(255), nullable=False)
    object_key = db.Column(db.String(255), nullable=False)   # stored file path
    content_type = db.Column(db.String(100))
    size_bytes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
    