import os

import mysql.connector
from mysql.connector import Error


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "pyqt_app"),
        user=os.getenv("DB_USER", "pyqt_user"),
        password=os.getenv("DB_PASSWORD", ""),
        connection_timeout=10,
    )


def initialize_database():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                text VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()
    finally:
        connection.close()


def add_note(text):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO notes (text) VALUES (%s)",
            (text,),
        )

        connection.commit()
    finally:
        connection.close()


def get_notes():
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, text, created_at
            FROM notes
            ORDER BY id DESC
            """
        )

        return cursor.fetchall()
    finally:
        connection.close()


def delete_note(note_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM notes WHERE id = %s",
            (note_id,),
        )

        connection.commit()
    finally:
        connection.close()