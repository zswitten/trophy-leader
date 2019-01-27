import requests
import json
import ast
from collections import Counter

base_url = 'https://draftsim.com/draft-log.php?id='

def get_draft(i):
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

def get_cardset(mtgset):
    base_url = 'http://mtgjson.com/json/'
    url = base_url + mtgset + '.json'
    result = requests.get(url)
    cards = json.loads(result.text)
    cardnames = set([c['name'].replace(' ', '_') for c in cards['cards']])
    return cardnames

def verify_drafts(drafts, mtgset):
    cardset = get_cardset(mtgset)
    verified_drafts = [d for d in drafts if draft_contains_valid_cards(d, cardset)]
    return verified_drafts

def draft_contains_valid_cards(draft, cardset):
    pickset = set()
    for picklist in draft['picks']:
        for card in picklist:
            pickset.add(card)
    mistaken_cards = []
    for card in pickset:
        if card not in cardset:
            mistaken_cards.append(card)
    import pdb; pdb.set_trace()
    return len(mistaken_cards) < 20

def get_cards(drafts):
    cards = Counter()
    for draft in drafts:
        for player in draft['picks']:
            for card in player:
                cards[card] += 1
    return cards

def parse_draft_to_flooey_format(draft, cardset):
    players = draft['picks']
    cards_per_pack = int(len(players[0]) / 3)
    packs = []
    for pack_index in range(3):
        choices = []
        for pick_index in range(cards_per_pack):
            options = []
            idx = pick_index
            while idx < cards_per_pack:
                options.append(players[(idx - pick_index) % 8][idx])
                idx += 1
            choices.append(options)
        packs.append(choices)
    return packs
