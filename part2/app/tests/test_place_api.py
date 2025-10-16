import json

def test_get_place_by_id(place):
    # Suppose we have a place with ID "1234"
    response = client.get("/api/places/1234")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "id" in data
    assert "title" in data
    assert "description" in data
    assert "price" in data
    assert "latitude" in data
    assert "longitude" in data
    assert "created_at" in data
    assert "updated_at" in data
    assert "owner" in data
    assert isinstance(data["amenities"], list)
