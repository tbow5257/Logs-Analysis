#!/usr/bin/env python3

import sys
import psycopg2


def connect(database_name, username):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name),
                              user=username)
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def fetch_query(query):
    """Login to the PSQL database and execute query. Return results
     for later use."""
    db, c = connect("news", "vagrant")

    c.execute(query)

    results = c.fetchall()

    c.close()

    db.close()

    return results


def print_top_articles():
    """Print the top articles from the DB by calculating the amount of
    webpage requests a singles article gets and sorting by highest amount"""
    results = fetch_query("SELECT title, COUNT(path) "
                          "AS views FROM log, articles "
                          "WHERE log.path = ('/article/' || articles.slug)"
                          "GROUP BY title ORDER BY 2 DESC LIMIT 3;")

    print('The top 3 articles of all time are:')

    for title, views in results:
        print("\"{}\" -- {} views".format(title, views))


def print_top_authors():
    """Print the top authors in the DB by summation of their article
    webpage requests, which is then sorted by most page hits"""
    results = fetch_query("SELECT authors.name, COUNT(path) as views "
                          "FROM log, articles "
                          "INNER JOIN authors ON authors.id=articles.author "
                          "WHERE log.path = ('/article/' || articles.slug)"
                          "GROUP BY authors.name ORDER BY 2 DESC ;")

    print("\nThe top authors of all time are:")

    for name, views in results:
        print("\"{}\" -- {} views".format(name, views))


def print_top_error_days():
    """Print the percentage of errors in which users do not request
    a page correctly if it is greater than 1 percent"""
    results = fetch_query("select time, (round(errorpercent, 2) || '%') "
                          "from errorscore where errorpercent > 1;")

    print('\nDays with error percentage greater than 1:')

    for time, errorpercent in results:
        print("\"{}\" -- {} views".format(time, errorpercent))

if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
