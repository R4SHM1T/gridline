.PHONY: demo db ingestion dbt test clean

demo:
	docker-compose up -d
	@echo "Waiting for postgres to start..."
	sleep 5
	python ingestion/db.py
	python simulator/simulate.py
	python ingestion/run_ingestion.py
	cd dbt && dbt run
	@echo "Demo stack is up! Metabase available at http://localhost:3000"

db:
	docker-compose up -d postgres

ingestion: db
	python ingestion/db.py
	python ingestion/run_ingestion.py

dbt:
	cd dbt && dbt run

test:
	python -m unittest discover simulator/tests

clean:
	docker-compose down -v
