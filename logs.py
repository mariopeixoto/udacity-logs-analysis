#!/usr/bin/env python3
import psycopg2

# 1. What are the most popular three articles of all time?
THREE_MOST_POPULAR_ARTICLES = """
    SELECT art.title, COUNT(l.id) AS num_views FROM articles art
    INNER JOIN log l ON l.path = concat('/article/', art.slug)
    GROUP BY art.id
    ORDER BY num_views DESC
    LIMIT 3
"""

# 2. Who are the most popular article authors of all time?
MOST_POPULAR_AUTHORS = """
    SELECT aut.name, COUNT(l.id) AS num_views FROM articles art
    INNER JOIN log l ON l.path = CONCAT('/article/', art.slug)
    INNER JOIN authors aut ON art.author = aut.id
    GROUP BY aut.id
    ORDER BY num_views DESC;
"""

# 3. On which days did more than 1% of requests lead to errors?
DAYS_MORE_THAN_1PCT_ERRORS = """
    SELECT day, error_pct FROM error_pct_by_day_view
    WHERE error_pct > 1;
"""


def connectDB(db_name):
    """Connect to database"""
    return psycopg2.connect(database=db_name)


def query(db, q):
    """Get a fresh cursor, execute the query against the provided db,
    close the cursor and return the results"""
    cursor = db.cursor()
    cursor.execute(q)
    result = cursor.fetchall()
    cursor.close()

    return result


def print_result(results, result_format):
    for r in results:
        print(result_format.format(*r))


# Connect to news database
db = connectDB("news")

print("1. What are the most popular three articles of all time?")
print_result(query(db, THREE_MOST_POPULAR_ARTICLES), "\"{}\" -- {} views ")

print("\n2. Who are the most popular article authors of all time?")
print_result(query(db, MOST_POPULAR_AUTHORS), "{} -- {} views ")

print("\n3. On which days did more than 1% of requests lead to errors?")
print_result(query(db, DAYS_MORE_THAN_1PCT_ERRORS), "{} -- {}% errors")

db.close()
