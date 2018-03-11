# EnerKnol - MovieSearch

## Structure

The file structure is separated into groups of files that perform similar functions.

* users/ - Manages all user state through a MySQL database, using SQLAlchemy ORMs
* el_search/ - Manages all internal movie information through ElasticSearch using elasticsearch_dsl ODMs and a MongoDB database using mongoengine ODMs
* main.py - The main flask application that runs the project
* templates/ - The templates for all the webpages used for Flask, using Jinja2 templating
* static/ - All the static elements that the templates depend on, including CSS and transpiled external JS
* js/ - The un-transpiled JS, utilizing React for easy HTML display
* clear_all.sh - Delete all data from ElasticSearch and MongoDB

## File Descriptions

### main.py

The main python entrypoint, which has a Flask application. This has multiple endpoints configured:

* / - Only showed to logged in users.
    * GET - The main search box.
    * POST - Signout the user
* /login
    * GET - Show the login/register page
    * POST - Try to login the user
* /register
    * POST - Try to register the user
* /search - Only showed to logged in users.
    * POST - Retrieve search results
* /item - Only showed to logged in users.
    * GET - Display one movie item
    * POST - Set the item favorite
* /favorites - Only showed to logged in users.
    * GET - get the list of favorites for the user

