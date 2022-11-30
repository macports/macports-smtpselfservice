FROM alpine:edge
ARG user

ENV FLASK_APP smtpselfservice

RUN apk add --no-cache build-base cargo
RUN apk add --no-cache libffi-dev postgresql-dev python3-dev
RUN apk add --no-cache py3-pip py3-virtualenv
RUN virtualenv -p /usr/bin/python3 /usr/lib/poetry && . /usr/lib/poetry/bin/activate && pip install poetry

ENV HOME /tmp/home
RUN mkdir /tmp/home && chown $user /tmp/home

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY smtpselfservice/ ./smtpselfservice/
RUN chown -R $user .

USER $user

RUN /usr/lib/poetry/bin/poetry config virtualenvs.in-project true
RUN /usr/lib/poetry/bin/poetry install --only main --verbose --no-ansi --no-interaction

EXPOSE 5000/tcp
ENTRYPOINT ["/usr/lib/poetry/bin/poetry", "run"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "smtpselfservice.wsgi:app"]
