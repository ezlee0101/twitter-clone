from flask import Blueprint, render_template, request, session
from sqlalchemy import text
from . import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    page = int(request.args.get('page', 1))
    per_page = 20
    offset = (page - 1) * per_page

    tweets = []
    total = 0

    if q:
        # Use plainto_tsquery for simplicity; you can also use websearch_to_tsquery
        ts_query = db.session.execute(
            text("SELECT plainto_tsquery('english', :q) AS query"),
            {'q': q}
        ).scalar_one()

        # Count total matches
        total = db.session.execute(
            text("""
              SELECT count(*) FROM tweets
              WHERE to_tsvector('english', content) @@ :query
            """), {'query': ts_query}
        ).scalar()

        # Fetch paginated results with ranking and headline
        rows = db.session.execute(
            text(f"""
              SELECT 
                t.id,
                u.username,
                ts_headline(
                  'english',
                  t.content,
                  :query,
                  'StartSel=<mark>,StopSel=</mark>'
                ) AS snippet,
                ts_rank_cd(
                  to_tsvector('english', t.content),
                  :query
                ) AS rank,
                t.created_at
              FROM tweets t
              JOIN users u ON u.id = t.user_id
              WHERE to_tsvector('english', t.content) @@ :query
              ORDER BY rank DESC
              LIMIT :limit OFFSET :offset
            """),
            {'query': ts_query, 'limit': per_page, 'offset': offset}
        ).all()

        # Build simple dicts for the template
        tweets = [
          {
            'id':    row.id,
            'username': row.username,
            'snippet': row.snippet,
            'created_at': row.created_at
          }
          for row in rows
        ]

    # Pagination links
    next_page = page + 1 if offset + len(tweets) < total else None
    prev_page = page - 1 if page > 1 else None

    return render_template(
        'search.html',
        query=q,
        tweets=tweets,
        prev_page=prev_page,
        next_page=next_page
    )

