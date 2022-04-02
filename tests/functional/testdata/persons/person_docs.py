from ..constants import EsIndexes

index = EsIndexes.persons.value

PERSONS = [
    {
        '_index': index,
        '_id': 'd4607082-0452-4f2f-b5b0-d1432098dba6',
        '_source': {
            'id': 'd4607082-0452-4f2f-b5b0-d1432098dba6',
            'full_name': 'Clint Morrill',
            'roles': ['actor', 'writer', 'director'],
            'films': [
                {'id': 'b5a56842-df30-4313-b22f-4c492196e6c3',
                 'title': 'Deep Inside Clint Star',
                 'imdb_rating': '7.2',
                 'role': 'actor'},
                {'id': 'b5a56842-df30-4313-b22f-4c492196e6c3',
                 'title': 'Deep Inside Clint Star',
                 'imdb_rating': '7.2',
                 'role': 'writer'},
                {'id': 'b5a56842-df30-4313-b22f-4c492196e6c3',
                 'title': 'Deep Inside Clint Star',
                 'imdb_rating': '7.2',
                 'role': 'director'}
            ]
        }
    },
    {
        '_index': index,
        '_id': '6af4d256-c82b-42b7-a785-0fc1f9aa959f',
        '_source': {
            'id': '6af4d256-c82b-42b7-a785-0fc1f9aa959f',
            'full_name': 'Valérie Kling',
            'roles': ['actor'],
            'films': [
                {'id': 'd154ff42-ee7f-4d01-972c-02ac11b3fb8f',
                 'title': 'The Butcher, the Star and the Orphan',
                 'imdb_rating': '7.3',
                 'role': 'actor'}
            ]
        }
    },
    {
        '_index': index,
        '_id': '02ef4094-0a0d-428b-94a5-1c99d74acff6',
        '_source': {
            'id': '02ef4094-0a0d-428b-94a5-1c99d74acff6',
            'full_name': 'Monthol Jira',
            'roles': ['actor'],
            'films': [
                {'id': '03b0c429-a63f-4045-a485-538a36c89264',
                 'title': 'Pop Star',
                 'imdb_rating': '6.0',
                 'role': 'actor'}
            ]
        }
    }
]
