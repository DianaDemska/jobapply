import pytest
from project import create_app
from project.api.models import db


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('project.config.TestingConfig')

    db.create_all()
    db.session.commit()
    yield app
    db.session.remove()
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
