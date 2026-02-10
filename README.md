## Hostel Management WebApp using django

### Pre-requisite: ``git, python``

## Quick start
1. Install app.
	```bash
	pip install ...
	```
1. Modify settings.py such that::
	```python
	AUTH_USER_MODEL = 'app.MyUser'
	# ...
	INSTALLED_APPS = [
		...,
		"app",
	]
	```
1. Include the app URLconf in your project urls.py like this::

    ``path("hstl/", include("app.urls")),``

1. Run ``python manage.py migrate`` to create the models.
1. Create Superuser::
	```python
	manage.py createsuperuser
	```
1. Visit the ``/hstl/`` URL to explore the WEB APP.

## Getting Started
1. Create a directory and cd into it.
	```bash
	mkdir ./hstl/
	cd ./hstl
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
1. Install app.
	```bash
	pip install ...
	```
1. Create a django project
	```bash
	django-admin startproject MyApp .
	```
1. Modify "MyApp/setting.py" such that::
	```python
	AUTH_USER_MODEL = 'app.MyUser'
	# ...
	INSTALLED_APPS = [
		# ...,
		"app",
	]
	```
1. Include the app URLconf in "MyApp/urls.py" like this::

    ``path("hstl/", include("app.urls")),``

1. Run ``python manage.py migrate`` to create the models.
1. Create Superuser::
	```python
	manage.py createsuperuser
	```
1. Visit the ``/hstl/`` URL to explore the WEB APP.
