## cornershop-backend-test

Needs `SLACK_TOKEN` and `SERVER_URL` in the environment variables.

To use the base development ecosystem maybe it's needed to give permissions to some files and directories (Because windows).

I used `docker-compose up -d celery_worker` to create a celery server

`docker-compose up -d redis` for the redis server

and `docker-compose run --service-ports --rm backend` to run the dev server.

The image now has a working selenium google-chrome-drive for testing.

TODO: Refactor with fixtures in the tests :(
 
### Running the development environment

* `make up`
* `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000

