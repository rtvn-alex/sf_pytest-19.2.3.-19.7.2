from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверка, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

    
def test_get_api_key_for_invalid_user(email=valid_email, password='valid_password'):
    """ Проверка, что запрос api ключа с невалидным паролем возвращает статус 403"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    
    
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверка, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

    
def test_get_all_pets_with_invalid_filter_data(filter='any'):
    """Проверка, что запрос питомцев с неверным фильтром не выполняется или выполняется с ошибкой"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)

    assert status != 200

    
def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверка, что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_new_no_photo_pet(name='Pies', animal_type='Pies', age='2'):
    """Проверка, можно ли добавить питомца без фото"""
    
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_no_photo_pet(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_unsuccesful_add_new_pet_with_null_data(name=None, animal_type=None, age=None):
    """Проверка, что нельзя добавить питомца с значениями полей None.
    Тест должен провалиться"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_no_photo_pet(auth_key, name, animal_type, age)

    assert status == 200


def test_add_new_no_photo_pet_with_invalid_age(name='Pies', animal_type='Pies', age='kot'):
    """Проверка, можно ли добавить питомца без фото, указав в поле Возраст буквенное значение"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_no_photo_pet(auth_key, name, animal_type, age)

    assert status == 400


def test_add_new_pet_with_fake_id(name='Pies', animal_type='Pies', age='4'):
    """Проверка, можно ли добавить питомца c неверным кодом авторизации"""
    
    auth_key = {"key": "z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1z1"}
    status, result = pf.add_new_no_photo_pet(auth_key, name, animal_type, age)

    assert status == 403


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_unsuccessful_deleting_pet_with_invalid_id():
    """Проверяем возможность удаления питомца c несуществующим id.
    Тест должен провалиться"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = 'a1a1'
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200


def test_successful_updating_of_pet_info_by_adding_photo(pet_photo='images/cat1.jpg'):
    """"Проверка добавления фото"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    print(my_pets)

    if len(my_pets['pets']) > 0:
        status, _ = pf.add_photo_to_pet_info(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
    else:
        raise Exception("There are no my pets")


def test_successful_updating_of_pet_info_by_adding_png_photo(pet_photo='images/cat1.png'):
    """"Проверка добавления фото в формате .png"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    print(my_pets)

    if len(my_pets['pets']) > 0:
        status, _ = pf.add_photo_to_pet_info(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
    else:
        raise Exception("There are no my pets")


def test_successful_updating_of_pet_info_by_adding_tiff_photo(pet_photo='images/cat1.tiff'):
    """"Проверка добавления фото в формате .tiff"""
    
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    print(my_pets)

    if len(my_pets['pets']) > 0:
        status, _ = pf.add_photo_to_pet_info(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 400
    else:
        raise Exception("There are no my pets")


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There are no my pets")
