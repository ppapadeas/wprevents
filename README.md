WPR Events
==========

An event list/calendar that aggregates updated information about Mozilla events happening in all spaces around the world and on Air Mozilla so that people know what is happening, where, and when.


Installation
============

1. Clone the repo: `git clone --recursive https://github.com/ppapadeas/wprevents`
2. `cd wprevents`
3. Assuming you have [virtualenv](http://www.virtualenv.org/en/latest/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) installed: `mkvirtualenv wprevents`
    * If you don't have virtualenv(wrapper) you can install them: `pip install virtualenvwrapper`
4. Upgrade pip: `pip install -U pip`
5. `pip install -r requirements/compiled.txt`
. `cp wprevents/settings/local.py-dist wprevents/settings/local.py`
. Update the PRIVILEGED_USERS variable in `wprevents/settings/local.py` with your email
. Assuming you have MySQL installed, start the MySQL service and create a database in the mysql console: `create database wprevents;`
. `./manage.py update_product_details`
. `./manage.py syncdb`
. `./manage.py runserver`
. Make sure you have [node.js](http://nodejs.org/) and [npm](https://www.npmjs.org/) installed.
. `cd client`
. `npm install`
. `npm install -g gulp`
. `gulp build-prod`
. Open a browser to http://localhost:8000/
