## Hostel Management WebApp using django

### Pre-requisite: ``git, python``

## Getting Started
1. Create a directory and cd into it.
	```bash
	mkdir ./hstl/
	cd ./hstl
	```
1. Clone the repo.
	```bash
	git clone https://github.com/dev-ShivamSingh-Github/hstl.git .
	```
1. Create "env/" and "env/__ init __.py" and "env/key.py".
	* LINUX / MAC
	```bash
	mkdir ./env/
	touch ./env/__init__.py
	touch ./env/key.py
	```
	> Windows user can do it via their code editor
1. env/key.py contains "SECRET_KEY" variable's value.
	```python
	DJANGO_SECRET_KEY = '<Your django secret key>'
	```
1. Create a virtual environment and activate it.
	* LINUX / MAC
	```bash
	python3 -m venv .venv
	source ./.venv/bin/activate
	```
	* WINDOWS
	```bash
	python -m venv .venv
	.\.venv\Scripts\activate
	```
1. Install requirements.
	```bash
	pip install -r requirements.txt
	```
1. Migrations
	```bash
	./manage.py makemigrations
	./manage.py migrate
	```
1. Create Super User
	```bash
	./manage.py createsuperuser
	```
1. Runserver and explore the WebApp
	```bash
	./manage.py runserver
	```
