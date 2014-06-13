WPR Events
==========

An event list/calendar that aggregates updated information about Mozilla events happening in all spaces around the world and on Air Mozilla so that people know what is happening, where, and when.


Installation (staging/prod)
===========================

* Clone the repo: `git clone --recursive https://github.com/ppapadeas/wprevents`
* `cd wprevents`
* Assuming you have [virtualenv](http://www.virtualenv.org/en/latest/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) installed: `mkvirtualenv wprevents`
  * If you don't have virtualenv(wrapper) you can install them: `pip install virtualenvwrapper`
* Upgrade pip: `pip install -U pip`
* `pip install -r requirements/compiled.txt`
* `cp wprevents/settings/local.py-dist wprevents/settings/local.py`
* Update the SECRET_KEY variable in `wprevents/settings/local.py`
* Assuming you have MySQL installed, start the MySQL service and create a database in the mysql console: `create database wprevents;`
* `./manage.py update_product_details`
* `./manage.py syncdb`
* Make sure you have [node.js](http://nodejs.org/) and [npm](https://www.npmjs.org/) installed.
* `cd client`
* `npm install`
* `npm install -g gulp`
* `gulp build-prod`
* Make sure the Apache `mod_wsgi` is installed
* Configure an Apache VirtualHost directive as described here: http://playdoh.readthedocs.org/en/latest/operations.html
* Restart Apache

Adding a user
=============
* `./manage.py createsuperuser` with the admin email address.

Updating the stage/prod server
==============================
* Set up a cron job running this command: `./bin/update_site.py -e stage`
