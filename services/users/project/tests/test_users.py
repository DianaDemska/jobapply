class TestUserService:
    """ Tests for Users Service."""

    def test_users(self, client):
        """Ensure the /ping route behaves correctly."""
        response = client.get('/users/ping')
        assert response.status_code == 200
        assert response.json['message'] == 'pong!'
        assert response.json['status'] == 'success'
