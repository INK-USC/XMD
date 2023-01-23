- The frontend stores data in DB using django.
- Django also acts as a gateway for the frontend to asynchronous send training requests to FastAPI.
- The model training updates are sent back to django by FastAPI
- ***(NEW)*** Django hosts front end static files, so running backend is sufficient to start the website.

# Table of contents

1. [Setup](#setup)
2. [URLs.py](#urls)
3. [Managers](#managers)
4. [Serializers](#serializers)

# Setup

1. Please install [Postgres 12.3](http://postgresguide.com/setup/install.html) (in the linked example they use
   PostgreSQL 9.2, please ensure you replace 9.2 with 12.3)
    - If on linux, please make sure to start postgres `sudo service postgresql start`
    - if you use the installation guide above for unix or windows you shouldn't have to do this
2. Ensure your `hilt-demo` environment is activated
3. We will now setup the postgres connection. So, ensure that postgres is up and running.
   Execute `cd HILT-demo/annotation_backend/annotation_backend`.
    - Inside the `annotation_backend` folder, navigate to [settings.py](annotation_backend/settings.py#L82)
        - Find the `DATABASES` dictionary, and replace the `PASSWORD` value with your own password
4. Run:
    - Create superuser/admin use django's `python manage.py createsuperuser`
5. Start the backend from `cd HILT-demo/annotation_backend` folder: `python manage.py runserver 0.0.0.0:8000`

### Potential Errors:

- Postgres is not installed:
    - To check: Open up terminal and exectue `which psql`. This should return a path.
    - To solve: Please follow the example [provided](http://postgresguide.com/setup/install.html)
- Some other application is listening on port 5432
    - To check: (Unix, Linux): `sudo lsof -i:5432`, (Windows): `netstat -tulpn | grep 5432`
        - [Useful Link](https://www.cyberciti.biz/faq/unix-linux-check-if-port-is-in-use-command/)
    - To solve: Get the Process ID of the application running on the port and kill the process.
        - [Windows](https://www.revisitclass.com/networking/how-to-kill-a-process-which-is-using-port-8080-in-windows/)
        - [Unix, Linux––2nd Answer](https://stackoverflow.com/questions/3855127/find-and-kill-process-locking-port-3000-on-mac)

# URLs

- Paths starting with `api/` are used by Vue.js frontend to save and retrieve data.

# Django Rest Framework

- DRF if used in this project to create views faster using models, serializers & DRF helpers.