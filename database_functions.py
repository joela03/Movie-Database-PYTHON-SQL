import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection, cursor
from imports import get_cursor
from datetime import date


def get_connection() -> connection:
    """Sets up connection"""
    return psycopg2.connect(
        "dbname=movies user=joel host=localhost")


def validate_sort_by(sort_by: str) -> bool:
    """Checks if we are sorting by a valid parameter"""
    if sort_by and sort_by not in ["title", "release_date", "genre", "revenue", "budget", "score"]:
        return False

    return True


def validate_sort_order(sort_order: str) -> bool:
    """Checks if we are ordering by a valid parameter"""
    if sort_order and sort_order not in ["asc", "desc"]:
        return False

    return True


def get_movies(search: str = None, sort_by: str = None, sort_order: str = None) -> list[dict]:
    """Gets all movies from table"""
    conn = get_connection()
    curs = get_cursor(conn)

    query = "SELECT * FROM movie"
    params = []

    if search:
        search = '%'+search+'%'
        query += " WHERE title ILIKE %s"
        params.append(search)

    if sort_by:
        query += " ORDER BY " + sort_by
        if sort_order:
            query += " " + sort_order

    print(query)
    curs.execute(query, tuple(params) if params else None)
    data = curs.fetchall()
    curs.close()

    return data


def add_movie(title: str, release_date: date, score: int,
              overview: str, orig_title: str, orig_lang: str,
              budget: int, revenue: int, country: str) -> dict:
    """Add's movie to table"""
    conn = get_connection()
    curs = get_cursor(conn)
