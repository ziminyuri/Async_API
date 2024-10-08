from http import HTTPStatus

import pytest

from src.dictionary import errors_dict

from ..testdata.constants import FILMS_ENDPOINT, EsIndexes
from ..testdata.films import FILM_INDEX, FILMS
from ..testdata.parser import filter_by_field, filter_films_by_genre, paginate
from ..utils import delete_es_index, populate_es


class TestFilm:
    film = FILMS[0]['_source']

    @pytest.mark.asyncio
    async def test_film_detail_success(self, make_get_request):
        """Тест для получения фильма по id"""
        response = await make_get_request(f'{FILMS_ENDPOINT}/{self.film["id"]}')
        assert response.status == HTTPStatus.OK
        assert all([self.film[key] == value
                    for key, value in response.body.items()])

    @pytest.mark.asyncio
    async def test_film_detail_not_found(self, make_get_request):
        """Тест для проверки 404 если фильм не найден"""
        response = await make_get_request(f'{FILMS_ENDPOINT}/1234567')

        assert response.status == HTTPStatus.NOT_FOUND

    @pytest.mark.asyncio
    async def test_films_success(self, make_get_request):
        """Тест для получения всех фильмов"""
        response = await make_get_request(f'{FILMS_ENDPOINT}')

        assert response.status == HTTPStatus.OK
        assert len(response.body) == len(FILMS)

        assert all([self.film[key] == value for key, value in response.body[0].items()])

    @pytest.mark.asyncio
    async def test_films_asc_sort(self, make_get_request):
        """Тест для получения всех фильмов с учетом сортировки asc"""
        min_rating = min(FILMS, key=lambda film: film['_source']['imdb_rating'])
        response = await make_get_request(f'{FILMS_ENDPOINT}?sort=imdb_rating')

        assert response.status == HTTPStatus.OK
        assert len(response.body) == len(FILMS)
        assert response.body[0]['imdb_rating'] == min_rating['_source']['imdb_rating']

    @pytest.mark.asyncio
    async def test_films_desc_sort(self, make_get_request):
        """Тест для получения всех фильмов с учетом сортировки desc"""
        max_rating = max(FILMS, key=lambda film: film['_source']['imdb_rating'])
        response = await make_get_request(f'{FILMS_ENDPOINT}?sort=-imdb_rating')

        assert response.status == HTTPStatus.OK
        assert len(response.body) == len(FILMS)
        assert response.body[0]['imdb_rating'] == max_rating['_source']['imdb_rating']

    @pytest.mark.asyncio
    async def test_films_genre_filter(self, make_get_request):
        """Тест для получения всех фильмов по жанру"""
        film_genre = self.film['genres'][0]
        response = await make_get_request(f'{FILMS_ENDPOINT}?genre={film_genre["id"]}')

        assert response.status == HTTPStatus.OK
        assert len(response.body) == len(filter_films_by_genre(FILMS, film_genre['id']))
        assert all([self.film[key] == value for key, value in response.body[0].items()])

    @pytest.mark.asyncio
    async def test_films_genre_not_exist(self, make_get_request):
        """Тест для проверки 404 если жанра нет"""
        response = await make_get_request(f'{FILMS_ENDPOINT}?genre=test')

        assert response.status == HTTPStatus.NOT_FOUND
        assert response.body['detail'] == errors_dict['404_films']

    @pytest.mark.asyncio
    async def test_films_pagination(self, make_get_request):
        """Тест для получения фильмов с учетом пагинауии"""
        page = 1
        size = 2
        first_page = await make_get_request(f'{FILMS_ENDPOINT}?page={page}&size={size}')
        assert first_page.status == HTTPStatus.OK
        assert len(first_page.body) == len(paginate(FILMS, page, size))

        page = 2
        second_page = await make_get_request(f'{FILMS_ENDPOINT}?page={page}&size={size}')
        assert second_page.status == HTTPStatus.OK
        assert len(second_page.body) == len(paginate(FILMS, page, size))

        assert all([second_page.body[0]['id'] != result['id']
                    for result in first_page.body])

    @pytest.mark.asyncio
    async def test_films_not_valid_pagination(self, make_get_request):
        """Тест для проверки 422 если параметры для пагинации не имеют числовой тип"""
        response = await make_get_request(f'{FILMS_ENDPOINT}?page=one&size=two')

        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.body['detail'][0]['msg'] == 'value is not a valid integer'

    @pytest.mark.asyncio
    async def test_films_search_by_title(self, make_get_request):
        """Тест для поиска фильмов по названию"""
        query = self.film['title'].split(' ')[0]
        url = f'{FILMS_ENDPOINT}/search/?query={query}'
        response = await make_get_request(url)

        assert response.status == HTTPStatus.OK
        assert len(response.body) == len(filter_by_field(FILMS, 'title', query))
        assert response.body[0]['title'] == self.film['title']

    @pytest.mark.asyncio
    async def test_films_search_by_description(self, make_get_request):
        """Тест для поиска фильмов по описанию"""
        query = self.film['description'].split(' ')[0]
        url = f'{FILMS_ENDPOINT}/search/?query={query}'
        response = await make_get_request(url)

        assert response.status == HTTPStatus.OK
        assert len(response.body) == len(filter_by_field(FILMS, 'description', query))
        assert response.body[0]['title'] == self.film['title']

    @pytest.mark.asyncio
    async def test_films_search_by_not_exist(self, make_get_request):
        """Тест для проверки 404 ошибки если ничего не найдено"""
        url = f'{FILMS_ENDPOINT}/search/?query=not_exist_text'
        response = await make_get_request(url)

        assert response.status == HTTPStatus.NOT_FOUND
        assert response.body['detail'] == errors_dict['404_films']

    @pytest.mark.asyncio
    async def test_film_detail_redis(self, make_get_request, es_client):
        """Тест для получения данных из Redis при повторном запросе конкретного фильма"""
        es_response = await make_get_request(f'{FILMS_ENDPOINT}/{self.film["id"]}')

        assert es_response.status == HTTPStatus.OK
        assert all([self.film[key] == value
                    for key, value in es_response.body.items()])

        await delete_es_index(es_client, EsIndexes.movies.value)

        redis_response = await make_get_request(f'{FILMS_ENDPOINT}/{self.film["id"]}')

        assert redis_response.status == HTTPStatus.OK
        assert es_response == redis_response

        await populate_es(es_client,
                          EsIndexes.movies.value,
                          FILM_INDEX,
                          FILMS)

    @pytest.mark.asyncio
    async def test_films_redis(self, make_get_request, es_client):
        """Тест для получения данных из Redis при повторном запросе всех фильмов"""
        es_response = await make_get_request(f'{FILMS_ENDPOINT}')

        assert es_response.status == HTTPStatus.OK
        assert len(es_response.body) == len(FILMS)
        assert all([self.film[key] == value for key, value in es_response.body[0].items()])

        await delete_es_index(es_client, EsIndexes.movies.value)

        redis_response = await make_get_request(f'{FILMS_ENDPOINT}')

        assert redis_response.status == HTTPStatus.OK
        assert es_response == redis_response

        await populate_es(es_client,
                          EsIndexes.movies.value,
                          FILM_INDEX,
                          FILMS)

    @pytest.mark.asyncio
    async def test_film_search_redis(self, make_get_request, es_client):
        """Тест для получения данных из Redis при повторном запросе с поиском"""
        query = self.film['description'].split(' ')[0]
        url = f'{FILMS_ENDPOINT}/search/?query={query}'
        es_response = await make_get_request(url)

        assert es_response.status == HTTPStatus.OK
        assert len(es_response.body) == len(filter_by_field(FILMS, 'description', query))

        await delete_es_index(es_client, EsIndexes.movies.value)

        redis_response = await make_get_request(url)

        assert redis_response.status == HTTPStatus.OK
        assert len(redis_response.body) == len(filter_by_field(FILMS, 'description', query))
        assert es_response == redis_response

        await populate_es(es_client,
                          EsIndexes.movies.value,
                          FILM_INDEX,
                          FILMS)
