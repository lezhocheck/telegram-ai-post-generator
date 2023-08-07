from flask.cli import FlaskGroup
from project import app
from project.extensions import db
from project.models import Model


cli = FlaskGroup(app)


@cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    model = Model(title='Some model 1', description='Some long description', is_available=True)
    db.session.add(model)
    db.session.commit()


if __name__ == "__main__":
    cli()
