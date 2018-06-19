#! /usr/bin/python
'''
Usage        : haodoo_cover.py file.epub cover.jpg
-h           : this help
file.epub    : Haodoo epub file to be added a cover image
cover.jpg    : the cover image

This program takes an Haodoo epub file and a jpg file (book's cover)
and insert it into the epub file (becomes OEBPS/cover.jpg) while
modifying the OEBPS/content.opf file to use the image as the cover.

Example:

$ haodoo_cover.py 172a.epub cover.jpg
'''

import sys, getopt, os, shutil
from ebooklib import epub

def usage():
    ''' Display command usage.''' 
    sys.stderr.write(__doc__)
    sys.stderr.flush()

def check_file(fname, ext):
    if not fname.lower().endswith(ext):
        sys.stderr.write(ext.upper() + ": " + fname + " does not have a correct extension!\n")
        sys.exit(2)
    if not os.path.isfile(fname):
        sys.stderr.write("File " + fname + " does not exist!\n")
        sys.exit(2)
        
def main(argv):
    # getopt
    try:                                
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    # handle options
    for opt, optarg in opts:
        if opt == '-h':
            usage()                     
            sys.exit()
    if len(args) == 2:
        epub_fname = args[0]
        jpg_fname = args[1]
        check_file(epub_fname, ".epub")
        check_file(jpg_fname, ".jpg")
    else:
        usage()
        sys.exit()
    book = epub.read_epub(epub_fname)
    f = open(jpg_fname, 'rb')
    content = f.read()
    f.close()
    book.set_cover('cover.jpg', content)
    epub.write_epub(epub_fname, book, {})

if __name__ == "__main__":
    main(sys.argv[1:])
