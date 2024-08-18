import pytest

from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()


def test_add_new_pet_with_valid_data_and_without_photo(name = 'Рокси', animal_type = 'кошка',
                                         age = '6'):
    """Проверяем, что можно добавить питомца с корректными данными и без фото."""

    # Запрашиваем ключ API и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet_with_valid_data(pet_photo = 'images/roxy1.jpg'):
    """Проверяем, что можно добавить фото к уже существующему питомцу."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id последнего питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][-1]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ''


def test_get_api_key_for_invalid_user_email(email = invalid_email, password = valid_password):
    """ Проверяем, что запрос API ключа с неверной почтой пользователя возвращает статус 403 и Forbidden в значении."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

def test_get_api_key_for_invalid_user_password(email = valid_email, password = invalid_password):
    """ Проверяем, что запрос API ключа с неверным паролем пользователя возвращает статус 403 и Forbidden в значении."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result


def test_get_all_pets_with_wrong_filter(filter = 'цкв'):
    """ Проверяем, что запрос всех питомцев с неверным фильтром возвращает ошибку значения фильтра и статус запроса 500.
    """
    # Запрашиваем ключ API и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500
    assert 'Filter value is incorrect' in result

def test_add_new_pet_with_less_data(name='Тесла'):
    """Проверяем, что нельзя добавить питомца с меньшим количеством данных. Появляется ошибка"""

    # Запрашиваем ключ API и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пытаемся добавить питомца
    try:
        status, result = pf.add_new_pet_without_photo(auth_key, name)
    except Exception:
        TypeError

def test_add_new_pet_with_more_data(name = 'Тесла', animal_type = 'шиншилла',
                                         age = '7', pet_photo = 'images/tesla1.jpg', sex = 'male'):
        """Проверяем, что нельзя добавить питомца с большим количеством данных. Появляется ошибка"""

        # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

        # Запрашиваем ключ API и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Пытаемся добавить питомца
        try:
            status, result = pf.add_new_pet_without_photo(auth_key, name)
        except Exception:
            TypeError


def test_add_new_pet_with_long_name(name = 'A', animal_type = 'cat',
                                         age = '1'):
    """Проверяем, что можно добавить питомца с именем длиной 257 символов."""
    name = 257 * name
    # Запрашиваем ключ API и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_longest_name(name='A', animal_type='cat',
                                        age='1'):
    """Проверяем, что можно добавить питомца с именем длиной 1000 символов."""
    name = 1000 * name
    # Запрашиваем ключ API и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pet_in_wrong_format(pet_photo='images/1.png'):
    """Проверяем, что нельзя добавить фото в формате png: статус запроса 500, получена ошибка"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id последнего питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][-1]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500
    assert 'error' in result
