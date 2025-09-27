from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Hardware(db.Model):
    __tablename__ = 'Hardware'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    source = db.Column(db.Text)
    impact = db.Column(db.Integer)

hardware = [
    { "name": "Keyboard", "price": 19.98, "description": "RGB Mechanical Keyboard for computers using the QWERTY layout", "source": "keyboard.jpeg", "impact": 1200*6 },
    { "name": "Monitor", "price": 139.99, "description": "External 27-inch HD 1080P LED curved monitor", "source": "monitor.jpeg", "impact": 2300*6 },
    { "name": "Mouse", "price": 12.74, "description": "Tekcnet (Yes, Tekcnet.) Wireless mouse with Bluetooth and USB connectivity", "source": "mouse.jpeg", "impact": 85*6 },
    { "name": "Headset", "price": 29.99, "description": "RGB Wired Gaming Headset with 3.5mm jack and USB connectivity", "source": "Headset.jpeg", "impact": 450*6 },
]

with app.app_context():
    db.drop_all()
    db.create_all()

    for hard in hardware:
        newHard = Hardware(name=hard["name"], price=hard["price"], description=hard["description"], source=hard["source"], impact=hard["impact"])
        db.session.add(newHard)
    
    db.session.commit()
