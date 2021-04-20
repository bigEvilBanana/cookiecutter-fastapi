Cookiecutter FastAPI
=====================

Powered by Cookiecutter_, Cookiecutter FastAPI is a framework that helps you to start
production-ready FastAPI projects quickly.

* Documentation: it's in progress
* If you have problems with Cookiecutter FastAPI, please open issues_

.. _issues: https://github.com/

Features
---------

* Works with Python 3.9
* FastAPI 0.63.0
* PostgreSQL + * SQLAlchemy models
* Alembic migrations.
* Basic starting models for users (modify and remove as you need).
* Secure password hashing by default.
* JWT token authentication.
* CORS (Cross Origin Resource Sharing).
* Gitlab CI or Github Actions support (by your choice) with backend linters, testing.
* Run tests with unittest or pytest
* Production ready Python web server using Uvicorn and Gunicorn. (TODO)

TODO:
* Default integration with pre-commit_ for identifying simple issues before submission to code review
.. _pre-commit: https://github.com/pre-commit/pre-commit


Acknowledgments
---------------------
We express my deep gratitude to the Mr. Sebastián Ramírez aka tiangolo_ for his work on creating a wonderful framework FastAPI. A lot of the code for this project was taken from his full-stack-fastapi-postgresql_ repository.
It seemed a bit heavy to me, so we created my own lightweight version. Hope you enjoy it :)

.. _tiangolo: https://github.com/tiangolo
.. _full-stack-fastapi-postgresql: https://github.com/tiangolo/full-stack-fastapi-postgresql

Also I'd like to say Thank you to all of the creators of Cookiecutter-Django_.
This is a very cool project with the same idea, but under the Django framework.

We admire the work they have done!

.. _Cookiecutter-Django: https://github.com/pydanny/cookiecutter-django


Usage
------

First, get Cookiecutter. Trust me, it's awesome::

    $ pip3 install "cookiecutter>=1.7.0"

Now run it against this repo::

    $ cookiecutter https://github.com/bigEvilBanana/cookiecutter-fastapi

You'll be prompted for some values. Provide them, then a FastAPI project will be created for you.


Optional Integrations
---------------------

*These features can be enabled during initial project setup.*
TODO

Constraints
-----------

* Only maintained 3rd party libraries are used.
* Environment variables for configuration (This won't work with Apache/mod_wsgi).

pyup
~~~~~~~~~~~~~~~~~~

.. image:: https://pyup.io/static/images/logo.png
   :name: pyup
   :align: center
   :alt: pyup
   :target: https://pyup.io/

Pyup brings you automated security and dependency updates used by Google and other organizations. Free for open source projects!


Community
-----------

If you think you found a bug or want to request a feature, please open an issue_.

.. _`issue`: https://github.com/


Not Exactly What You Want?
---------------------------

This is what I want. *It might not be what you want.* Don't worry, you have options:

Fork This
~~~~~~~~~~

If you have differences in your preferred setup, we encourage you to fork this to create your own version.
Once you have your fork working, let me know and I'll add it to a '*Similar Cookiecutter Templates*' list here.
It's up to you whether or not to rename your fork.

If you do rename your fork, we encourage you to submit it to the following places:

* cookiecutter_ so it gets listed in the README as a template.

.. _cookiecutter: https://github.com/cookiecutter/cookiecutter

Submit a Pull Request
~~~~~~~~~~~~~~~~~~~~~~

We accept pull requests if they're small, atomic, and make our own project development
experience better.
