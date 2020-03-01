# dvdjay
The bare minimum effort to keep a shred of sanity In the eternal fracas of media in our house

## Chaos this is intended to help manage

* Do we have Scrubs on DVD? Oh wait, or is that on your Mac? It's not in Plex...oh wait, only my computer goes to Plex
* Alexa, play Original Sin. Alexa, stop the music. Alexa, play INXS Original Sin. Oh for gods sakes, Alexa, stop the music. *opens Sonos app to play it from library*

## First:

* ~~Easily searchable or browseable catalog of video (cutouts for music, maybe other), with some data-driven attributes (shared across and/or specific to media type)~~
* ~~Add new show to catalog~~
* ~~Persistent data for media catalog~~
  * ~~ok, I give up, I've rewritten the same pickle/csv/etc. stuff over and over again for every little thing. going to make a data wrangler for that stuff that we can pull in as a submod~~
* ~~Add item to a given attribute list (e.g., create new Genre)~~
* Backup of catalog data to something like Google Sheets
* basic profiles (pick one / create new, cutouts for auth). profiles unlock future stuff like tags, lists, RBAC, etc.
* per-profile tags [to watch, love, hate]
* Class out the basic gvars and funcs of the media manager so we can start to abstract things out as we go

## Next
* API routes for GETs / POSTs
* Scrapers to automatically add stuff to the catalog:
  * filesystem path (incl. network mount)
  * iTunes library OTA
  * Sonos library?
* SENDER - make thing X play on device Y
  * Sonos library to start. Later, figure out apple tv? Chromecast? Don't want to reinvent wheels, but orchestrate into systems that do the lifting.
* profile stuff
  * little viz of all profiles' tags / other


