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
1. Create "hostelManagement/local_setting.py".
	* LINUX / MAC
	```bash
	touch ./hostelManagement/local_setting.py
	```
	> Windows user can do it via their code editor
1. hostelManagement/local_setting.py:
	```python
	DJANGO_SECRET_KEY = '<Your django secret key>'
	ALLOWED_HOSTS = []
	DEBUG = True
	```
	> Change settings according to the need
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
