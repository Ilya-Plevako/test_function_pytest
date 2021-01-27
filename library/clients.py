from requests import post


def create_client(alias: str, name: str, surname: str, phone: str) -> str:
    """OAPI: Создание клиента (service/v1/client/create)

    Args:
        alias: псевдоним соединения.
        name: имя клиента.
        surname: фамилия клиента.
        phone: номер телефона клиента.

    Returns:
        client_id: идентификатор созданного клиента.
    """
    uri = "service/v1/client/create"
    data = {
        'name': name,
        'surname': surname,
        'phone': phone
    }

    response = post(alias=alias, uri=uri, data=data)
    return response.json()["client_id"]
