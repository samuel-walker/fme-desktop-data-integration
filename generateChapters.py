#!/usr/bin/env

# import required modules
import os # lib for operating system operations
import csv # lib for reading csv
import requests  # lib for reading url as file
import re # regex
import wget

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
            # download md file
            url = bookpath + branch + row[7] # form url
            # r = requests.get(url, allow_redirects=True) # make request
            # md_read = open(row[8] + "_read.md", 'r').write(r.text)
            if not os.path.exists(row[8]):
                wget.download(url, row[8])
            md_read = open(row[8], encoding="utf8")
            # download images
            for line in md_read: # iterate on md file lines
                # print(line)
                if "](/" in line: # look for images by line
                    imgsplit = line[6:-2].rsplit('/', 1)[-1] # grab image filename
                    print(bookpath + branch + row[0] + "/Images/" + imgsplit + " downloading to " + row[5] + "/Images/" + imgsplit)
                    # download using requests, doesn't work, likely rate limited
                    url = bookpath + branch + row[0] + "/Images/" + imgsplit # form url
                    # r = requests.get(url, allow_redirects=True) # make request
                    # open(row[5] + "/Images/" + imgsplit, 'wb').write(r.content) # write content
                    if not os.path.exists(row[5] + "/Images/" + imgsplit):
                        print(url + " to " + row[5] + "/Images/" + imgsplit)
                        wget.download(url, row[5] + "/Images/" + imgsplit)

# working wget

# url = 'https://raw.githubusercontent.com/safesoftware/FMETraining/Desktop-Basic-2018/DesktopBasic1Basics/Images/Img1.000.TranslationIntro.png'
# wget.download(url, 'C:/Users/swalker/Documents/GitHub/fme-desktop-data-integration/test.png')

# url = "https://raw.githubusercontent.com/safesoftware/FMETraining/Desktop-Basic-2018/DesktopBasic1Basics/Images/Img1.001.WhatIsFME.png"
# wget.download(url, "Integration1Lecture/Images/Img1.001.WhatIsFME.png")

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
