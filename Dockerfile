FROM alpine:edge
ARG user

ENV FLASK_APP smtpselfservice
ENV FLASK_ENV production

RUN apk add --no-cache build-base cargo
RUN apk add --no-cache libffi-dev postgresql-dev python3-dev
RUN apk add --no-cache poetry py3-platformdirs

ENV HOME /tmp/home
RUN mkdir /tmp/home && chown $user /tmp/home

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY smtpselfservice/ ./smtpselfservice/
RUN chown -R $user .

USER $user

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev --verbose --no-ansi --no-interaction

EXPOSE 5000/tcp
ENTRYPOINT ["poetry", "run"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "smtpselfservice.wsgi:app"]
