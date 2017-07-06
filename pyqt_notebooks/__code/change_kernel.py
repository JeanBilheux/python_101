import click
import os
import json

@click.command()
@click.argument('notebook', type=click.Path(exists=True))
@click.option('--kernel-display-name', default='imaging', help='display_name of new kernel')
@click.option('--kernel-name', default='imaging', help='name of new kernel')
def run(notebook, kernel_display_name, kernel_name):

	# load json
	json_data = open(notebook)
	data = json.load(json_data)

	json_data.close()

	# change kernel values
	data['metadata']['kernelspec']['name'] = kernel_name
	data['metadata']['kernelspec']['display_name'] = kernel_display_name

	# replace notebook with new json
	with open(notebook, 'w') as f:
		json_text = json.dumps(data, indent=2)
		f.write("{}\n".format(json_text))

if __name__ == '__main__':
	run()

