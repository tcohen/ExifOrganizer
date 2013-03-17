# finds all .jpg files in the current directory
# renames them to YYYY-MM-DD_HH-MM-SS[.####].jpg
# moves them into a subdirectory named YYYY-MM-DD,
#   creating that directory if it doesn't exist

import EXIF
import glob
import os.path
import shutil

filenames = glob.glob("*.jpg")

for filename in filenames:

    file = open(filename, 'rb')
    tags = EXIF.process_file(file, details=False, stop_tag='DateTimeOriginal')
    file.close()

    try:
        datetime = str(tags['EXIF DateTimeOriginal'])
    except:
        continue

    datetime = datetime[:4] + "-" + datetime[5:7] + "-" + datetime[8:10] + "_" + datetime[11:13] + "-" + datetime[14:16] + "-" + datetime[17:19]

    rename = datetime + ".jpg"

    if (filename != rename):

        #find a unique name
        if os.path.isfile(rename):
            index = 1
            rename = datetime + "." + str(index) + ".jpg"
            while os.path.isfile(rename):
                index = index + 1
                rename = datetime + "." + str(index) + ".jpg"

        print "* Renaming " + filename + " to " + rename
        shutil.move(filename, rename)

    else:

        print "* Skipping " + filename + " (already renamed)"

    dirname = rename[:10]

    print "* Moving " + rename + " to " + dirname
    
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    shutil.move(rename, dirname)

print "* Done"
