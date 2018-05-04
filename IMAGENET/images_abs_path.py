#! usr/bin/python

import os

directory = "/Users/rahul/Big_data/ass2/part2/ufo_images_final/"
file = open("absolute_paths.txt", "a+")

for filename in os.listdir(directory):
    s = directory+str(filename)
    file.write(s+'\n')