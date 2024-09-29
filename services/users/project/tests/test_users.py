from ..api.models import User
from project import db


class TestUserService:
    """ Tests for Users Service."""

    user_object = User(username='Kenshi', email='email@email.com')
    user_dict = {
        'username': 'Kenshi', 'email': 'email@email.com'
    }

    def add_user(self, username='Kenshi', email='email@email.com'):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    def test_users(self, client):
        """Ensure the /ping route behaves correctly."""
        response = client.get('/users/ping')
        assert response.status_code == 200
        assert response.json['message'] == 'pong!'
        assert response.json['status'] == 'success'

    def test_add_user(self, client):
        """Test if user can be added to database"""
        response = client.post('/users/', data=self.user_dict)
        assert response.status_code == 201
        assert response.json['message'] == 'Kenshi was added.'
        assert response.json['status'] == 'success'

    def test_add_user_invalid_payload(self, client):
        """Test adding user without sending any payload"""
        response = client.post('/users/')
        assert response.status_code == 400
        assert response.json['message'] == 'Invalid payload.'
        assert response.json['status'] == 'fail'

    def test_add_user_missing_key(self, client):
        """Test adding user with missing variable"""
        response = client.post('/users/', data={'email': "hello@h.com"})
        assert response.status_code == 400
        assert response.json['message'] == 'Invalid payload.'
        assert response.json['status'] == 'fail'

    def test_add_user_duplicate_email(self, client):
        """Test adding user with the duplicate email"""
        response = client.post('/users/', data=self.user_dict)
        response = client.post('/users/', data={
            'username': 'Ken', 'email': 'email@email.com'
        })
        assert response.status_code == 400
        assert response.json['message'] == 'Email already exist.'
        assert response.json['status'] == 'fail'

    def test_add_user_duplicate_user(self, client):
        """Test adding user that already exist"""
        response = client.post('/users/', data=self.user_dict)
        response = client.post('/users/', data=self.user_dict)
        assert response.status_code == 400
        assert response.json['message'] == 'Email already exist.'
        assert response.json['status'] == 'fail'

    def test_get_user(self, client):
        """Test getting user behaves correctly"""
        # client.post('/users/', data=self.user_dict)
        user = self.add_user()
        response = client.get(f'/users/{user.id}')
        assert response.status_code == 200
        assert response.json['data']['user']['username'] == user.username
        assert response.json['data']['user']['email'] == user.email
        assert response.json['status'] == 'success'

    def test_user_get_not_found(self, client):
        response = client.get('/users/9999')
        assert response.status_code == 404
        assert response.json['message'] == 'User was not found.'
        assert response.json['status'] == 'fail'

    def test_get_all_users(self, client):
        self.add_user()
        self.add_user('Ent', 'ent@g.com')
        self.add_user('Ara', 'ara@g.cc')

        response = client.get('/users/')
        assert response.status_code == 200
        assert len(response.json['data']['users']) == 3
        assert response.json['data']['users'][0]['username'] == 'Kenshi'
        assert response.json['data']['users'][0]['email'] == 'email@email.com'
        assert response.json['data']['users'][2]['username'] == 'Ara'
        assert response.json['data']['users'][2]['email'] == 'ara@g.cc'
        assert response.json['status'] == 'success'
