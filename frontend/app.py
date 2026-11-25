import requests
from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

# Address of the FastAPI backend
API_URL = "http://127.0.0.1:8000"


def get_form_data():
    return {
        "exercise": request.form["exercise"],
        "sets": int(request.form["sets"]),
        "reps": int(request.form["reps"]),
        "weight": float(request.form["weight"]),
        "date": request.form["date"],
    }


@app.route("/")
def index():
    response = requests.get(f"{API_URL}/workouts")
    workouts = response.json()
    return render_template("workouts.html", workouts=workouts)


@app.route("/workouts/new", methods=["GET", "POST"])
def create_workout():
    if request.method == "POST":
        response = requests.post(f"{API_URL}/workouts", json=get_form_data())
        if response.status_code == 201:
            return redirect(url_for("index"))
        return render_template(
            "workout_form.html",
            heading="Add Workout",
            error="Could not save the workout. Check your values.",
        )
    return render_template("workout_form.html", heading="Add Workout")


@app.route("/workouts/<int:workout_id>")
def workout_detail(workout_id):
    response = requests.get(f"{API_URL}/workouts/{workout_id}")
    if response.status_code == 404:
        abort(404)
    workout = response.json()
    return render_template("workout_detail.html", workout=workout)


@app.route("/workouts/<int:workout_id>/edit", methods=["GET", "POST"])
def edit_workout(workout_id):
    if request.method == "POST":
        data = get_form_data()
        response = requests.put(f"{API_URL}/workouts/{workout_id}", json=data)
        if response.status_code == 404:
            abort(404)
        if response.status_code == 200:
            return redirect(url_for("index"))
        return render_template(
            "workout_form.html",
            heading="Edit Workout",
            workout=data,
            error="Could not save the workout. Check your values.",
        )

    response = requests.get(f"{API_URL}/workouts/{workout_id}")
    if response.status_code == 404:
        abort(404)
    return render_template(
        "workout_form.html", heading="Edit Workout", workout=response.json()
    )

@app.route("/workouts/<int:workout_id>/delete", methods=["POST"])
def delete_workout(workout_id):
    response = requests.delete(f"{API_URL}/workouts/{workout_id}")
    if response.status_code == 404:
        abort(404)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)