
USERS = {
    'user1': {'name': 'Albert'},
    'user2': {'name': 'Berry'},
    'user3': {'name': 'Constance'},
}

ITEMS = {
    'item1': {
        'item': {
            'name': "Item Nº 1", 
            'winning': 'bid2',
            'bids': [
                'bid1','bid2'
            ]
        }
    },
    'item2': {'item': {'name': "Item Nº 2", 'winning': None, 'bids': []}}
}

BIDS = {
    'bid1' : { 
        'bid_id': 'bid1',
        'bid' : {
            'item':'item1',
            'value':500.00,
            'user': 'user1'
        }
    },
    'bid2' : { 'bid_id': 'bid2', 'bid' : {'item':'item1', 'value':1000.00, 'user': 'user2' }}
}

USERBIDS = {
    'user1' : ['bid1'],
    'user2' : ['bid2'],
    'user3' : []
}
