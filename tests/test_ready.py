
def test_ready_endpoint(client):
    """Test the root endpoint '/'"""
    response = client.get('/')
    assert response.status_code == 200

   