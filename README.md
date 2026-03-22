# Plex Generate Spoiler Free Thumbnails
Python script to create spoiler-free (blurred) thumbnails for Plex TV shows. Uses ffmpeg to support AV1 and other modern codecs.

## Requirements
- Python 3.6 or higher
- ffmpeg installed on your system

## How to use
 1.  Install ffmpeg on a system-level: `sudo apt install ffmpeg`
 2.  Install ffmpeg-python, pillow and numpy: `pip install ffmpeg-python pillow numpy`
 3.  Make the script executable (if needed): `chmod +x /path/to/your/script.py`
 4.  Copy `generate-thumbs.py` to a directory of choice or directly into TV shows directory (e.g. `X:\TV Shows\The X-Files\...(place here)`)
 5.  Open Terminal and cd into the directory you copied `generate-thumbs.py` to (e.g. `cd "X:\TV Shows\The X-Files"`)
 6.  Run:
     1. `python generate-thumbs.py` directly to generate thumbnails in the directory the file is in and its subdirectories and files recursively
     2. `python generate-thumbs.py /your/folder` to only generate thumbnails in the specified directory and its subdirectories and files recursively
 7.  ...
 8.  Profit

## Supported file types (should support most of the codecs by using ffmpeg)
-  `.mkv`
-  `.mp4`
-  `.avi`

## Additional configuration
The following arguments are available:

|Argument|Information|
|-|-|
|`/my/folder/`|Path to the folder containing videos|
|`--force`|Force thumbnail creation even if they already exist|
|`--blur_radius 100`|Set the radius of the blur effect (default: 100)|
|`--thumb_quality 80`|Set the quality of the thumbnail (default: 80)|
|`--debug`|Enables debug output for frame analysis|

```python generate-thumbs.py /my/tv-show/ --force --blur_radius 50 --thumb_quality 60```

## Notes
- Without a directory argument, the script processes the current directory and all subdirectories recursively - you could copy it to your main TV shows directory to generate thumbnails for all your TV shows. However, this could take a long time and has not been tested extensively.
- Thumbnails are saved as JPG files with the same name as the video file (e.g., video.mkv → video.jpg)
- The script checks 21 frames around the middle timestamp to avoid black screens and transitions

## License

MIT License

Copyright (c) 2026 himynameisubik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
