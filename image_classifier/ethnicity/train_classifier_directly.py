import os
import imghdr

image_dir = "../../scrapers/ethnicity/google_dl"
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

output_graph = os.getcwd() + os.sep + 'output_graph.pb'
output_labels = os.getcwd() + os.sep + 'output_labels.txt'
summaries_dir = os.getcwd() + os.sep + 'retrain_logs'
bottleneck_dir = os.getcwd() + os.sep + 'bottleneck'

cmd_str = "python retrain.py"
cmd_str = cmd_str + " --image_dir " + image_dir
cmd_str = cmd_str + " --output_graph " + output_graph
cmd_str = cmd_str + " --output_labels " + output_labels
cmd_str = cmd_str + " --summaries_dir " + summaries_dir
cmd_str = cmd_str + " --bottleneck_dir " + bottleneck_dir

os.system(cmd_str)
