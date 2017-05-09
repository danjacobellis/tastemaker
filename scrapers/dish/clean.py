import imghdr
import os

WORK_DIR = './google_dl'

folders = os.listdir(WORK_DIR)
print(folders)

for folder in folders:
	images = os.listdir(WORK_DIR + '/' + folder)
	print(folder)
	print(images)
	for image in images:
		what = imghdr.what(WORK_DIR + '/' + folder + '/' + image)
		if what != 'jpeg':
			print(folder + '/' + image + ' is invalid: ' + str(what))
			os.remove(WORK_DIR + '/' + folder + '/' + image)
