### Running the Project

#### Development

To run the project in development mode with hot reloading enabled:

docker-compose up --build

The Flask backend will be available at `http://localhost:8080`, and the React frontend will be accessible at `http://localhost:3000`.

#### Production

To run the project in production mode:

1. Edit the `docker-compose.yml` file to change the target from `development` to `production` for both the backend and frontend services.
2. Then, run:

docker-compose up --build

This setup will build the React application into static files served by Nginx and run the Flask application behind Gunicorn as specified in the Dockerfiles.

### Cleanup

To stop and remove the containers, networks, and volumes created by `docker-compose`:

docker-compose down -v

