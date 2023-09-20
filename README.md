# JustWatch Scrapper
This scrapper is just a handy project that I have made for myself. As such, the results can't be fully trusted and it may lead to some false positives.

It's only intended usage is for streaming services in Spain.
## Requirements
 - `pip install -r requirements`
 - You need your Letterboxd watchlist file as a CSV input. You can download it from your settings.
 - Optionally, you may add a `streaming_platforms.txt` file to indicate which platforms you have access, and only show in the final results the movies that are streaming in said services. If the file is not present, it will show everything.
## Usage
 - Run `python scrapper.py`. 
