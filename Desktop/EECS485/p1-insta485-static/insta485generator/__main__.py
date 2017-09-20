"""Build static HTML site from directory of HTML templates and plain files."""

import json
from distutils.dir_util import copy_tree
import os
import click
import jinja2


# does jinja stuff
def __do_jinja__(input_dir, template_type, context):
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(input_dir + '/templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )
    template = template_env.get_template(template_type)
    html_string = template.render(context)
    return html_string


# Reads JSON file and puts it somewhere(haven't decided)
def __read_json__(input_dir):
    with open(input_dir + '/config.json', 'r') as myfile:
        json_object = json.load(myfile)
    return json_object


# Does the writing into a new file.
def __make_files__(json_object, input_dir, verbose):
    static_folder = input_dir + '/static/'
    dest_folder = input_dir + '/html/'
    if os.path.exists(static_folder):
        copy_tree(static_folder, dest_folder)
        if verbose:
            print('Copied ' + static_folder + ' -> ' + dest_folder)
    for index in json_object:
        out_path = (input_dir + '/html' + index['url'])
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        template_html_string = __do_jinja__(input_dir, index['template'],
                                            index['context'])
        if os.path.exists(out_path + 'index.html'):
            print('Error: output directory already contains files: ')
            exit(1)
        with open(out_path + 'index.html', 'w+') as output_file:
            print(template_html_string, file=output_file, end="")
        if verbose:
            print('Rendered ' + index['template'] + ' -> ' +
                  out_path + 'index.html')


@click.command()
@click.option('-v', '--verbose', is_flag=True,
              help='Print more output.')
@click.argument('input_dir', type=click.Path(exists=True))
def main(verbose, input_dir):
    """Templated static website generator."""
    json_object = __read_json__(input_dir)
    __make_files__(json_object, input_dir, verbose)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
