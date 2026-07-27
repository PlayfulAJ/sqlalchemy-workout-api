from flask import Flask, make_response, request
from flask_migrate import Migrate
from datetime import datetime

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

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)

    if workout is None:
        return make_response({"error": "Workout not found"}, 404)

    return make_response({
        "id": workout.id,
        "date": str(workout.date),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes
    }, 200)

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()

    workout = Workout(
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        duration_minutes=data['duration_minutes'],
        notes=data.get('notes')
    )

    db.session.add(workout)
    db.session.commit()

    return make_response({
        "id": workout.id,
        "date": str(workout.date),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes
    }, 201)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)

    if workout is None:
        return make_response({"error": "Workout not found"}, 404)

    db.session.delete(workout)
    db.session.commit()

    return make_response({"message": "Workout deleted successfully"}, 200)

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()

    exercise_list = []

    for exercise in exercises:
        exercise_list.append({
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        })

    return make_response(exercise_list, 200)

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)

    if exercise is None:
        return make_response({"error": "Exercise not found"}, 404)

    return make_response({
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed,
        "workouts": [
            {
                "id": workout_exercise.workout.id,
                "date": str(workout_exercise.workout.date),
                "duration_minutes": workout_exercise.workout.duration_minutes,
                "notes": workout_exercise.workout.notes
            }
            for workout_exercise in exercise.workout_exercises
        ]
    }, 200)

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()

    exercise = Exercise(
        name=data['name'],
        category=data['category'],
        equipment_needed=data['equipment_needed']
    )

    db.session.add(exercise)
    db.session.commit()

    return make_response({
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed
    }, 201)



@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)

    if exercise is None:
        return make_response({"error": "Exercise not found"}, 404)

    db.session.delete(exercise)
    db.session.commit()

    return make_response({"message": "Exercise deleted successfully"}, 200)

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST']
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if workout is None:
        return make_response({"error": "Workout not found"}, 404)

    if exercise is None:
        return make_response({"error": "Exercise not found"}, 404)

    data = request.get_json()

    workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )

    db.session.add(workout_exercise)
    db.session.commit()

    return make_response({
        "id": workout_exercise.id,
        "workout_id": workout_exercise.workout_id,
        "exercise_id": workout_exercise.exercise_id,
        "reps": workout_exercise.reps,
        "sets": workout_exercise.sets,
        "duration_seconds": workout_exercise.duration_seconds
    }, 201)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/jabar/Moringa/sqlachemy-workout-api/server/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


if __name__ == '__main__':
    app.run(port=5555, debug=True)