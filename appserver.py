from app import create_app, DATABASE_URI


if __name__ == '__main__':
    create_app = create_app(DATABASE_URI)
    create_app.run()
else:
    gunicorn_app = create_app(DATABASE_URI)
