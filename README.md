## Wookie Books with FastAPI

Make sure you have Docker and Docker Compose installed. This makes use of PostgreSQL.

1. Ensure you are in the root (`wookie-books`) directory
2. Run `docker-compose up -d` (this will download the postgres
   image and build the image for the wookie books app)
3. Visit `http://localhost:8001/` and `http://localhost:8001/docs` for the documentation


If you want to run locally with `Poetry`, follow these steps listed below instead. This makes use of SQLite.

1. `pip install poetry`
2. Install dependencies `cd` into the `app` directory where the `pyproject.toml` is located then `poetry install`
3. Run the DB migrations via poetry `poetry run python app/prestart.py`
4. Uncomment out the section highlighted in `app/run.sh` file
5. Run the FastAPI server via poetry with the bash script: `poetry run ./run.sh`
6. Visit `http://localhost:8001/`  and `http://localhost:8001/docs` for the documentation

