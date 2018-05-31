# Edits existing content by inserting or replacing
# an include to edit or add content. Run after downloading warehousing
# generateChapters.py.

import csv
import os

# Function to read edits from CSV and write to chapter md file
def editBook(edit_file = "edits.csv"):
    with open(edit_file) as csvfile: # open csv
        next(csvfile, None) # skip header
        data = csv.reader(csvfile, delimiter=',') # define csvreader
        for row in data: # iterate on urls to generate chapters
            section = row[0]
            type = row[1]
            line_num = int(row[2])
            include = row[3]
            with open(section, "r", encoding="utf8") as infile: # open chapter to write
                with open(section + "_write.md", "w", encoding="utf8") as outfile: # open chapter to write
                    for index, line in enumerate(infile, start=1):
                        if index == line_num:
                            if type == "include": # includes just add an include
                                print("Add line " + str(index))
                                line = "\n{% include \"../includes/" + include + ".md\" %} \n\n"
                            elif type == "replace": # replace replace lines
                                if include == "":
                                    print("Delete line")
                                    line = "\n"
                                else:
                                    print("Replace line " + str(index))
                                    line = line.replace(line,"{% include \"../includes/" + include + ".md\" %} \n\n")
                        else:
                            print("Don't edit line " + str(index))
                        outfile.write(line)
                    infile.close()
                    outfile.close()
            os.remove(section)
            os.rename(section + "_write.md", section)
