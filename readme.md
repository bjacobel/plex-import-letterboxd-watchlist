# plex-import-letterboxd-watchlist

Export your Letterboxd watchlist to your Plex native watchlist.

Forked from https://github.com/techkek/PlexImportWatchlist

Minor improvements to:
* Improve dependency handling
* Be more reusable (use .env files, etc)

### Directions
1. Clone the repo
1. Install requirements from `requirements.txt`: `pip install -r requirements.txt`
1. Copy `.env.example` to `.env`
1. Provide values for the example secrets in `.env`
  - [Instructions on obtaining your Plex token can be found here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)
1. Run `python main.py`
