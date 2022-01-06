# EII Learning Platform

## Creating a virtual environment
TO DO I've been using python poetry to do dependency management, but it may be easier to start to use
a basic python virtual env. Those are the steps that I've laid out here. This will be updated in the future,
along with automating some of these set up steps.

Install Python on your machine. I have been building with python 3.8.10 though I don't think the 
dependencies require that. Anything between 3.7 and 3.9 should be fine.

Within the root folder of the project run the following:
`python -m venv env`

This will create a virtual environment in a new ./env directory. Then you can run
`source env/bin/activate` to activate the environment. All other commands within this
README must be run with this environment activated.

Install all dependencies with `pip install -r requirements.txt`

## Running migrations & Loading example data
The repo includes some sample data. First, however you have to run migrations. This can 
be done with the command `python manage.py migrate`

Once the migrations are run you can load the data with `python manage.py loaddata <fixture-name>`


## Accessing Site

### Creating superuser

To create a superuser that will give you access to the wagtail CMS and Django admin pages, you can run
the command `python manage.py createsuperuser` which will prompt you to create a username and password.

TO DO This is currently throwing an error, due to a missing file, *but do not fear, the user is created anyway*.


## API

### Exploring the API with the Django Rest Framework GUI
Django Rest Framework provides a simple interface that should make it fairly straight forward to explore the data 
available from the API. With your browser you can navigate to the urls outlines below and it will show you the JSON
response to expect. 

### Main endpoints
All api endpoints are found at `<...localhost...>/api/v1` and they include the following:
- `/textbooks/` fields: title, completed, lessons
- `/lessons/` fields: title, completed, sections
- `/sections/` fields: title, completed, slides
- `/slides/` fields: title, body
- `/grades/` [only accepts POST]
- `/` _Root endpoint returns the authenticated user's current course and next section._

Each endpoint has a field that provides some data about child pages including links to 
their respective detail views to make it easy to move through the tree.

Most fields are accessed by adding a query ie `.../?fields=...`. You can provide a
comma-separated list of field names to select the data you need.

A detailed list of available fields for each endpoint is provided above.

### Base Wagtail page fields
For the most part, the content models subclass the Wagtail CMS's `Page` model. The full
guide to the API usage can be found [here](https://docs.wagtail.io/en/stable/advanced_topics/api/v2/usage.html#default-endpoint-fields)

## Example calls
