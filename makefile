EXPORT = export PYTHONPATH=$(PWD)

db:
	psql -c "DROP DATABASE IF EXISTS mms"
	#psql -c "DROP ROLE IF EXISTS mms_admin"
	#psql -c "CREATE USER mms_admin WITH SUPERUSER PASSWORD '12345'"
	psql -c "CREATE DATABASE harmony_product OWNER mms_admin"

db_test:
	psql -c "DROP DATABASE IF EXISTS mms_test"
	psql -c "CREATE DATABASE mms_test OWNER mms_admin"

migration:
	$(EXPORT) && pipenv run alembic revision --autogenerate -m "initial tables"

upgrade:
	$(EXPORT) && pipenv run alembic upgrade head

downgrade:
	$(EXPORT) && pipenv run alembic downgrade head

shell:
	$(EXPORT) && pipenv run python

# checks:
# 	$(EXPORT) && pipenv run sh scripts/checks.sh