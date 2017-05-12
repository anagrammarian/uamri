#!/usr/bin/python

import os

def spaceToUnderscore(filename):

    new_file_name = filename.replace(" ", "_")
    os.rename(filename, new_file_name)

    return new_file_name