# this script return how many tag named "group" are in this xml file

import os
from xml.dom import minidom


file = 'data/nomad.xml'
assert os.path.exists(file)

xmldoc = minidom.parse(file)
itemlist = xmldoc.getElementsByTagName('group')
print(len(itemlist))