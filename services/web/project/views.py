from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Tweet, User
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    page     = int(request.args.get('page', 1))
    per_page = 20
    offset   = (page - 1) * per_page

    rows = (
        db.session
          .query(Tweet, User.username)
          .join(User, Tweet.user_id == User.id)
          .order_by(Tweet.created_at.desc())
          .limit(per_page)
          .offset(offset)
          .all()
    )

    tweets = [
      {'id': t.id, 'username': u, 'content': t.content, 'created_at': t.created_at}
      for t, u in rows
    ]

    next_page = page + 1 if len(tweets) == per_page else None
    prev_page = page - 1 if page > 1 else None

    return render_template('home.html',
                           tweets=tweets,
                           prev_page=prev_page,
                           next_page=next_page)

@main_bp.route('/create_message', methods=['GET', 'POST'])
def create_message():
    # Redirect anonymous users to login
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        content = request.form['content']
        # Insert new tweet
        new_tweet = Tweet(
            user_id=session['user_id'],
            content=content
        )
        db.session.add(new_tweet)
        db.session.commit()
        # After posting, go back to the home feed
        return redirect(url_for('main.home'))

    # GET: show the form
    return render_template('create_message.html')

