# Plex Generate Spoiler Free Thumbnails
Python script to create spoiler free (blurred) thumbnails for Plex TV shows

# How to use
 1.  Install pillow: `pip install pillow`
 2.  Copy `generate-thumbs.py` to a directory of choice or directly into TV shows directory (e.g. `X:\TV Shows\The X-Files\...(place here)`) 
 3.  Open Terminal and cd into the directory you copied `generate-thumbs.py` to (e.g. `cd "X:\TV Shows\The X-Files"`)
 4.  Run:
     1. `python generate-thumbs.py` directly to generate thumbnails in the directory the file is in and its subdirectories and files recursively
     2. `python generate-thumbs.py /your/folder` to only generate thumbnails in the specified directory and its subdirectories and files recursively and
7.  ...
8.  Profit

Optional: Without a directory argument the script iterates through all subdirectories and files recursively. You could copy it to your main TV shows directory to generate thumbnails for all your TV shows. However, this could take a long time and has not been tested extensively.

# Supported file types
The usuals, probably could be extended(?)
-  `.mkv`
-  `.mp4`
-  `.avi`

# Additional configuration
The following arguments are available:

|Argument|Information|
|-|-|
|`/my/folder/`|Path to the folder containing videos|
|`--force`|Force thumbnail creation even if they already exist|
|`--blur_radius 100`|Set the radius of the blur effect (default: 100)|
|`--thumb_quality 80`|Set the quality of the thumbnail (default: 80)|

e.g. `python generate-thumbs.py /my/tv-show/ --force --blur_radius 50 --thumb_quality 60`
