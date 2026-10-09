import sqlite3

DB_NAME = "saga.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT NOT NULL,
            effort REAL NOT NULL,
            priority TEXT NOT NULL,
            progress INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def add_task(title, deadline, effort, priority):
    if effort <= 0:
        raise ValueError("Effort must be greater than 0")
    if priority not in ["Low", "Medium", "High"]:
        raise ValueError("Priority must be Low, Medium, or High")
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, deadline, effort, priority)
        VALUES (?, ?, ?, ?)
    """, (title, deadline, effort, priority))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks ORDER BY deadline")
    tasks = cursor.fetchall()

    conn.close()
    return tasks


def update_task(task_id, progress):
    if progress < 0 or progress > 100:
        raise ValueError("Progress must be between 0 and 100")
    conn = get_connection()
    cursor = conn.cursor()

    status = "Completed" if progress == 100 else "In Progress"

    cursor.execute("""
        UPDATE tasks
        SET progress = ?, status = ?
        WHERE id = ?
    """, (progress, status, task_id))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()