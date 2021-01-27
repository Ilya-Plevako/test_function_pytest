from datetime import datetime
from typing import Dict, List

from requests import post

from library import clients


def create_order_and_get_order_info(alias: str, client_id: str, address: str, phone: str, item_id: int,
                                    price: float, quantity: int) -> List[Dict]:
    """OAPI: Создание заказа (service/v1/order/create)

    Args:
        alias: псевдоним соединения.
        client_id: идентификатор клиента.
        address: адрес клиента.
        phone: номер телефона клиента.
        item_id: идентификатор товара.
        price: цена товара (за шт.).
        quantity: количество товара.

    Returns:
        order_info: информация о созданном заказе
    """
    uri = "service/v1/order/create"
    data = {
        'client_id': client_id,
        'address': address,
        'phone': phone,
        'items': [{
            'item_id': item_id,
            'price': price,
            'quantity': quantity
        }]
    }

    response = post(alias=alias, uri=uri, data=data)
    order_number = response.json()["order_number"]

    order_info = [{
        'order_number': order_number,
        'client_id': client_id,
        'last_purchase_date': str(datetime.now().replace(microsecond=0)),
        'items': [{
            'item_id': item_id,
            'price': price,
            'quantity': quantity
        }
        ]
    }]
    return order_info


def create_client_and_add_one_order(alias='token', name='Vanya', surname='Pupkin', address='Moscow, Red Square, 1',
                                    phone='+79265437898', item_id=7800188, price=500, quantity=2):
    """Создание клиента и оформление ему одного заказа
    """
    client_id = clients.create_client(alias=alias, name=name, surname=surname, phone=phone)
    order_info = create_order_and_get_order_info(alias=alias, client_id=client_id, address=address,
                                                 phone=phone, item_id=item_id, price=price,
                                                 quantity=quantity)
    return order_info


def create_client_and_add_two_orders(alias='token', name='Vanya', surname='Pupkin', address='Moscow, Red Square, 1',
                                     phone='+79265437898', item_id=7800188, price=500, quantity_first_order=5,
                                     quantity_second_order=15):
    """Создание клиента и оформление ему двух заказаов
    """
    client_id = clients.create_client(alias=alias, name=name, surname=surname, phone=phone)
    first_order_info = create_order_and_get_order_info(alias=alias, client_id=client_id, address=address,
                                                       phone=phone, item_id=item_id, price=price,
                                                       quantity=quantity_first_order)

    second_order_info = create_order_and_get_order_info(alias=alias, client_id=client_id, address=address,
                                                        phone=phone, item_id=item_id, price=price,
                                                        quantity=quantity_second_order)

    final_order_info = [first_order_info, second_order_info]
    return final_order_info


def count_item_id_from_orders(item_id, orders_info):
    """Вычисление суммарного количества товара item_id среди переданных заказов
    """
    sum_item_count = sum(
        [count["items"][0]["quantity"] for count in orders_info if count["items"][0]["quantity"] is not None
         and count["items"][0]["item_id"] == item_id])

    return sum_item_count


def get_last_order_number(item_id, orders_info):
    """Нахождение последнего номера заказа по item_id
    """
    # отбираем только информацию по необходимому товару, отбрасываем другие товары
    order_info_by_item_id = [count for count in orders_info if count["items"][0]["quantity"] is not None
                             and count["items"][0]["item_id"] == item_id]
    # сортируем по дате
    sorted_orders_info = sorted(order_info_by_item_id, key=lambda k: k['last_purchase_date'])

    return sorted_orders_info[-1]['order_number']
