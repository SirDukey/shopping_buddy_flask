import pytest

from app import create_app, db


@pytest.fixture()
def app():
    # This will create an in-memory database for use with tests
    app = create_app("sqlite://")

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
