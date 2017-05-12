#!/usr/bin/python

import sys
import os

#def webpage(directory, url):
def webpage(directory, link):
    print('This is link in webpage:'+link)
#    import change_index_url

#   change_index_url.changeindex(url)

    os.chdir(directory)

#    print('Now creating the webpage html files')

 #   import copying_directories

#    copying_directories.copying_directories()



#    print('Now checking for .xml files to create tables for')

#   import ProtParser

#    ProtParser.runParser()

    print('Now adding the links to the index file')

    import directoryURLlink

#    directoryURLlink.runCreateLinks(url)
    directoryURLlink.runCreateLinks(link)

    print('Webpage complete')

    return