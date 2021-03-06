FROM alpine:edge
ARG user

ENV FLASK_APP smtpselfservice
ENV FLASK_ENV production

RUN echo "@testing https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --no-cache \
	build-base \
	python3 \
	python3-dev \
	libffi-dev \
	postgresql-dev \
	py3-virtualenv \
	py3-distlib \
	poetry@testing


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
