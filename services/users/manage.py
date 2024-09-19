from flask.cli import FlaskGroup
import pytest
from project import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    result = pytest.main(['-v', 'project/tests'])
    return result


if __name__ == '__main__':
    cli()
