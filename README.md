# B2B Test Task

### Environment
Here is the complite list of environment variables that you can save in the `.env` file. Values for the sensitive variables are omitted, and all other variables have default values for local development.

    SECRET_KEY='secret'
    ALLOWED_HOSTS=localhost, 127.0.0.1
    DEBUG=True

    DB_ENGINE=django.db.backends.mysql
    DB_HOST=db
    DB_NAME=django
    DB_USER=django
    DB_PASSWORD='secret'

    MYSQL_ROOT_PASSWORD='secret'

### Build
Since we don’t have a shared image repository, you need to build the image manually:

    docker compose build app

If you encounter platform issues related to `poetry.lock`, remove it and reinstall all packages by running:

    poetry install

### Initialization
We need to set up our database first: create a user with privileges and schema. For this purpose, please run the following:

    docker compose run --rm --entrypoint=python3 app /app/init_local_db.py

If a connection error occurs, please report it to me. I may need to tweak the health check settings. However, try running the command again, as it should work on the second attempt.

Next, we need to migrate the schema to the DB:

    docker compose run --rm app migrate

As you can see, the entry point is the `manage.py` file if you use Docker Compose orchestration. If you run the Docker image manually, it will also work - see below...

To drop the DB, simply run:

    rm -rf ./mysql_data

then follow the steps above.

### Tests
After completing all the above steps, simply run the following:

    docker compose up -d
    docker compose exec app pytest

It will run a single test case. You can read the description in the `wallets/tests.py` module.

### Swagger
Please check the URL: <a href="http://localhost:8000/swagger/" target="_blank">http://localhost:8000/swagger/</a>

### Pre-production
I'm using Uvicorn with Gunicorn to run it in production, as I inherited this setup from previous projects. Although Uvicorn is not strictly necessary here, given that all the code is implemented in a linear approach with no cooperative multitasking, I prefer not to disrupt what is already working well.

Here are the commands for testing purposes only, which uses the same `.env` file and requires the DB service to be up and running (make sure it appears in `docker stats`) from the `docker-compose.yml` file:

    docker compose up -d db

    docker network create b2b-app-network

    docker run --rm -d \
        --env-file .env \
        --network b2b-app-network \
        --network b2b-db-network \
        --name b2b-app \
        -v b2b-static-volum:/app/static \
        b2b-app-image

In contrast to `runserver`, Gunicorn doesn't serve static files, so we have to use Nginx for that purpose:

    docker run --rm -d \
        --name b2b-nginx \
        --network b2b-app-network \
        -p 80:80 \
        -v ./nginx/80.conf:/etc/nginx/conf.d/default.conf:ro \
        -v b2b-static-volum:/media/static:ro \
        nginx:1.25.3-alpine

Check the auto-docs page: <a href="http://localhost/swagger/" target="_blank">http://localhost/swagger/</a>

To stop this weirdo:

    docker stop b2b-nginx
    docker stop b2b-app
    docker network rm b2b-app-network
    docker compose down

PS: The purpose of this mode is to demonstrate that the app image can run in different environments independently of the Docker Compose orchestration.
