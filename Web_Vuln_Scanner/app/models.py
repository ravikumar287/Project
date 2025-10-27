from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    scans = db.relationship('Scan', backref='user', lazy=True)

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_url = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Running, Completed, Failed
    vulnerabilities = db.relationship('Vulnerability', backref='scan', lazy=True)

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    payload = db.Column(db.String(500))
    severity = db.Column(db.String(20), nullable=False)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=False)