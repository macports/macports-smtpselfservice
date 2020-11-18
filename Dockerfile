FROM alpine:latest
ARG user

ENV FLASK_APP smtpselfservice
ENV FLASK_ENV production

RUN echo "@edge http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --no-cache \
	build-base \
	python3 \
	python3-dev \
	libffi-dev \
	postgresql-dev \
	py3-virtualenv@edge \
	py3-distlib@edge \
	poetry@testing \
	py3-pkginfo@community \
	py3-secretstorage@community \
	py3-jeepney@community \
	py3-keyring@community

WORKDIR /app
COPY --chown=$user pyproject.toml poetry.lock ./
COPY --chown=$user smtpselfservice/ ./smtpselfservice/

USER $user

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev --verbose --no-ansi --no-interaction

EXPOSE 5000/tcp
ENTRYPOINT ["poetry", "run"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "smtpselfservice.wsgi:app"]
