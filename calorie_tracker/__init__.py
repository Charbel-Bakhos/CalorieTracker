from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy

(
    db_user, 
    db_pass, 
    db_name, 
    db_domain
) = (os.environ.get(item) for item in [
    "DB_USER", 
    "DB_PASS", 
    "DB_NAME", 
    "DB_DOMAIN"
    ]
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_domain}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class Foods(db.Model):
    __tablename__ = 'foods'
    food_id = db.Column(db.Integer, primary_key = True)
    food_name = db.Column(db.String(80), unique = True, nullable = False)

    def __init__(self, food_name):
        self.food_name = food_name
    
    @property
    def serialize(self):
        return {
            'food_id': self.food_id,
            'food_name': self.food_name
        }

db.create_all()

@app.route('/')
def hello_world():
    return "Hello, world! Check this out!"

@app.route('/foods/', methods = ['GET'])
def get_foods():
    foods = Foods.query.all()
    return jsonify([food.serialize for food in foods])

@app.route('/foods/', methods = ['POST'])
def create_food():
    new_food = Foods(request.json['food_name'])
    db.session.add(new_food)
    db.session.commit()
    return jsonify(new_food.serialize)

@app.route("/foods/<int:id>/", methods = ["GET"])
def get_food(id):
    food = Foods.query.get_or_404(id)
    return jsonify(food.serialize)

@app.route("/foods/<int:id>/", methods=["PUT", "PATCH"])
def update_food(id):
    food = Foods.query.filter_by(food_id = id)
    food.update(dict(food_name = request.json['food_name']))
    db.session.commit()
    return jsonify(food.first().serialize)

@app.route("/foods/<int:id>/", methods = ["DELETE"])
def delete_food(id):
    food = Foods.query.get_or_404(id)
    db.session.delete(food)
    db.session.commit()
    return jsonify(food.serialize)

if __name__ == '__main__':
    app.run(debug=True)

