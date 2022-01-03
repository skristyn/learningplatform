# EII Learning Platform

## Using Poetry to install dependencies
## Loading fixtures
## Accessing Site
## API
### Main endpoints
All api endpoints are found at `<...localhost...>/api/v1` and they include the following:
- `/textbooks/`
- `/lessons/`
- `/sections/`
- `/slides/`
- `/grades/`
- `/` _The root endpoint returns the users current course and next incomplete section._
Each endpoint has a field that provides some data about child pages including links to 
their respective detail views.

### Base Wagtail page fields
For the most part, the content models subclass the Wagtail CMS's `Page` model. The full
guide to the API usage can be found [here](https://docs.wagtail.io/en/stable/advanced_topics/api/v2/usage.html#default-endpoint-fields)

## Example calls
