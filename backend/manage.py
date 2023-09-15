from flask.cli import FlaskGroup
from project.extensions import db
from project.api.sd14 import SD14Api
from project import create_app


cli = FlaskGroup(create_app=create_app)


@cli.command('create_db')
def create_db() -> None:
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('preload')
def preload_dependencies() -> None:
    db.session.add(SD14Api.preload())
    db.session.commit()
    

if __name__ == '__main__':
    cli()

