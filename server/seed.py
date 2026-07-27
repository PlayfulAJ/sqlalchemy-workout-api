#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    pushups = Exercise(
        name="push ups",
        category="Chest",
        equipment_needed=False
    )

    squats = Exercise(
        name="squats",
        category="Legs",
        equipment_needed=False
    )

    bench_press = Exercise(
        name="sit ups",
        category="Chest",
        equipment_needed=True
    )

    db.session.add_all([pushups, squats, bench_press])
    db.session.commit()

    workout1 = Workout(
        date=date(2026, 7, 27),
        duration_minutes=45,
        notes="upper bidy workout"
    )

    workout2 = Workout(
        date=date(2026, 7, 28),
        duration_minutes=60,
        notes="lower body workout"
    )

    db.session.add_all([workout1, workout2])
    db.session.commit()

    workout_exercise1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushups.id,
        reps=20,
        sets=3
    )

    workout_exercise2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=bench_press.id,
        reps=10,
        sets=4
    )

    workout_exercise3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=squats.id,
        reps=15,
        sets=4
    )

    db.session.add_all([
        workout_exercise1,
        workout_exercise2,
        workout_exercise3
    ])

    db.session.commit()

    print("seed data added successfully!")