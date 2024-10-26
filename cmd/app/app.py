import os
from flask import Flask, request, g
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DATABASE_URI = os.getenv('DATABASE_URI')

def get_db_connection():
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(DATABASE_URI, cursor_factory=RealDictCursor)
    return g.db_conn

@app.teardown_appcontext
def close_db_connection(exception):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()

@app.route('/counter')
def counter():
    conn = get_db_connection()
    user_agent = request.headers.get('User-Agent', 'unknown user agent')
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO table_Counter (datetime, client_info) VALUES (now(), %s) RETURNING id, client_info, datetime;",
                (user_agent,)
            )
            result = cur.fetchone()
            conn.commit()
            inserted_id = result['id']
            inserted_user_agent = result['client_info']
            inserted_datetime = result['datetime']
            return {
                "id": inserted_id,
                "client_info": inserted_user_agent,
                "datetime": inserted_datetime
            }
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
@app.route('/')
def hello():
    return 'Hello World!\n'

if __name__ == '__main__':
    app.run()