from flask.cli import FlaskGroup
from project import create_app
from project.extensions import db
from project.api.sd14 import SD14Api


cli = FlaskGroup(create_app=create_app)


@cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('preload')
def preload_dependencies():
    db.session.add(SD14Api.preload())
    db.session.commit()


if __name__ == '__main__':
    cli()
