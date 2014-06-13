WPR Events
==========

An event list/calendar that aggregates updated information about Mozilla events happening in all spaces around the world and on Air Mozilla so that people know what is happening, where, and when.


Installation steps (production)
-------------------------------

* Clone the repo: `git clone --recursive https://github.com/ppapadeas/wprevents`
* `cd wprevents`
* Assuming you have [virtualenv](http://www.virtualenv.org/en/latest/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) installed: `mkvirtualenv wprevents`
  * If you don't have virtualenv(wrapper) you can install them: `pip install virtualenvwrapper`
* Upgrade pip: `pip install -U pip`
* `pip install -r requirements/compiled.txt`
* `cp wprevents/settings/local.py-dist wprevents/settings/local.py`
* Configure variables in `wprevents/settings/local.py`:
  - Set DEV, DEBUG and TEMPLATE_DEBUG to False
  - Set a value for SECRET_KEY, HMAC_KEYS and SITE_URL
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

Stage server
------------
* (optional) Add fake events: `./manage.py loaddata data/dummy-events.json`
* Set up a cron job running this command: `./bin/update_site.py -e stage`

Adding a privileged user
------------------------
* `./manage.py createsuperuser` and enter the user's email address.