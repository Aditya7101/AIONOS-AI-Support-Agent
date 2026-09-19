import sqlite3
from datetime import datetime


DATABASE = "aionos.db"


def initialize_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE,
            issue TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_ticket(issue, priority="Medium"):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tickets
        (issue, priority, status, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        issue,
        priority,
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    database_id = cursor.lastrowid

    ticket_id = f"AIONOS-{1000 + database_id}"

    cursor.execute("""
        UPDATE tickets
        SET ticket_id = ?
        WHERE id = ?
    """, (ticket_id, database_id))

    connection.commit()
    connection.close()

    return ticket_id


def get_ticket(ticket_id):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticket_id, issue, priority, status, created_at
        FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id,))

    ticket = cursor.fetchone()

    connection.close()

    return ticket


def get_all_tickets():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticket_id, issue, priority, status, created_at
        FROM tickets
        ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    connection.close()

    return tickets


initialize_database()