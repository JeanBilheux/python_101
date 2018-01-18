import os
import sys
import re

list_of_languages = ['en', 'es', 'fr']

def read_ascii(filename=''):
    '''return contain of an ascii file'''
    f = open(filename, 'r')
    text = f.read()
    f.close()
    text_array = text.split('\n')
    return text_array

def write_ascii(filename='', html_text=[]):
    f = open(filename, 'w')
    for _text in html_text:
        f.write(_text + '\n')
    f.close()

def fix_hugo():

    # where to look for
    input_path = sys.argv[1]

    for _language in list_of_languages:

        print("** Working with language: {}".format(_language))
        top_folder = os.path.join(input_path, _language)

        # list all html files
        for root, directories, filenames in os.walk(top_folder):
            for filename in filenames:
                if ".html" in filename:
                    full_filename = os.path.join(root, filename)
                    print("-> Looking at file: {}".format(full_filename))

                    html_text = read_ascii(filename=full_filename)
                    new_html_text = []

                    string_to_find = r'href="{}/'.format(_language)
                    new_string = 'href="/{}/'.format(_language)

                    for _index, _line in enumerate(html_text):
                        _new_line = re.sub(string_to_find, new_string, _line)
                        new_html_text.append(_new_line)
                        if not(_new_line == _line):
                            print("   Replaced line #{}".format(_index))

                    write_ascii(filename=full_filename, html_text=new_html_text)

if __name__ == '__main__':

    fix_hugo()


