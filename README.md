Description
===========

Darwins Music is a framework to work with the linked and the structured music data on the web. 
The modules which constituted the framwework allow a user to manage the data sources, 
map the entities between them,  visualize the data, and republish the data with added insights. 

The source code also includes a set of example use cases which are relevant to music information research. 
These include:

* Visualization fo evolution of genres by artist popularity over countries and time-periods. 
This can be accessed online: [http://darwinsmusic.herokuapp.com/](http://darwinsmusic.herokuapp.com/)
* Sentiment analysis of user-generated content, with observations on how to integrate and use
this data with the integrated data source
* Evaluation of richness of the vocabulary in the user-generated content

The available data sources at the moment are [DBPedia](http://dbpedia.org/) and [last.fm](http://last.fm/). 
We are pushing our work on Musicbrainz soon. Other data sources which will also be added in near future 
include twitter, youtube and facebook.


Setup Instructions
==================

Crawler
-------
Right now, the scripts are designed to quickly get data per genre from last.fm and DBPedia. 
Later they will be modularized and the documentation will change accordingly. At the moment,
just running the scripts as given below should fetch you data for each genre without any issue.
It also triplifies the data fetched and puts the resulting file at '../../data/<genre>/triples.nt'.

```bash
$ python getTracks.py <genre> '../../data/'
$ python getAlbums.py <genre> '../../data/'
$ python getArtists.py <genre> '../../data/'
$ python triplify.py <genre> '../../data/'
```


Server
------



Visualization
-------------


SPARQL endpoint
===============

Coming soon ...


Team
====

* Gopala Krishna Koduri
* Michael Petychakis
* Patrick Philipp
* Zaenal Akbar

