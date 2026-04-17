def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_structure_and_count(client):
    response = client.get("/activities")
    payload = response.json()

    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert len(payload) == 9

    for activity_name, activity in payload.items():
        assert isinstance(activity_name, str)
        assert set(activity.keys()) == {
            "description",
            "schedule",
            "max_participants",
            "participants",
        }
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
