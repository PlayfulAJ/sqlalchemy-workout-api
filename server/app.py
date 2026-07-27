from flask import Flask, make_response
from flask_migrate import Migrate

from models import *

app = Flask(__name__)

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()

    workout_list = []

    for workout in workouts:
        workout_list.append({
            "id": workout.id,
            "date": str(workout.date),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        })

    return make_response(workout_list, 200)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/jabar/Moringa/sqlachemy-workout-api/server/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


if __name__ == '__main__':
    app.run(port=5555, debug=True)