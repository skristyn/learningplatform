# EII Learning Platform

## Using Poetry to Manage Dependencies
## Loading Fixtures
## Accessing Site
## API
### Main Endpoints
All api endpoints are found at .../api/v1/ and they include the following:
- `/textbooks/`
- `/lessons/`
- `/sections/`
- `/grades/`
- `/` The root endpoint returns the users current course and next incomplete section. 

### Base Wagtail Page Fields
For the most part, the content models subclass the Wagtail CMS's PAGE model. The full
guide to the API usage can be found [here](https://docs.wagtail.io/en/stable/advanced_topics/api/v2/usage.html#default-endpoint-fields)

## Example Calls
