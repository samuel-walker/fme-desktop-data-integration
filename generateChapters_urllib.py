#!/usr/bin/env

# import required modules
import os # lib for operating system operations
import csv # lib for reading csv
import urllib # lib for reading url as file
import urllib3  # lib for reading url as file
import re # regex
import time # to get sleep function to avoid API rate limits
import wget # to download raw github images

# define variables
# update bookpath if repo changes
bookpath = "https://raw.githubusercontent.com/safesoftware/FMETraining/"
branch = "Desktop-Basic-2018/" # update for current branch/version
rawgit = "https://cdn.rawgit.com/safesoftware/FMETraining/"

# download md files from other books, create new folders if needed,
# edit their image paths, save to this book
with open('chapters.csv', 'r') as csvfile: # open csv
    next(csvfile, None) # skip header
    data = csv.reader(csvfile, delimiter=',') # define csvreader
    for row in data: # iterate on urls to generate chapters
        if row[0] == "":
            pass
        else:
            # check if dir exists, make it if not
            if not os.path.exists(row[5]):
                os.makedirs(row[5])
            if not os.path.exists(row[5] + "/Images"):
                os.makedirs(row[5] + "/Images")
            md = urllib.URLopener() # start url reader
            # download md file
            md.retrieve(bookpath + branch + row[7], row[8] + "_read.md")
            md_read = open(row[8] + "_read.md","r") # open downloaded md file
            md_write = open(row[8],"w") # new temp write md file
            for line in md_read: # iterate on md file lines
                # edit image paths [note: currently for FME training, CHANGE]
                # line = line.replace("](./", "](../" + row[7].split("/")[0] + "/")
                # edit image paths
                line = line.replace("](./", "](/" + row[5] + "/")
                if "](/" in line: # look for images by line
                    # img = line[6:-2]
                    imgsplit = line[6:-2].rsplit('/', 1)[-1] # grab image filename
                    # print img
                    # print imgsplit
                    # img = urllib.URLopener() # start url reader for img
                    # download image
                    print(rawgit + branch + row[0] + "/Images/" + imgsplit + " downloading to " + row[5] + "/Images/" + imgsplit)
                    # download using urllib, doesn't work, likely rate limited
                    urllib3.urlretrieve(rawgit + branch + row[0] + "Images/" + imgsplit, row[5] + "/Images/" + imgsplit)
                    # time.sleep(10)
                    # img_write = open(img,"w") # new temp write md file
                    # img_write.write(line) # print new line in temp file
                md_write.write(line) # print new line in temp file
            # identify and download required images
            # pat = re.compile("\]\(\.\.\/.*\)")
            # for line in md_read:
            #     img = pat.find(line)
            # print img
            md_write.close() # close temp file
            md_read.close() # close md file
            os.remove(row[8] + "_read.md")

# generate summary.md to create book structure
summary = open("SUMMARY.md","w") # open summary.md to write
summary.write("# Summary \n\n") # write summary title
with open('chapters.csv', 'r') as csvfile: # open csv
    next(csvfile, None) # skip header
    data = csv.reader(csvfile, delimiter=',') # define csvreader
    for row in data: # read rows in csv
        # camel case to spaces (not working with file exts)
        title = re.sub("([a-z])([A-Z])","\g<1> \g<2>",row[6])
        # write link in summary with proper indentation
        summary.write(2*int(row[3])*" " + "* [" + title[5:-3] + "](" + row[8] + ")\n")

summary.close() # close summary.md
