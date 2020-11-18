"""
WSGI entrypoint for smtpselfservice
"""

from smtpselfservice import app

if __name__ == "__main__":
    app.run()
