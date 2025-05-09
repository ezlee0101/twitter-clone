#!/usr/bin/env python
import click
from flask.cli import FlaskGroup

from project import create_app, db
from project.models import User, Tweet, Url

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command("create_db")
def create_db():
    """Drop all tables and recreate them."""
    db.drop_all()
    db.create_all()
    click.echo("Database tables created.")

@cli.command("seed_db")
@click.option('--users', default=10, help='Number of users to seed.')
@click.option('--tweets', default=20, help='Number of tweets to seed.')
def seed_db(users, tweets):
    """Seed the database with USERS and TWEETS."""
    # Seed users
    for i in range(users):
        db.session.add(User(username=f'user_{i}', password='pass'))
    db.session.commit()

    # Collect user IDs
    user_ids = [u.id for u in User.query.all()]

    # Seed tweets
    for i in range(tweets):
        uid = user_ids[i % len(user_ids)]
        db.session.add(Tweet(user_id=uid, content=f'Tweet #{i}'))
    db.session.commit()

    click.echo(f"Seeded {users} users and {tweets} tweets.")

if __name__ == '__main__':
    cli()
