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
6. `cp wprevents/settings/local.py-dist wprevents/settings/local.py`
7. Update the PRIVILEGED_USERS variable in `wprevents/settings/local.py` with your email
8. Assuming you have MySQL installed, start the MySQL service and create a database in the mysql console: `create database wprevents;`
9. `./manage.py update_product_details`
10. `./manage.py syncdb`
11. `./manage.py runserver`
12. Make sure you have [node.js](http://nodejs.org/) and [npm](https://www.npmjs.org/) installed.
13. `cd client`
14. `npm install`
15. `npm install -g gulp`
16. `gulp build-prod`
17. Open a browser to http://localhost:8000/
