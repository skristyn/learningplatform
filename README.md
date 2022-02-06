# EII Learning Platform

## Creating a virtual environment
TO DO I've been using python poetry to do dependency management, but it may be easier to start to use
a basic python virtual env. Those are the steps that I've laid out here. This will be updated in the future,
along with automating some of these set up steps.

Install Python on your machine. I have been building with python 3.8.10 though I don't think the 
dependencies require that. Anything more recent than 3.7 should be fine.

Within the root folder of the project run the following:
`python -m venv env`

This will create a virtual environment in a new ./env directory. Then you can run
`source env/bin/activate` to activate the environment. 

_All other commands within this README must be run with this environment activated!_

Install all dependencies with `pip install -r requirements.txt`

## Running migrations & Loading example data

_These two commands will have to be run occasionally if there are db model changes_

The repo includes some sample data. First, however you have to run migrations. This can 
be done with the command `python manage.py migrate`

Once the migrations are run you can load the data with `python manage.py loaddata dev_example_data.json`

## Accessing Site
### Running the server
Starting the development server can be done with `python manage.py runserver`. This will start a development server
at localhost:8000.

### Logging in as superuser
In the database loaded with loaddata above, there is already a superuser created:

username: "user\_one"
password: "bad\_password"

For convinence the user is already enrolled in the course so after signin the data is available
from a student's point of view.

## API
### IMPORTANT: Change the wagtail site settings to the correct port
Once you have the server running you can sign into the wagtail backend at localhost:8000/admin. For the API to
serve the detail links correctly, you have to change the port setting. This can be done by clicking the settings
link at the bottom of the menu on the left of the admin page, then clicking 'sites'. If you click on localhost, you
will be taken to the site options page where you can set the port to 8000. _You will need to repeat this step when
starting the development server if you plan to browse the links with the drf explorer._ 

### Exploring the API with the Django Rest Framework GUI
Django Rest Framework provides a simple interface that should make it fairly straight forward to explore the data 
available from the API. With your browser you can navigate to the urls outlines below and it will show you the JSON
response to expect. 

### Main endpoints
All api endpoints are found at `<...localhost...>/api/v1` and they include the following:
- `/textbooks/` fields: `title, completed, lessons`
- `/lessons/` fields: `title, completed, sections, time_remaining`
- `/sections/` fields: `title, completed, slides, time_to_complete`
- `/slides/` fields: `title, body`
- `/grades/` [only accepts POST]
- `/images/` _currently empty_
- `/` _Root endpoint returns the authenticated user's current course, next section_ 
      _(or first if the user has completed the course) and announcements._

Each endpoint has a field that provides some data about child pages including links to 
their respective detail views to make it easy to move through the tree.

Most fields are accessed by adding a query ie `.../?fields=...`. You can provide a
comma-separated list of field names to select the data you need.

A detailed list of available fields for each endpoint is provided above.

### Base Wagtail page fields
For the most part, the content models subclass the Wagtail CMS's `Page` model. The full
guide to the API usage can be found [here](https://docs.wagtail.io/en/stable/advanced_topics/api/v2/usage.html#default-endpoint-fields)

## Example call using fetch with auth information
For development providing the username and password to the fetch call will work.

```
<script>
    let url = 'http://localhost:8000/api/v1/';
    let username = 'user_one';
    let password = 'bad_password';

    let headers = new Headers({
                'Authorization': `Basic  ${btoa(`${username}:${password}`)}`
            });
    fetch(url, {
                method:'GET',
                headers: headers
            })
      .then(response => response.json())
      .then(data => console.log(data));
</script>
```
