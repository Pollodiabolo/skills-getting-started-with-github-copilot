from urllib.parse import quote


def test_get_activities(client):
    # Arrange

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data, dict)


def test_signup_success_and_duplicate(client):
    # Arrange
    activity = "Chess Club"
    encoded = quote(activity, safe="")
    email = "newstudent@mergington.edu"

    # Act - success signup
    resp1 = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert success
    assert resp1.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Act - duplicate signup
    resp2 = client.post(f"/activities/{encoded}/signup", params={"email": email})

    # Assert duplicate fails
    assert resp2.status_code == 400


def test_remove_participant_success_and_not_found(client):
    # Arrange
    activity = "Chess Club"
    encoded = quote(activity, safe="")
    existing = "michael@mergington.edu"
    missing = "ghost@mergington.edu"

    # Act - remove existing
    resp1 = client.delete(f"/activities/{encoded}/participants", params={"email": existing})

    # Assert removed
    assert resp1.status_code == 200
    assert existing not in client.get("/activities").json()[activity]["participants"]

    # Act - remove missing
    resp2 = client.delete(f"/activities/{encoded}/participants", params={"email": missing})

    # Assert not found
    assert resp2.status_code == 404
