CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE tweets (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE urls (
  id SERIAL PRIMARY KEY,
  tweet_id INTEGER NOT NULL REFERENCES tweets(id),
  url TEXT NOT NULL,
  expanded_url TEXT NOT NULL
);

-- Indexes for fast feed
CREATE INDEX ON tweets (created_at DESC);
CREATE INDEX ON tweets (user_id);

-- FTS: RUM index example (requires pg_trgm and rum extensions)
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS rum;
CREATE INDEX tweets_content_rum_idx ON tweets USING rum (to_tsvector('english', content));
