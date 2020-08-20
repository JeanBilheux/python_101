import sys

[in_filename, out_filename] = sys.argv[1:]

def escape(character):
    code = ord(character)
    return (
        u"&#{hex_code};".format(hex_code=hex(code)[1:])
        if code > 127
        else character
    )


with open(in_filename, mode='rb') as text_file:
    contents = text_file.read().decode('utf-8')
    escaped = u''.join(
        escape(c)
        for c in contents
    )
with open(out_filename, mode='wb') as text_file:
    text_file.write(escaped.encode('utf-8'))
