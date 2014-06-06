WPR Events
==========

An event list/calendar that aggregates updated information about Mozilla events happening in all spaces around the world and on Air Mozilla so that people know what is happening, where, and when.


Installation (staging/prod)
===========================

1. Clone the repo: `git clone --recursive https://github.com/ppapadeas/wprevents`
2. `cd wprevents`
3. Assuming you have [virtualenv](http://www.virtualenv.org/en/latest/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) installed: `mkvirtualenv wprevents`
    * If you don't have virtualenv(wrapper) you can install them: `pip install virtualenvwrapper`
4. Upgrade pip: `pip install -U pip`
5. `pip install -r requirements/compiled.txt`
6. `cp wprevents/settings/local.py-dist wprevents/settings/local.py`
7. Update the PRIVILEGED_USERS variable in `wprevents/settings/local.py` with your email
8. Update the SECRET_KEY variable in `wprevents/settings/local.py`
9. Assuming you have MySQL installed, start the MySQL service and create a database in the mysql console: `create database wprevents;`
10. `./manage.py update_product_details`
11. `./manage.py syncdb`
13. Make sure you have [node.js](http://nodejs.org/) and [npm](https://www.npmjs.org/) installed.
14. `cd client`
15. `npm install`
16. `npm install -g gulp`
17. `gulp build-prod`
18. Make sure the Apache `mod_wsgi` is installed
19. Configure an Apache VirtualHost directive as described here: http://playdoh.readthedocs.org/en/latest/operations.html
20. Restart Apache

In order to updated the environment automatically on the stage server, set up a cron job running this command: `./bin/update_site.py -e stage`



