# Edits existing content by inserting or replacing
# an include to edit or add content. Run after downloading warehousing
# generateChapters.py.

import csv
import os
import time

# Function to read edits from CSV and write to chapter md file
def editBook(edit_file = "edits.csv"):
    with open(edit_file) as csvfile: # open csv
        next(csvfile, None) # skip header
        data = csv.reader(csvfile, delimiter=',', ) # define csvreader
        old_section = None
        for row in data: # read rows of csv to define edits
            section = row[0]
            type = row[1]
            line_num = int(row[2])
            content = row[3]
            # trying to optimize opening and closing files here
            # not really working. currently not editing at all...
            # if section from last row = section from this row
            # if first loop
            if old_section == None:
                # proceed to edit
                print("First loop, proceed.")
                pass
            # if current section = previous section
            elif section == old_section:
                # proceed to edit
                print("Same section, proceed.")
                pass
            # otherwise
            elif section != old_section:
                # close temp files, clean up
                print("New section, clean up temp files.")
                infile.close()
                outfile.close()
                os.remove(old_section)
                os.rename(old_section + "_write.md", old_section)
            else:
                print("ERROR: section variable problem")
            with open(section, "r", encoding="utf8") as infile: # open chapter to write
                with open(section + "_write.md", "w", encoding="utf8") as outfile: # open chapter to write
                    print("Editing " + section)
                    # iterate over lines in section md file
                    for index, line in enumerate(infile, start=1):
                        if index == line_num:
                            if type == "insert": # insert an include
                                print("Add line " + str(index))
                                line = "\n{% include \"../includes/" + content + ".md\" %} \n\n"
                            elif type == "replace": # replace w/ an include
                                print("Replace line " + str(index))
                                line = "{% include \"../includes/" + content + ".md\" %} \n\n"
                            elif type == "delete": # delete lines
                                print("Delete lines")
                                # deletion = row[2].split("-")
                                if index <= int(content.split("-")[1]):
                                    # delete the line
                                    print("Delete line " + str(index))
                                    line = ""
                        else:
                            print("Don't edit line " + str(index))
                        # write the line with edits from if loop above
                        outfile.write(line)
                    # store current section to compare to next section
                    old_section = section

# editBook()
