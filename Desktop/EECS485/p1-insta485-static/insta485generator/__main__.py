"""Build static HTML site from directory of HTML templates and plain files."""

import click
import jinja2
import json
import os
import errno


#Reads JSON file and puts it somewhere(haven't decided)
def readJSON(input_dir):
    with open(input_dir + '/config.json', 'r') as myfile:
        jsonObject=json.load(myfile)
    return jsonObject
      

    

#Does the writing into a new file.
def newFiles(jsonObject, input_dir):    #make list of urls
    urls = [i['url'] for i in jsonObject]
    for url in urls:
        outPath = (input_dir + '/html' + url + 'index.html')
        #if not os.path.exists(os.path.dirname(outPath)):
         #   os.makedirs(os.path.dirname(input_dir + '/html'))

        with open(outPath, 'w+') as outputFile:
            print('hello', file=outputFile, end="")
        #print(outPath)


@click.command()
@click.option('-v','-verbose', is_flag=True, help='Print more output.(still under construction)')
@click.argument('INPUT_DIR', type=click.Path())
def main(verbose, input_dir):
    """Templated static website generator."""
    json = readJSON(input_dir)
    newFiles(json, input_dir)
    


if __name__ == "__main__":
    main()