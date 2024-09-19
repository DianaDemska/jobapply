import os
import pytest
from flask import current_app
from project import create_app


class TestDevelopmentConfig:
    @pytest.fixture
    def dev_app(self):
        app = create_app()
        app.config.from_object('project.config.DevelopmentConfig')
        yield app

    def test_app_is_development(self, dev_app):
        assert dev_app.config['SECRET_KEY'] == 'my_precious'
        assert current_app is not None
        assert dev_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
            'DATABASE_URL')


class TestTestingConfig:
    @pytest.fixture
    def test_app(self):
        app = create_app()
        app.config.from_object('project.config.TestingConfig')
        yield app

    def test_app_is_testing(self, test_app):
        assert test_app.config['SECRET_KEY'] == 'my_precious'
        assert test_app.config['TESTING']
        assert not test_app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
        assert test_app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
            'DATABASE_TEST_URL')


class TestProductionConfig:
    @pytest.fixture
    def prod_app(self):
        app = create_app()
        app.config.from_object('project.config.ProductionConfig')
        yield app

    def test_app_is_production(self, prod_app):
        assert prod_app.config['SECRET_KEY'] == 'my_precious'
        assert not prod_app.config['TESTING']
