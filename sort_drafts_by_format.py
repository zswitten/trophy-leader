import os
import json

os.system('mkdir drafts')

fmts = set()

for file in os.listdir('../drafts'):
    print(file)
    with open('../drafts/' + file, 'r') as draft_file:
        draft_string = draft_file.read()
        draft_string = draft_string.replace("'", '"')
        for c in ['s', '-', '_']:
            draft_string = draft_string.replace('"' + c, c)
        draft = json.loads(draft_string)
        fmt = draft['format']
        if fmt not in fmts:
            os.system('mkdir drafts/%s' % fmt)
            fmts.add(fmt)
        os.system('mv ../drafts/%s drafts/%s/%s' % (file, fmt, file))
