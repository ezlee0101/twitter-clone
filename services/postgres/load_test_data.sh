#!/usr/bin/env bash
set -euo pipefail

USERS=${1:-100}
TWEETS=${2:-200}
URLS=${3:-200}

PSQL="psql -U $POSTGRES_USER -d $POSTGRES_DB -t -A -c"

# seed users
$PSQL "INSERT INTO users(username, password, created_at)
          SELECT 'user_'||g, md5(random()::text), NOW()
          FROM generate_series(1, $USERS) AS g;"
\# seed urls
$PSQL "INSERT INTO urls(tweet_id, url, expanded_url)
          SELECT (g-1)%$TWEETS+1,
                 'http://example.com/'||g,
                 'http://example.com/'||g||'/expanded'
          FROM generate_series(1, $URLS) AS g;"
\# seed tweets
$PSQL "INSERT INTO tweets(user_id, content, created_at)
          SELECT (random()*$USERS)::int+1,
                 'Tweet '||g,
                 NOW()
          FROM generate_series(1, $TWEETS) AS g;"
