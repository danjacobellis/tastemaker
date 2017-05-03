import os

image_dir = "/home/dan/Desktop/scraped/ethnicity"

bad_files = [image_dir+"/hungarian/30.jpg",
             image_dir+"/dairy/5.jpg",
             image_dir+"/dairy/80.jpg",
             image_dir+"/dairy/41.jpg",
             image_dir+"/dairy/30.jpg",
             image_dir+"/dairy/61.jpg",
             image_dir+"/dairy/18.jpg",
             image_dir+"/dairy/60.jpg",
             image_dir+"/dairy/31.jpg",
             image_dir+"/norwegian/68.jpg",
             image_dir+"/norwegian/13.jpg",
             image_dir+"/norwegian/46.jpg",
             image_dir+"/norwegian/79.jpg",
             image_dir+"/norwegian/37.jpg",
             image_dir+"/norwegian/43.jpg",
             image_dir+"/norwegian/78.jpg",
             image_dir+"/appetizers/1.jpg",
             image_dir+"/appetizers/44.jpg",
             image_dir+"/appetizers/84.jpg",
             image_dir+"/appetizers/99.jpg",
             image_dir+"/american/20.jpg",
             image_dir+"/american/32.jpg",
             image_dir+"/american/75.jpg",
             image_dir+"/southern/37.jpg",
             image_dir+"/southern/36.jpg",
             image_dir+"/southern/78.jpg",
             image_dir+"/african/86.jpg",]

for file in bad_files:
    if os.path.isfile(file):
        os.remove(file)
        print("deleting ", file)
    else:
        print(file, " does not exist")

cmd_str = "python retrain.py"
cmd_str = cmd_str + " --image_dir " + image_dir

os.system(cmd_str)