# Logs Analysis

## About
This project queries a large database with over a million records to answer 3 questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

It connects to a PostgreSQL database, run the queries and print out the results - each in its own format.
It uses the `log` table to determine the number of views of each article and the number of errors per day.

## How to run

### Pre-requisites

1. [VirtualBox](https://www.virtualbox.org/)
2. [Vagrant](https://www.vagrantup.com/)

### Installation
Install VirtualBox, Vagrant and clone [this repository](https://github.com/udacity/fullstack-nanodegree-vm).
Launch the Vagrant VM by running `vagrant up`. SSH into the newly created VM by running `vagrant ssh`.

Clone this repository by running `git clone git@github.com:mariopeixoto/udacity-logs-analysis.git`

Import news data into database by running `psql -d news -f newsdata.sql`
After that, create the following views in the `news` database:

```sql
CREATE VIEW error_pct_by_day_view AS
SELECT
  ROUND(
    SUM(CASE l.status WHEN '200 OK' THEN 0 ELSE 1 END)*100.0/COUNT(l.id)
  ,2) AS error_pct,
  date(time) AS day
FROM log l
GROUP BY day;
```

### Running
Execute `python logs.py` to run the reporting tool (example response below).

```
1. What are the most popular three articles of all time?
"Candidate is jerk, alleges rival" -- 338647 views 
"Bears love berries, alleges bear" -- 253801 views 
"Bad things gone, say good people" -- 170098 views 

2. Who are the most popular article authors of all time?
Ursula La Multa -- 507594 views 
Rudolf von Treppenwitz -- 423457 views 
Anonymous Contributor -- 170098 views 
Markoff Chaney -- 84557 views 

3. On which days did more than 1% of requests lead to errors?
2016-07-17 -- 2.26% errors
```