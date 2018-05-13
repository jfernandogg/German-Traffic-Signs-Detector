#!/usr/bin/env python
import click
import urllib.request
import zipfile

@click.group()
def cli():
	pass
	
@cli.command()
def download():
	click.echo('downloading train dataset')
	remote = r"http://benchmark.ini.rub.de/Dataset_GTSDB/FullIJCNN2013.zip"
	local = r"images\\full.zip"
	with urllib.request.urlopen(remote) as response, open(local, 'wb') as out_file:
		data = response.read() # a `bytes` object
		out_file.write(data)
	zip_ref = zipfile.ZipFile(local, 'r')
	zip_ref.extractall("images\\")
	zip_ref.close()

if __name__ == '__main__':
	cli()
