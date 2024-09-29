from flask.cli import FlaskGroup
import pytest
from project import create_app, db
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    db.session.add(User(username='michael', email="hermanmu@gmail.com"))
    db.session.add(User(username='michaelherman', email="michael@mherman.org"))
    db.session.commit()


@cli.command()
def test():
    result = pytest.main(['-v', 'project/tests'])
    return result


if __name__ == '__main__':
    cli()
