# Plex Generate Spoiler Free Thumbnails
Python script to create spoiler free (blurred) thumbnails for Plex TV shows

# How to use
1.  Install pillow: `pip install pillow`
2.  Copy `generate-thumbs.py` to a TV shows directory (e.g. `X:\TV Shows\The X-Files\...(place here)`) 
4.  Open Terminal and cd into the directory you copied `generate-thumbs.py` to (e.g. `cd "X:\TV Shows\The X-Files"`)
5.  Run `python generate-thumbs.py` and wait
6.  ...
7.  Profit

Optional: As the script iterates through all subdirectories and files recursively by default you could copy it to your main TV shows directory to generate thumbnails for all your TV shows. However, this could take a long time and has not been tested extensively.

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
