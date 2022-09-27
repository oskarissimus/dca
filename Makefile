requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

dotenv-yaml:
	python scripts/dotenv_to_yaml.py