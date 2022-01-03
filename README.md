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
- `/` _Root endpoint returns the authenticated user's current course and next section._

Each endpoint has a field that provides some data about child pages including links to 
their respective detail views to make it easy to move through the tree.

Most fields are accessed by adding a query ie `.../?fields=...`. You can provide a
comma-separated list of field names to select the data you need.

A detailed list of available fields for each endpoint is provided below.

### Base Wagtail page fields
For the most part, the content models subclass the Wagtail CMS's `Page` model. The full
guide to the API usage can be found [here](https://docs.wagtail.io/en/stable/advanced_topics/api/v2/usage.html#default-endpoint-fields)

## Example calls
