from ..constants import EsIndexes

index = EsIndexes.movies.value


FILMS = [
    {
        '_index': index,
        '_id': 'b5a56842-df30-4313-b22f-4c492196e6c3',
        '_source': {
            'id': 'b5a56842-df30-4313-b22f-4c492196e6c3',
            'imdb_rating': 7.2,
            'genres': [{'id': '6d141ad2-d407-4252-bda4-95590aaf062a', 'name': 'Documentary'}],
            'title': 'Deep Inside Clint Star',
            'description': 'Test case',
            'directors_names': ['Clint Morrill'],
            'actors_names': ['Clint Morrill'],
            'writers_names': ['Clint Morrill'],
            'directors': [{'id': 'd4607082-0452-4f2f-b5b0-d1432098dba6', 'name': 'Clint Morrill'}],
            'actors': [{'id': 'd4607082-0452-4f2f-b5b0-d1432098dba6', 'name': 'Clint Morrill'}],
            'writers': [{'id': 'd4607082-0452-4f2f-b5b0-d1432098dba6', 'name': 'Clint Morrill'}]
        }
    },
    {
        '_index': index,
        '_id': 'd154ff42-ee7f-4d01-972c-02ac11b3fb8f',
        '_source': {
            'id': 'd154ff42-ee7f-4d01-972c-02ac11b3fb8f',
            'imdb_rating': 7.3,
            'genres': [{'id': '5373d043-3f41-4ea8-9947-4b746c601bbd', 'name': 'Comedy'}],
            'title': 'The Butcher, the Star and the Orphan',
            'description': None,
            'directors_names': ['Jérôme Savary'],
            'actors_names': ['Valérie Kling', 'Elisabeth Mortensen', 'Rosa Fumetto', 'Gérard Croce'],
            'writers_names': ['Roland Topor', 'Jérôme Savary', 'Jean Bach'],
            'directors': [{'id': 'cf30a819-5c1d-4198-b776-bdd16d43aefc', 'name': 'Jérôme Savary'}],
            'actors': [
                {'id': '6af4d256-c82b-42b7-a785-0fc1f9aa959f', 'name': 'Valérie Kling'},
                {'id': '02835024-90fe-4f70-b998-9896aa9b11c9', 'name': 'Elisabeth Mortensen'},
                {'id': '388bb96d-6e06-4f33-ba80-73aac90062b4', 'name': 'Rosa Fumetto'},
                {'id': 'dcb8e052-e3a4-4430-bd5e-fdb0bee3b5c6', 'name': 'Gérard Croce'}
            ],
            'writers': [
                {'id': 'a89c8051-cb6e-43b1-8824-c2b3bbe50a13', 'name': 'Roland Topor'},
                {'id': 'cf30a819-5c1d-4198-b776-bdd16d43aefc', 'name': 'Jérôme Savary'},
                {'id': '7567d884-46e4-4e19-89d4-73e54951dc80', 'name': 'Jean Bach'}
            ]
        }
    },
    {
        '_index': index,
        '_id': '03b0c429-a63f-4045-a485-538a36c89264',
        '_source': {
            'id': '03b0c429-a63f-4045-a485-538a36c89264',
            'imdb_rating': 6.0,
            'genres': [{'id': '526769d7-df18-4661-9aa6-49ed24e9dfd8', 'name': 'Thriller'}],
            'title': 'Pop Star',
            'description': 'When a former teen idol succeeds at a major comeback'
                           ' he has a violent meltdown in his penthouse'
                           ' suite at a fashionable hotel.',
            'directors_names': ['Robert La Force'],
            'actors_names': ['Bongkoj Khongmalai', 'Monthol Jira', 'Nirut Sirichanya'],
            'writers_names': ['Robert La Force'],
            'directors': [{'id': 'cf50fdfa-54d7-4d0c-9463-a5bb892d490d', 'name': 'Robert La Force'}],
            'actors': [
                {'id': '21778021-0ec3-4172-a85a-305dff51ab6e', 'name': 'Bongkoj Khongmalai'},
                {'id': '02ef4094-0a0d-428b-94a5-1c99d74acff6', 'name': 'Monthol Jira'},
                {'id': '293ab291-2bba-4204-b5ba-48043548357c', 'name': 'Nirut Sirichanya'}
            ],
            'writers': [{'id': 'cf50fdfa-54d7-4d0c-9463-a5bb892d490d', 'name': 'Robert La Force'}]
        }
    }
]
