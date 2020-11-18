# smtpselfservice.macports.org

This Python web application allows [MacPorts Developers][macports-devs] to set
an SMTP password for the MacPorts mailserver.

It is written in Python >= 3.8, and uses the [Flask][flask] web application
framework.

## Development

To install a development copy of this, you will need [poetry][poetry], which
can be installed [from MacPorts][poetry-mp]. Once you have poetry installed,
run `poetry install` to download and install the required dependencies. Poetry
will by default do that in a virtualenv. Note that you may want to run `poetry
config virtualenvs.in-project true` to have the virtualenv created in the
project directory, rather than in some cache directory.

Start the server using

```
FLASK_APP=smtpselfservice FLASK_ENV=development poetry run flask run
```

The application will then be running on localhost:5000. Note that for the
application to work correctly, you will have to send a valid GitHub OAuth2
token with the `email:read` scope in the `X-Forwarded-Access-Token` HTTP
header. This can, for example, be achieved by forwarding your local
installation to the remote server running smtpselfservice.macports.org using

```
ssh -v -N -R:$remoteport:127.0.0.1:$localport $server
```

You can set the database URI using the `DATABASE_URI` environment variable. See
the documentation on [libpq connection strings][libpq-conn] for the format.

[macports-devs]: https://trac.macports.org/wiki/MacPortsDevelopers
[flask]: https://flask.palletsprojects.com/
[poetry]: https://python-poetry.org/
[poetry-mp]: https://ports.macports.org/port/poetry/summary
[libpq-conn]: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
