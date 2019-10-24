ARG PYTHON_VERSION=3.7
FROM python:$PYTHON_VERSION-alpine
MAINTAINER Arthur Alvim

ARG LUIGI_VERSION=2.8.9
ARG LUIGI_SCHEDULER_DATABASE_URL
ARG LUIGI_PORT=8082

ENV LUIGI_VERSION $LUIGI_VERSION
ENV PYTHON_VERSION $PYTHON_VERSION
ENV LUIGI_SCHEDULER_DATABASE_URL $LUIGI_SCHEDULER_DATABASE_URL
ENV LUIGI_PORT $LUIGI_PORT
ENV LUIGI_CONFIG_DIR /luigi
ENV LUIGI_CONFIG_PATH /luigi/luigi.cfg

RUN apk add --no-cache --virtual .build-deps \
      build-base \
      gcc \
      libc-dev \
      musl-dev \
      postgresql-dev  \
      libffi-dev && \
    apk add --no-cache \
      postgresql-libs \
      bash && \
    pip install --no-cache-dir \
      luigi==${LUIGI_VERSION} \
      sqlalchemy==1.3.10 \
      psycopg2-binary \
      psycopg2==2.8.3 && \
    apk del .build-deps

RUN mkdir -p ${LUIGI_CONFIG_DIR}
COPY luigi.cfg ${LUIGI_CONFIG_DIR}/luigi.cfg

EXPOSE ${LUIGI_PORT}/TCP

CMD ["/bin/sh", "-c", "luigid \
     --port ${LUIGI_PORT} \
     --logdir ${LUIGI_CONFIG_DIR}"]
