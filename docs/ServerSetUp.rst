The server in general a django project

So, the normal rules apply :D

#########################################
#########################################
##############SET UP  ###################
#########################################
#########################################

First, to set up the database (we actually not make any usage of that) we run:

python manage.py syncdb

You should select yes and add an admin profile.

The admin panel is enabled in the {site_url}/admin

To have the server running, run on the command line:

python manage.py runserver

#######
In production level it would be better to run the whole project under gunicorn.

command - gunicorn server.wsgi
or in Heroku

web: gunicorn server.wsgi to enable the dyno scaling!!



#########################################
#########################################
##############URLS    ###################
#########################################
#########################################


We have already presented the {site_url}/admin url
TO enable the capabilities of the map, the url is {site_url}/map

The public sparql endpoint is sitting at the {site_url}/sparql and is a GET request with a query parameter where
you give the query.
As simple as that.

You can also run it in the browser.
Some simple examples:

Return 1000 triples
http://127.0.0.1:8000/sparql?query=SELECT%20?s%20?p%20?o%20WHERE%20{%20?s%20?p%20?o}%20LIMIT%201000

The number of all triples in the triplestore
http://127.0.0.1:8000/sparql?query=SELECT%20(COUNT(*)%20AS%20?count)%20WHERE%20{%20?s%20?p%20?o}