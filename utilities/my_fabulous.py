# example of use of fabulous
# only works with python 2.7

# fabulous is a python library (and command line tools) desinged to make the output of terminal application look Fabulous

import fabulous
from fabulous.color import bold, magenta, highlight_red

print("print(bold(magenta(\"Hellow world\")) => " + bold(magenta("Hellow world")))
print("print(highlight_red('Danger will robinson') => " + highlight_red('Dange will robinson'))
print("bold('hello') => " + bold('hello'))


from fabulous import text
print(text.Text("fabulous!", color='#0099ff', shadow=True, skew=5))

from fabulous.color import fg256, bg256
print(fg256('#F0F', 'hello world'))
print(bg256('#F0F', 'hello world'))
