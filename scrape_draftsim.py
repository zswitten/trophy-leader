import requests
import json
import ast
from collections import Counter

base_url = 'https://draftsim.com/draft-log.php?id='

def get_draft(i):
    # Call this for all i 
    try:
        result = requests.get(make_url(i))
        text = result.text
        s = get_draft_string(text)
        dl = get_draft_list(s)
        draft_format = get_format(text)
        return {'picks': dl, 'format': draft_format}
    except:
        return None

def get_draft_list(draft_string):
    lst = ast.literal_eval(draft_string)
    decks = [d.replace(',_', '_').split(',') for d in lst]
    return decks

def get_draft_string(content):
    start_string = '\nvar send_draft = '
    start_index = content.index(start_string) + len(start_string)
    end_index = content.index(';\nvar send_format = ')
    return content[start_index:end_index]

def get_format(content):
    start_string = '\nvar send_format = '
    start_index = content.index(start_string) + len(start_string)
    end_index = content.index(';\n\nreconstruct')
    return content[start_index+1:end_index-1]

def make_url(i):
    return base_url + str(i)

def save_drafts(draft_min, draft_max):
    for i in range(draft_min, draft_max):
        draft = get_draft(i)
        json.dump(draft, open('draft_'+str(i), 'w'))
