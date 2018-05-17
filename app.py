#!/usr/bin/env python
import click
import urllib.request
import zipfile
import os
import shutil
import random
import glob

@click.group()
def cli():
	pass
	
@cli.command()
def download():
	#this function downloads the dataset and setup the train and test directories
	remote = r"http://benchmark.ini.rub.de/Dataset_GTSDB/FullIJCNN2013.zip"
	local = r"images"+os.path.sep+"full.zip"
	#only download if full.zip is not present
	if not (os.path.isfile(local) ):
		with urllib.request.urlopen(remote) as response, open(local, 'wb') as out_file:
			click.echo('downloading full dataset')
			data = response.read() # a `bytes` object
			out_file.write(data)
			print(".")
	#now we decompress full.zip
	click.echo("found train and test decompressing")
	zip_ref = zipfile.ZipFile(local, 'r')
	zip_ref.extractall("images"+os.path.sep)
	zip_ref.close()
	#now lets clean and assamble the train and test directories
	if os.path.isdir(os.path.join("images","train")):
		shutil.rmtree(os.path.join("images","train"))
	os.rename(os.path.join("images","FullIJCNN2013"), os.path.join("images","train"))
	if os.path.isdir( os.path.join("images","test" ) ):
		shutil.rmtree(os.path.join("images","test"))
		os.makedirs(os.path.join("images","test"))
	else:
		os.makedirs(os.path.join("images","test"))
	#test directory needs to have the 20% of files
	files = []
	folders = []
	root = os.path.join("images","train")
	#remove files for object location
	filelist = glob.glob(os.path.join(root, "*.ppm"))
	for f in filelist:
		os.remove(f)
	labels = os.listdir(root)
	labels = labels[:43]
	for (path, dirnames, filenames) in os.walk(root):
		for name in filenames:
			pathc = path.split(os.path.sep)
			cdir = pathc[len(pathc)-1]
		folders.extend(os.path.join(path, name) for name in dirnames)
		files.extend(os.path.join(path, name) for name in filenames)
	files = files[2:]
	p2 = int( len(files)*0.2 ) #20% of files
	idxh = []
	for i in range(0,p2):
		ridx = int(random.uniform(0,len(files)))
		while idxh.__contains__(ridx):
			ridx = int(random.uniform(0,len(files)))
		idxh.append(ridx)
		cf = files[ridx] #choose a random file for test
		cfa = cf.split(os.path.sep)
		nfn = cfa[-2]+"-"+cfa[-1] #create a new name for test files which is label-filename.ppm
		print ("moviendo "+cf+" a "+os.path.join("images","test",nfn))
		shutil.move(cf, os.path.join("images","test",nfn))

if __name__ == '__main__':
	cli()
