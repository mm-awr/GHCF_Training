from urllib.parse import quote


def test_unregister_success_removes_participant_and_returns_message(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}",
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_student_not_signed_up(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "not.enrolled@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_second_attempt_returns_404(client):
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    encoded_activity = quote(activity_name)

    first_response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )
    second_response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_after_signup_flow(client):
    activity_name = "Debate Team"
    email = "flow.student@mergington.edu"
    encoded_activity = quote(activity_name)

    signup_response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )
    unregister_response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )

    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants
