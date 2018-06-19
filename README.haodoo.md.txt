# Suite Description

## Introduciton

This suite is written to help backing up haodoo site.

## Scripts

1. haodoo_spider.py

   a. This script crawls the haodoo site and extract the epub files and (if existing) the cover images.
   b. epub files will be under ./epub/*.epub and cover files will be under ./covers/*.jpg
   c. Required Python package: scrapy.  Please check http://scrapy.org
   d. How to run the spider:
      scrapy runspider haodoo_spider.py -o haodoo.csv

2. haodoo.csv

   a. Output file generated when running the spider.
   b. This file saves the information scrapped by the spider for post processing and also for the
      comparison with future update (thus the md5 digest).
   c. It's recommended to open and edit this file with a good editor (e.g., EditPad Lite) before
      doing post-processing.
      Typical editing includes:
      i.   Sort the lines.  Note: Remember to put the header line ("author,title,epub,epub_md5,image,img_md5"
           back to the first line after sorting.
      ii.  Add the missing authors
      iii. Change full-width characters to half-width characters.

3. haodoo_pp.py

   a. The post-processing of the epub and covers folders.  The actions include:
      i.   Creation of books/ directory.
      ii.  Copy a epub file from epub/ to books/.
      iii. Add an associated cover image (if existing) from covers/ to the above epub file in books/.
      iv.  Rename the above epub file in books/ to conform with "author - title" style.
   b. How to run:
      python haodoo_pp.py haodoo.csv

4. haodoo_cover.py

   a. This script adds a cover image into an epub file.
   b. How to run:
      python haodoo_cover.py file.epub cover.jpg

## Requirements

1. Python 3.6.

2. Scrapy 1.5

3. ebooklib 0.16

## Aftermath

   a. If haodoo starts to update again, more scripts may be made by this author for automatic incremental
      update.  So plesae preserve epub/. covers/, and haodoo.csv for this possibility.
   b. Enjoy reading!


