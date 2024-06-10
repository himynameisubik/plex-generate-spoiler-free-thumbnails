# Plex Generate Spoiler Free Thumbnails
 Simple python script to create spoiler free (blurred) thumbnails for Plex TV Shows

# Supported folder structure
 Both loose and season folder structure works
 - `.../The Office/Season X/...(files are here)`
 - `.../The Office/...(files are here)` 

# Supported file types
 The usuals, probably could be extended(?)
- `.mkv`
- `.mp4`
- `.avi`

# How to use
 1. Install pillow: `pip install pillow`
 2. Copy paste `generate-thumbs.py` in to your desired TV shows folder (e.g. `X:\TV Shows\The Office`)
 3. Open Terminal and cd into the folder you copied `generate-thumbs.py` to (e.g. `cd "X:\TV Shows\The Office"`)
 4. Run `python generate-thumbs.py` and wait
 5. ...
 6. Profit

# Configuration
 - Line #68: configure the amount of blur for the thumbnail (default: 100)
 - Line #71: configure the quality of the thumbnail picture (default: 80)
