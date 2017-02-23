import tkinter as tk 
from tkinter import filedialog as fd
import PIL
from PIL import ImageEnhance as ie
from PIL import Image as img
import os

def get_image_paths():
    #open file paths dialog for image paths
	print('find images to contrast-process')
	root = tk.Tk()
	root.withdraw()
	param ={}
	param['title'] = 'find all image files'
	param['multiple'] = True
	param['defaultextension'] = '.jpg'
	image_types = ['.bmp','.jpg','.tif','.tiff']
	param['filetypes'] = [('bitmap, jpeg, and tiff',tuple(image_types)),
	('jpeg (.jpg)',image_types[1]),
	('tif (.tif, .tiff)',tuple([t for t in image_types if 'tif' in t])),
	('bitmap (.bmp)',image_types[0])]
	param['parent'] = root
	return list(fd.askopenfilename(**param))

def get_contrast_levels():
    # dialog for finding filepath
	print('find .txt file of contrast levels')
	root = tk.Tk()
	root.withdraw()
	param = {}
	param['defaultextension'] = '.txt'
	param['filetypes'] = [('text file','.txt'),('CSV','.csv')]
	param['title'] = 'Find .txt file of contrast levels'
	param['parent'] = root
	contrast_level_path = fd.askopenfilename(**param)
    # read in .txt file with contrast levels
	with open(contrast_level_path, 'r') as f:
		contrast_levels = f.read()
	# contrast levels comes in as long string with newlines
	# split string by newlines into list
	contrast_levels = contrast_levels.split('\n')
	# change list items to floats
	contrast_levels = [float(i) for i in contrast_levels if i != ""]
	return contrast_levels

def process_images(image_paths,contrast_levels,save_dir):
    #TODO takes list of image paths, 
    #   processes them n times where n= number of contrast levels
    #   saves processed and original copies in save_dir
	save_path = save_dir + '\{0}_{1!s}{2}'
	# save_path: 
	#  {0} = filename; 
	#  {1} = contrast level flag 
	#  {2} = file extension
	for i in image_paths:
		#get filename out of filepath
		filename = os.path.basename(i)
		filename = os.path.splitext(filename)
		#open file
		tmp_img = img.open(i)
		#change bit depth
		tmp_img = tmp_img.convert(mode='RGBA',palette=256)
		##TODO## change all black pixels to transparent
		#  sample first pixel (I imagine that's top left)
		#  for all other pixels, if they match, change to alpha
		for c in contrast_levels:
			#change contrast
			tmp_img = ie.Contrast(tmp_img).enhance(c)
			#save file in new location
			print('saving...',save_path.format(filename[0],
			int(c*100),filename[1]))
			tmp_img.save(save_path.format(filename[0],int(c*100),filename[1]))
	return

if __name__ == '__main__':
    # open dialog for finding all files to process
	image_paths = get_image_paths()
	print(image_paths)
    # read in contrast levels from .txt file
	contrast_levels = get_contrast_levels()
	print(contrast_levels)
    #create new image files at each contrast level
	#	 make new folder. 
	#	if it exists, it will throw an error, but idgaf
	os.system('mkdir save_images')
	save_dir ='.\save_images'
	process_images(image_paths,contrast_levels,save_dir)

