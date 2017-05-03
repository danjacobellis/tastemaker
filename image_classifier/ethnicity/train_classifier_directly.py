import os
import imghdr

image_dir = "/home/dan/Desktop/scraped/ethnicity"
dirs = os.listdir(image_dir)
bad_files = [];
for directory in dirs:
    directory = image_dir + os.sep + directory
    files = os.listdir(directory)
    for file in files:
        file = directory + os.sep + file
        what = (imghdr.what(file))
        if what != 'jpeg':
            print(file, "is invalid")
            bad_files.append(file)

for file in bad_files:
    if os.path.isfile(file):
        os.remove(file)
        print("deleting ", file)
    else:
        print(file, " does not exist")

cmd_str = "python retrain.py"
cmd_str = cmd_str + " --image_dir " + image_dir

os.system(cmd_str)