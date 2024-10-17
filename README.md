# Shopping Buddy

A small shopping list application made with *Flask*, *jinja* templating and *SQLAlchemy* (*SQLite* database)

Add products and recipes, which contain groups of products.
Select the products or recipes to be added to the grocery list and go shopping!

### Usage

Set environment variables `DEBUG` and `SECRET_KEY`

The application can be run using various approaches:

#### Local install
Create a virtual environment for the app, install the requirements
`python -m venv venv`
`source ./venv/bin/activate`
`pip install -r requirements.txt`

1. Run application with `flask run`

2. Run application with Gunicorn `gunicorn --bind 127.0.0.1:8000 appserver:gunicorn_app`

Or...

Using Docker `docker compose up -d`

#### Server install

1. Deploy the application to a server with `nginx` and `gunicorn` (see the readme in the folder called **ansible**)

### Tests

Run unit tests `pytest`

### Notes
A GitHub action is configured to execute tests automatically when raising a PR to `main`

The repository structure:
* `app.py` the main application
* `appserver.py` used by gunicorn to start the application
* `extensions.py` SQLAlchemy object instance
* `models.py` table schema
* `routes.py` the api endpoints
* `utils.py` generic functions
* `ansible` folder containing ansible related information
* `templates` html template files
* `tests` unit testing
