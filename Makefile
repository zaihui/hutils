fix:
	@isort .
	@black -l 120 .

check:
	flake8 .
	isort --check .
	black -l 120 --check .

