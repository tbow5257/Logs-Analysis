# Log Analysis Project by Thomas Bowen for Udacity FSND

This is a program designed for Udacity's PSQL Database named news, written in python3. It answers 3 questions about the database information by executing queries. Run the program via command line by entering 'python db_queries.py' and receive answers for:

- The top 3 most popular articles in the database
- The top 3 most popular authors
- The amount of days more than 1% of webpage requests lead to error

## Important information about query 3 DB views

Query 3, the amount of days more than 1% of webpage requests lead to error, requires PSQL views in order to execute properly. Please create these views in your PSQL console by running the following:
$ create view hitsperday as SELECT DISTINCT time::timestamp::date, count(time) FROM log GROUP BY time::timestamp::date;
$ create view errorsperday as SELECT DISTINCT time::timestamp:: date, count(time) FROM log WHERE status!='200 OK' GROUP BY time::timestamp::date;
$ create view errorscore as SELECT errorsperday.time, 100.00*(errorsperday.count)/(hitsperday.count) AS errorpercent FROM hitsperday, errorsperday WHERE errorsperday.time=hitsperday.time GROUP BY errorsperday.time, errorpercent;