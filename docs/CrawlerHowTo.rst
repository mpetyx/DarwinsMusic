Running the crawler
===================

Right now, the crawler starts scraping from last.fm. In future this is scheduled to start from musicbrainz. Here is how the scripts need to be run to get the data about recordings, albums and artists:

In the crawler directory:

For the following scripts, the first argument is tag, and second argument is the data folder.

python getTracks.py 'jazz' '../../data/'    -> gets the toptracks for the given tag, and also detailed information for each track.

python getAlbums.py 'jazz' '../../data/'    -> gets the album information of all the tracks that are previously fetched.

python getArtists.py 'jazz' '../../data/'   -> gets the artist information which includes geo and influence information.
