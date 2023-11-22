# Shopping Buddy

A shopping list application made with *Flask*, *jinja* templating and *SQLAlchemy* (*SQLite* database)

Add products and recipes, which contain groups of products.
Select the products or recipes to be added to the grocery list and go shopping.

### Usage

Set environment variables `DEBUG` and `SECRET_KEY`

Run application with `flask run`

Run application with Gunicorn `gunicorn --bind 127.0.0.1:8000 appserver:gunicorn_app`

Or deploy the application to a server with `nginx` and `gunicorn` (see the readme in the folder called **ansible**)

Run unit tests `pytest`
