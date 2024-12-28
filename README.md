# Plex Generate Spoiler Free Thumbnails
Python script to create spoiler free (blurred) thumbnails for Plex TV shows

# Folder structure
The script iterates through all directories and their sub directories from where it is placed and executed and will generate blurred thumbnails for every file it supports. 

In a specific TV show folder to generate thumbnails only for a specific TV show:
`.../TV Shows/The X-Files/...(place here)`

In your main TV shows directory to generate thumbnails for all your TV shows:
`.../TV Shows/...(place here)`

# How to use
1. Install pillow: `pip install pillow`
2. Copy paste `generate-thumbs.py` in to your desired TV shows folder (e.g. `X:\TV Shows\The X-Files`)
3. Open Terminal and cd into the folder you copied `generate-thumbs.py` to (e.g. `cd "X:\TV Shows\The X-Files"`)
4. Run `python generate-thumbs.py` and wait
5. ...
6. Profit

# Supported file types
The usuals, probably could be extended(?)
-  `.mkv`
-  `.mp4`
-  `.avi`

# Additional configuration
The following arguments are available:

|Argument|Information|
|-|-|
|`--force`|Forces the regeneration of existing thumbnails|
|`--blur_radius 100`|Changes the blur amount (default: 100)|
|`--thumb_quality 80`|Changes the quality (default: 80)|

e.g. `python generate-thumbs.py --force --blur_radius 50 --thumb_quality 60`
