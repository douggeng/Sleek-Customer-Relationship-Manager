# Sleek

A Customer Relationship Manager

## Description

Sleek (Customer Relationship Manager) website catered
towards real estate agents. My CRM opens in flask. Once you arrive at the website you have the option to login or
register. All the data is stored in a SQL database that connects a user to a specific id. This allows users to have their own client lists and
add/delete from only their specific database. Once logged in, the
index page is the table of clients in your system with names, emails, and phone numbers. Additionally, you have the capability to email off
the website to your customers from your personal email address.

## Getting Started

### Video Demo
[![Video Demo](https://img.youtube.com/vi/gb7Ahh8z0aQ/0.jpg)](https://www.youtube.com/watch?v=gb7Ahh8z0aQ)


### Libraries

* Flask
* Werkzeug.security
* Email.message
* Ssl
* Smtplib
* SQL
* Functools

### Instructions

* Run:
```
flask run
```
* Register account. (Use your gmail app password for email password)
* Now you can add contacts, delete contacts, and email!


## What I learned

* Utilizing flask.
* Working with 2 tables to connect user_ids with their data.
* Practiced new libraries to allow emailing.


## What I want to improve/add

* The UI.
* Having the email autofill names from database
* Making the program more dynamic
* Adding analytics for user
* Schedule emails
