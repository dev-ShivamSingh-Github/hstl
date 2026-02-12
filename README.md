## Hostel Management WebApp using django

### Pre-requisite: ``git, python``

## Quick start
1. Install app.
	```bash
	pip install django-hstl
	```
1. Modify settings.py such that
	```python
	AUTH_USER_MODEL = 'django_hstl.MyUser'
	
	# Add the app in your INSTALLED_APPS
	
	INSTALLED_APPS = [
		# ...,
		"django_hstl",
	]
	```
1. Include the app URLconf in your project urls.py like this
	```python
	path("hstl/", include("django_hstl.urls")),
	```
1. Run `python manage.py migrate` to create the models.
1. Create Superuser `manage.py createsuperuser`
1. Visit the `/hstl/` URL to explore the WEB APP.

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
	pip install django-hstl
	```
1. Create a django project
	```bash
	django-admin startproject MyApp .
	```
1. Modify "MyApp/setting.py" such that
	```python
	AUTH_USER_MODEL = 'django_hstl.MyUser'
	
	# Add the app in your INSTALLED_APPS
	
	INSTALLED_APPS = [
		# ...,
		"django_hstl",
	]
	```
1. Include the app URLconf in "MyApp/urls.py" like this
    ```python
	path("hstl/", include("django_hstl.urls")),
	```
1. Run `python manage.py migrate` to create the models.
1. Create Superuser `manage.py createsuperuser`
1. Visit the `/hstl/` URL to explore the WEB APP.
