#!/home/dron/PycharmProjects/flaskProjects/tim_proj/venv/bin/python
from website import create_app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=8080)
