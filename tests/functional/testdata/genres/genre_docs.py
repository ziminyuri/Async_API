from ..constants import EsIndexes

index = EsIndexes.genres.value

GENRES = [
    {
        '_index': index,
        '_id': '31cabbb5-6389-45c6-9b48-f7f173f6c40f',
        '_source': {
            'id': '31cabbb5-6389-45c6-9b48-f7f173f6c40f',
            'name': 'Talk-Show',
            'films': [
                {
                    'id': '83af8d01-580a-462e-8c96-2171385935cc',
                    'title': 'Jimmy Kimmel Live\'s All-Star Salute to Jimmy Kimmel Live!',
                    'imdb_rating': '7.5'
                },
                {
                    'id': '75ded9f4-1894-4996-8945-0023fe055bc0',
                    'title': 'The Star Jones Reynolds Report',
                    'imdb_rating': '4.4'
                },
                {
                    'id': 'f9ca2c1f-dc35-471d-ad65-d9be49735210',
                    'title': 'Super Star',
                    'imdb_rating': '3.9'
                },
                {
                    'id': '9db186d9-a813-4d86-8e3e-d023cc9926c8',
                    'title': 'Star Wars: The Last Jedi Cast Live Q&A',
                    'imdb_rating': '3.9'
                },
                {
                    'id': '5c568226-b6cb-4c04-b9a8-24117ec85bb2',
                    'title': 'Top star magazín',
                    'imdb_rating': '2.9'
                },
                {
                    'id': '46143f45-25f5-4df9-8927-b5f7fa92e1a3',
                    'title': 'The Star Wars Show',
                    'imdb_rating': '8.0'
                }
            ]
        },
    },

    {
        '_index': index,
        '_id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
        '_source': {
            'id': '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
            'name': 'Action',
            'films': [
                {
                    'id': '25fd2547-d006-49b2-b673-e6dae7f45dad',
                    'title': 'Fist of the North Star: The Souther Saga',
                    'imdb_rating': '7.3'
                },
                {
                    'id': '8c6fc75b-0004-41c5-9e9b-36ffff653f55',
                    'title': 'Star Trek: Deception',
                    'imdb_rating': '5.2'
                },
                {
                    'id': '3bdae84f-9a04-4b04-9f7c-c05582d529e5',
                    'title': 'Star Wars: Qui-Gon Jinn III',
                    'imdb_rating': '7.2'
                },
            ]
        }
    },

    {
        '_id': '6a0a479b-cfec-41ac-b520-41b2b007b611',
        '_index': index,
        '_source': {
            'id': '6a0a479b-cfec-41ac-b520-41b2b007b611',
            'name': 'Animation',
            'films': [
                {
                    'id': '25fd2547-d006-49b2-b673-e6dae7f45dad',
                    'title': 'Fist of the North Star: The Souther Saga',
                    'imdb_rating': '7.3'
                },
                {
                    'id': '49c79cbf-5cf5-45df-95ef-89368152dc8d',
                    'title': 'Star Trek: Pinball',
                    'imdb_rating': '6.3'
                },
                {
                    'id': '6894afe9-1d20-4c73-a518-05f461b04237',
                    'title': 'Phantasy Star Online Version 2',
                    'imdb_rating': '7.8'
                },
                {
                    'id': '8f128d84-dd99-4d0d-a9c8-df11f87ac133',
                    'title': 'All-Star American Destiny Trek',
                    'imdb_rating': '4.6'
                }
            ]
        }
    }
]
