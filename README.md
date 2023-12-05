# Overview
This is the entry for the aynchronous task for the Senior Full Stack Developer Position.

It was created using

* Python/Django
* django-ninja for API creation
* OpenAI for image analysis.

[Github](https://github.com/CodeCrow/edlight)

# Setup
Clone the code from github:

`git clone https://github.com/CodeCrow/edlight.git`

Navigate into the directory:

`cd edlight`

Build the local docker environment:

`docker-compose build`


## API keys

To access Open AI, you will have to sign up and get access keys, and then add them to the application.

1. Find the `edlight/settings/local_template.py` file and copy it to `edlight/settings/local.py `: 
  2. `cp edlight/settings/local_template.py edlight/settings/local.py`
  2. Make sure you do not add this new file to the respository.
2. Go to the [Open AI website](https://openai.com/) and sign up.
3. Once you have logged in, navigate to the [api-keys section](https://platform.openai.com/api-keys) and create a new secret key.
4. Open the `edlight/settings/local.py` file and replace <ENTER OPEN AI API KEY HERE> with the API key.

# Access

Make sure you are in the project directory.  Now run the following to stand the application up:

`docker-compose up`

You can access the api here: [http://127.0.0.1:8000/analyze/](http://127.0.0.1:8000/analyze/).  Images can be sent via 'POST' as a field named 'file'.

This can be accessed and tested most simply here: [http://127.0.0.1:8000/docs#/default/edlight_api_analyze](http://127.0.0.1:8000/docs#/default/edlight_api_analyze).   Click on the button marked 'Try it out' and then upload the file.

# Testing

To test, enter the docker container: 

`docker exec -it edlight-python-1 bash`

Then run the tests . . .

`./manage.py test --settings=edlight.settings.local`