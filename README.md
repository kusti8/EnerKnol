# EnerKnol - MovieSearch

Demo: https://immense-shore-53640.herokuapp.com/

## Requirements Fullfilled

* Login/Registration with MySQL ORM (SQLAlchemy)
* Keyword search box searching multiple fields
* Data stored in MongoDB and ElasticSearch with same _id
* Results displayed with lazy pagination
* New tab displaying data from MongoDB

### Bonuses

* ElasticSearch and MongoDB ODMs used
* Scraper for ImDB written using BeautifulSoup4, retrieving 9 fields

### Extra features

* Favorite selection for each movie w/ realtime saving, which stores a list of favorites in the MySQL database
* Show a list of favorites on the main-page using a button
* Password hashing

## Structure

The file structure is separated into groups of files that perform similar functions.

* `users/` - Manages all user state through a MySQL database, using SQLAlchemy ORMs
* `el_search/` - Manages all internal movie information through ElasticSearch using elasticsearch_dsl ODMs and a MongoDB database using mongoengine ODMs
* `main.py` - The main flask application that runs the project
* `templates/` - The templates for all the webpages used for Flask, using Jinja2 templating
* `static/` - All the static elements that the templates depend on, including CSS and images
* `clear_all.sh` - Delete all data from ElasticSearch and MongoDB

## Hosting locations

Total movies: ~15,000

Flask server - Heroku
MySQL - AWS
MongoDB - mLab
ElasticSearch - ElasticCloud

## File Descriptions

### main.py

The main python entrypoint, which has a Flask application. This has multiple endpoints configured:

* `/` - Only showed to logged in users.
    * `GET` - The main search box. Accepts arguments for page, query, and favorites
    * `POST` - Signout the user
* `/login`
    * `GET` - Show the login/register page
    * `POST` - Try to login the user
* `/register`
    * `POST` - Try to register the user
* `/item` - Only showed to logged in users.
    * `GET` - Display one movie item
    * `POST` - Set the item favorite

### searchmanager.py

Two classes, one for elasticsearch_dsl and one for mongoengine. Both are ODMs

`MovieItem` is an ElasticSearch ODM, while `MovieItemDB` is a MongoDB ODM.

A third class, `MovieItemManager` is used to manage both ElasticSearch and MongoDB simultaneously, and is used in main to initialize the DBs and request values.
Currently, the class can add, search, and retrieve movies. The class makes sure that the same data is added to both ODMs using the `copy_attributes()` function.

When run normally, this also creates the ElasticSearch mappings.

### scraper.py

This scrapes ImDB for the 200 movies with the most votes, from each year 1940-2018. This downloads around ~15,000 movies in total. It uses bs4 to extract each individual movie information from the page. Some are not present for all movies, so it checks before adding them to prevent any errors from occuring. It fully populates `MovieItem`. Using `MovieItemManager`, it adds it to ElasticSearch and MongoDB, making sure they have the same ID.

`get_directors()` is a helper function because some movies don't have directors, and the only separator for directors and stars is a vertical line, so if filters for that and correctly returns the list of directors and stars.

### manage_users.py

A single class which handles the user database. The ORM is retireved from `models.py`, while `ManageUsers` gives functions to add users, login users, retireve user info,
and set and get favorites, for each user.

### models.py

Declares the User model for the MySQL database. This, when run as a script, creates the table for the Users.

### templates/

The templates for each page, including login, index, and item. They all use Jinja2 server rendering rather than something like React. All the CSS and images that they depend on is in static.

## Typical Flowchart

Typically, the user logs in -> searches something -> and clicks on a movie to view it.

In the code, this works by:

* Redirecting to `/login` because there was no username in the session. This receives a POST request when the HTML form is submitted, which tries to login the user by checking the password hash. If it is successful, the user is redirected to `/index`. If not, an error is passed to Jinja.

* In `/index`, the user is presented with a search box. They can type, and when enter is pressed, JS changes the URL to add a `GET` parameter `q`, which sets the search query. The endpoint sees that `q` is present, so it uses `MovieManager` to search. It handles pages by another `GET` parameter `page` which defaults to 1. In `index.html`, using Jinja, it constructs a URL for next and previous if they exist. If the user clicks the favorites button, a GET request is send using parameter `favorites`, which queries the MySQL database for favorites and returns them. The user then clicks on a movie.

* This then opens a new tab with the `/item` endpoint, with the `GET` parameter `id` setting the id to retrieve. This returns the information formattted with Jinja. It also updates the favorites button. If the user toggles the favorite button, JS sends a `POST` request to `/item` with the id and status, which saves or deletes the favorite.