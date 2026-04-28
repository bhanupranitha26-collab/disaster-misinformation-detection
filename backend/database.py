import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("misinfo.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyzed_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        credibility_score INTEGER,
        status TEXT,
        response_action TEXT,
        location TEXT,
        panic_index INTEGER,
        reviewed_by TEXT,
        reviewed_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_post(text, score, status, action, location, panic_index):
    conn = sqlite3.connect("misinfo.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyzed_posts
        (text, credibility_score, status, response_action,
         location, panic_index)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (text, score, status, action, location, panic_index))

    conn.commit()
    conn.close()


def get_recent_posts():
    conn = sqlite3.connect("misinfo.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, text, credibility_score, status,
               response_action, location, panic_index,
               reviewed_by, reviewed_at
        FROM analyzed_posts
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    posts = []
    for row in rows:
        posts.append({
            "id": row[0],
            "text": row[1],
            "credibility_score": row[2],
            "status": row[3],
            "response_action": row[4],
            "location": row[5],
            "panic_index": row[6],
            "reviewed_by": row[7],
            "reviewed_at": row[8]
        })

    return posts


def review_post(post_id, reviewer, new_status, new_action):
    conn = sqlite3.connect("misinfo.db")
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE analyzed_posts
        SET status = ?, response_action = ?,
            reviewed_by = ?, reviewed_at = ?
        WHERE id = ?
    """, (new_status, new_action, reviewer, timestamp, post_id))

    conn.commit()
    conn.close()