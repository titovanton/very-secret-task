# ---------------
# Python version
ARG PYTHON_V=3.12
ARG BUILD_FOR=dev
ARG USER_NAME=django


# ---------------
# Gunicorn/Uvicorn default settings
ARG WORKERS=1
ARG TIMEOUT=10
ARG USER=$USER_NAME
ARG PORT=8000
ARG HOST=0.0.0.0


# ---------------
# FULL SIZE IMAGE
FROM python:${PYTHON_V} as build-python
MAINTAINER Titov Anton <webdev@titovanton.com>

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.in-project false
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY ./pyproject.toml /app
COPY ./poetry.lock /app

ARG BUILD_FOR
RUN poetry install --no-interaction \
    $(test "${BUILD_FOR}" != "dev" && echo "--no-dev")

# I don't have C libs dependencies for this package on my
# local macOS, so I'm adding them manually here.
RUN poetry add mysqlclient:^2.2.4


# ----------
# SLIM IMAGE
FROM python:${PYTHON_V}-slim
MAINTAINER Titov Anton <webdev@titovanton.com>

ARG USER_NAME
RUN adduser --disabled-password $USER_NAME

ARG PYTHON_V

# These C libraries are required by mysqlclient.
# The cost is 116MB. I could go wild and copy the C libraries,
# but that's too painful. Moreover, their location depends on
# the platform, which further complicates the problem.
RUN apt-get update
RUN apt-get install -y libmariadb-dev

# Copy all of the python packages
COPY --from=build-python \
    /usr/local/lib/python$PYTHON_V/site-packages/ \
    /usr/local/lib/python$PYTHON_V/site-packages/
COPY --from=build-python \
    /usr/local/bin/ \
    /usr/local/bin/

WORKDIR /app

COPY ./b2btest /app

RUN chown -R $USER_NAME:$USER_NAME /app

USER $USER_NAME

ARG WORKERS
ARG TIMEOUT
ARG USER
ARG PORT
ARG HOST

ENV WORKERS=$WORKERS
ENV TIMEOUT=$TIMEOUT
ENV USER=$USER
ENV PORT=$PORT
ENV HOST=$HOST

ENTRYPOINT ["gunicorn", "main.asgi:application"]
CMD ["-c", "/app/gunicorn.conf.py"]
