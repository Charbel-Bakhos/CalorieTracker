from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, world! Check this out!"

@app.route('/tracker/')
def get_tracker():
    return "This will be a list of all foods eaten on the day"

@app.route('/tracker/<food_id>/')
def get_specific_food(food_id):
    return f"This is info on a {food_id}"


if __name__ == '__main__':
    app.run(debug=True)