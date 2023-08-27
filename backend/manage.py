from flask.cli import FlaskGroup
from project import app
from project.extensions import db
from project.nn.sd14 import SD14Api


cli = FlaskGroup(app)


@cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('preload')
def preload_dependencies():
    SD14Api.load_api()
    db.session.add(SD14Api.build_model())
    db.session.commit()


if __name__ == "__main__":
    cli()
