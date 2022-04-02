import pytest

from src.dictionary import errors_dict

from ..testdata.constants import PERSON_ENDPOINT, EsIndexes
from ..testdata.persons import PERSON_INDEX, PERSONS
from ..utils import delete_es_index, populate_es


class TestPerson:
    person = PERSONS[0]['_source']

    @pytest.mark.asyncio
    async def test_person_detail_success(self, make_get_request):
        """Тест для получения персоны по id"""
        response = await make_get_request(f'{PERSON_ENDPOINT}/{self.person["id"]}')
        assert response.status == 200
        assert len(response.body) == 4

        assert all([self.person[key] == value
                    for key, value in response.body.items()])

    @pytest.mark.asyncio
    async def test_person_detail_not_found(self, make_get_request):
        """Тест для проверки 404 если персона не найдена"""
        response = await make_get_request(f'{PERSON_ENDPOINT}/1234567')

        assert response.status == 404

    @pytest.mark.asyncio
    async def test_persons_success(self, make_get_request):
        """Тест для получения всех персон"""
        response = await make_get_request(f'{PERSON_ENDPOINT}')

        assert response.status == 200
        assert len(response.body) == 3

        assert all([self.person[key] == value for key, value in response.body[0].items()])

    @pytest.mark.asyncio
    async def test_persons_asc_sort(self, make_get_request):
        """Тест для получения всех персон с учетом сортировки по имени asc"""
        sorted_persons = sorted(PERSONS, key=lambda person: person['_source']['full_name'])
        response = await make_get_request(f'{PERSON_ENDPOINT}?sort=full_name')

        assert response.status == 200
        assert len(response.body) == 3
        assert response.body[0]['full_name'] == sorted_persons[0]['_source']['full_name']

    @pytest.mark.asyncio
    async def test_persons_desc_sort(self, make_get_request):
        """Тест для получения всех персон с учетом сортировки по имени desc"""
        sorted_persons = sorted(PERSONS,
                                key=lambda person: person['_source']['full_name'],
                                reverse=True)
        response = await make_get_request(f'{PERSON_ENDPOINT}?sort=-full_name')

        assert response.status == 200
        assert len(response.body) == 3
        assert response.body[0]['full_name'] == sorted_persons[0]['_source']['full_name']

    @pytest.mark.asyncio
    async def test_persons_pagination(self, make_get_request):
        """Тест для получения персон с учетом пагинауии"""
        first_page = await make_get_request(f'{PERSON_ENDPOINT}?page=1&size=2')
        assert first_page.status == 200
        assert len(first_page.body) == 2

        second_page = await make_get_request(f'{PERSON_ENDPOINT}?page=2&size=2')
        assert second_page.status == 200
        assert len(second_page.body) == 1

        assert all([second_page.body[0]['id'] != result['id']
                    for result in first_page.body])

    @pytest.mark.asyncio
    async def test_persons_not_valid_pagination(self, make_get_request):
        """Тест для проверки 422 если параметры для пагинации не имеют числовой тип"""
        response = await make_get_request(f'{PERSON_ENDPOINT}?page=one&size=two')

        assert response.status == 422
        assert response.body['detail'][0]['msg'] == 'value is not a valid integer'

    @pytest.mark.asyncio
    async def test_persons_search_by_full_name(self, make_get_request):
        """Тест для поиска персон по имени"""
        query = self.person["full_name"]
        url = f'{PERSON_ENDPOINT}/search/?query={query}'
        response = await make_get_request(url)

        assert response.status == 200
        assert len(response.body) == 1
        assert response.body[0]['full_name'] == self.person['full_name']

    @pytest.mark.asyncio
    async def test_persons_search_by_not_exist(self, make_get_request):
        """Тест для проверки 404 ошибки если ничего не найдено"""
        url = f'{PERSON_ENDPOINT}/search/?query=not_exist_text'
        response = await make_get_request(url)

        assert response.status == 404
        assert response.body['detail'] == errors_dict['404_persons']

    @pytest.mark.asyncio
    async def test_person_detail_redis(self, make_get_request, es_client):
        """Тест для получения данных из Redis при повторном запросе конкретной персоны"""
        es_response = await make_get_request(f'{PERSON_ENDPOINT}/{self.person["id"]}')

        assert es_response.status == 200
        assert len(es_response.body) == 4

        await delete_es_index(es_client, EsIndexes.persons.value)

        redis_response = await make_get_request(f'{PERSON_ENDPOINT}/{self.person["id"]}')

        assert redis_response.status == 200
        assert len(redis_response.body) == 4
        assert es_response == redis_response

        await populate_es(es_client, EsIndexes.persons.value, PERSON_INDEX, PERSONS)

    @pytest.mark.asyncio
    async def test_persons_redis(self, make_get_request, es_client):
        """Тест для получения данных из Redis при повторном запросе всех персон"""
        es_response = await make_get_request(f'{PERSON_ENDPOINT}')

        assert es_response.status == 200
        assert len(es_response.body) == 3

        await delete_es_index(es_client, EsIndexes.persons.value)

        redis_response = await make_get_request(f'{PERSON_ENDPOINT}')

        assert redis_response.status == 200
        assert len(redis_response.body) == 3
        assert es_response == redis_response

        await populate_es(es_client, EsIndexes.persons.value, PERSON_INDEX, PERSONS)

    @pytest.mark.asyncio
    async def test_person_search_redis(self, make_get_request, es_client):
        """Тест для получения данных из Redis при повторном запросе с поиском"""
        query = self.person["full_name"]
        url = f'{PERSON_ENDPOINT}/search/?query={query}'
        es_response = await make_get_request(url)

        assert es_response.status == 200
        assert len(es_response.body) == 1

        await delete_es_index(es_client, EsIndexes.persons.value)

        redis_response = await make_get_request(url)

        assert redis_response.status == 200
        assert len(redis_response.body) == 1
        assert es_response == redis_response

        await populate_es(es_client, EsIndexes.persons.value, PERSON_INDEX, PERSONS)
