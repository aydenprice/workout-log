SAMPLE_WORKOUT = {
    "exercise": "Bench Press",
    "sets": 3,
    "reps": 8,
    "weight": 135.0,
    "date": "2026-11-24",
}


def test_create_workout(client):
    response = client.post("/workouts", json=SAMPLE_WORKOUT)
    data = response.json()

    assert response.status_code == 201
    assert data["id"] == 1
    assert data["exercise"] == "Bench Press"
    assert data["sets"] == 3
    assert data["reps"] == 8
    assert data["weight"] == 135.0
    assert data["date"] == "2026-11-24"


def test_read_all_workouts(client):
    client.post("/workouts", json=SAMPLE_WORKOUT)
    client.post(
        "/workouts", json={**SAMPLE_WORKOUT, "exercise": "Squat", "weight": 185.0}
    )

    response = client.get("/workouts")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["exercise"] == "Bench Press"
    assert data[1]["exercise"] == "Squat"
    assert data[1]["weight"] == 185.0


def test_read_one_workout(client):
    created = client.post("/workouts", json=SAMPLE_WORKOUT).json()

    response = client.get(f"/workouts/{created['id']}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == created["id"]
    assert data["exercise"] == "Bench Press"
    assert data["sets"] == 3
    assert data["reps"] == 8
    assert data["weight"] == 135.0
    assert data["date"] == "2026-11-24"


def test_update_workout(client):
    created = client.post("/workouts", json=SAMPLE_WORKOUT).json()

    response = client.put(
        f"/workouts/{created['id']}", json={**SAMPLE_WORKOUT, "weight": 145.0}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == created["id"]
    assert data["weight"] == 145.0
    assert data["exercise"] == "Bench Press"

    # Confirm the change was actually saved
    saved = client.get(f"/workouts/{created['id']}").json()
    assert saved["weight"] == 145.0


def test_delete_workout(client):
    created = client.post("/workouts", json=SAMPLE_WORKOUT).json()

    response = client.delete(f"/workouts/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/workouts/{created['id']}").status_code == 404
    assert client.get("/workouts").json() == []

