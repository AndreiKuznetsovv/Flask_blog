#!/home/dron/PycharmProjects/flaskProjects/flask_blog/venv/bin/python
from website import create_app
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8080)
