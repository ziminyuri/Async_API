import pytest

from ..testdata.constants import GENRE_ENDPOINT, EsIndexes
from ..testdata.genres import GENRE_INDEX, GENRES
from ..utils import delete_es_index, populate_es


class TestGenre:
    genre = GENRES[0]['_source']

    @pytest.mark.asyncio
    async def test_get_genres(self, make_get_request):
        """ Получения жанров """
        response = await make_get_request(f'{GENRE_ENDPOINT}')

        assert response.status == 200
        assert len(response.body) == 3

        assert all([self.genre[key] == value for key, value in response.body[0].items()])

    @pytest.mark.asyncio
    async def test_get_genre_by_id_success(self, make_get_request):
        """ Получение жанра по id """
        response = await make_get_request(f'{GENRE_ENDPOINT}/{self.genre["id"]}')
        assert response.status == 200
        assert len(response.body) == 3

        assert all([self.genre[key] == value
                    for key, value in response.body.items()])

    @pytest.mark.asyncio
    async def test_get_genre_by_id_404(self, make_get_request):
        """ Получение жанра по id, жанр не сущетсвует """
        response = await make_get_request(f'{GENRE_ENDPOINT}/75ded9f4-1894-4996-8945-0023fe055bc0')
        assert response.status == 404

    @pytest.mark.asyncio
    async def test_get_genres_with_pagination(self, make_get_request):
        """ Получение жанров с пагинауией """
        first_page = await make_get_request(f'{GENRE_ENDPOINT}?page=1&size=2')
        assert first_page.status == 200
        assert len(first_page.body) == 2

        second_page = await make_get_request(f'{GENRE_ENDPOINT}?page=2&size=2')
        assert second_page.status == 200
        assert len(second_page.body) == 1

        assert all([second_page.body[0]['id'] != result['id']
                    for result in first_page.body])

    @pytest.mark.asyncio
    async def test_search_genres_by_title(self, make_get_request):
        """ Поиск жанра по названию"""
        query = self.genre["name"].split(" ")[0]
        url = f'{GENRE_ENDPOINT}/?query={query}'
        response = await make_get_request(url)

        assert response.status == 200
        assert len(response.body) == 1
        assert response.body[0]['name'] == self.genre['name']

    @pytest.mark.asyncio
    async def test_get_genre_from_cache(self, make_get_request, es_client):
        """ Получения жанра из кеша """
        es_response = await make_get_request(f'{GENRE_ENDPOINT}/{self.genre["id"]}')

        assert es_response.status == 200
        assert len(es_response.body) == 3

        await delete_es_index(es_client, EsIndexes.genres.value)

        redis_response = await make_get_request(f'{GENRE_ENDPOINT}/{self.genre["id"]}')

        assert redis_response.status == 200
        assert len(redis_response.body) == 3
        assert es_response == redis_response

        await populate_es(es_client, EsIndexes.genres.value, GENRE_INDEX, GENRES)

    @pytest.mark.asyncio
    async def test_get_genres_from_cache(self, make_get_request, es_client):
        """ Получение всех жанров из кеша """
        es_response = await make_get_request(f'{GENRE_ENDPOINT}')

        assert es_response.status == 200
        assert len(es_response.body) == 3

        await delete_es_index(es_client, EsIndexes.genres.value)

        redis_response = await make_get_request(f'{GENRE_ENDPOINT}')

        assert redis_response.status == 200
        assert len(redis_response.body) == 3
        assert es_response == redis_response

        await populate_es(es_client, EsIndexes.genres.value, GENRE_INDEX, GENRES)

    @pytest.mark.asyncio
    async def test_get_genres_asc_sort(self, make_get_request):
        """ Все жанры, отсортированные по имени asc """
        sorted_genres = sorted(GENRES, key=lambda genre: genre['_source']['name'])
        response = await make_get_request(f'{GENRE_ENDPOINT}?sort=name')

        assert response.status == 200
        assert len(response.body) == 3
        assert response.body[0]['name'] == sorted_genres[0]['_source']['name']

    @pytest.mark.asyncio
    async def test_get_genres_desc_sort(self, make_get_request):
        """ Все жанры, отсортированные по имени desc """
        sorted_genres = sorted(GENRES, key=lambda genre: genre['_source']['name'],
                               reverse=True)
        response = await make_get_request(f'{GENRE_ENDPOINT}?sort=-name')

        assert response.status == 200
        assert len(response.body) == 3
        assert response.body[0]['name'] == sorted_genres[0]['_source']['name']
