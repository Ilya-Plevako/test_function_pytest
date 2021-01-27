from unittest.mock import Mock

import pytest

from library import orders
from library import purchases


class TestCreateClient(object):

    # проверка, что для товара с purchased = True обязательно purchase_count > 0,
    #                          с purchased = False обязательно purchase_count = 0
    @pytest.mark.parametrize('item_ids',
                             [[7800181, 7800182, 7800183]])
    def test_client_purchased_and_count_purchased(self, item_ids):
        items = purchases.client_purchase_by_item_id(item_ids)['items']

        assert all([item['purchased'] == (item['purchase_count'] > 0) for item in items])

    # проверка, что если в одном заказе успешно куплено ненулевое количество товара, то итоговое количество корректное;
    #           что если в одном заказе при оформлении заказа передано quantity = 0, то и итоговое значение 0.
    @pytest.mark.parametrize('item_id,mock_value_order,mock_value_purchase',
                             [('7800181', [{
                                 'order_number': '999999',
                                 'client_id': '256865',
                                 'items': [{
                                     'item_id': '7800181',
                                     'price': 500,
                                     'quantity': 5
                                 }
                                 ]
                             }
                             ], [{'item_id': 7800181,
                                  'purchased': True,
                                  'last_order_number': '999999',
                                  'last_purchase_date': '2021-01-29 17:19:43.027852',
                                  'purchase_count': 5}]),
                              ('7800182', [{
                                  'order_number': None,
                                  'client_id': '256865',
                                  'items': [{
                                      'item_id': '7800182',
                                      'price': None,
                                      'quantity': 0
                                  }
                                  ]
                              }
                              ], [{'item_id': 7800182,
                                   'purchased': False,
                                   'last_order_number': None,
                                   'last_purchase_date': None,
                                   'purchase_count': 0}]
                               )])
    def test_count_item_id_by_one_purchase(self, item_id, mock_value_order, mock_value_purchase):
        orders_info = orders.create_client_and_add_one_order = Mock(return_value=mock_value_order)
        result = orders.count_item_id_from_orders(item_id=item_id, orders_info=orders_info.return_value)
        exp_result = purchases.client_purchase_by_item_id = Mock(return_value=mock_value_purchase)
        assert result == exp_result.return_value[0]['purchase_count']

    # проверка для фиксации ожидаемого некорректного поведения, которое уже зафиксировано и скоро будет поправлено.
    @pytest.mark.xfail(reason="Если бы сейчас система работа некорректно и вернула на 1 товар больше, чем реально "
                              "куплено")
    @pytest.mark.parametrize('item_id,mock_value_order,mock_value_purchase',
                             [('7800181', [{
                                 'order_number': '999999',
                                 'client_id': '256865',
                                 'items': [{
                                     'item_id': '7800181',
                                     'price': 500,
                                     'quantity': 6
                                 }
                                 ]
                             }
                             ], [{'item_id': 7800181,
                                  'purchased': False,
                                  'last_order_number': None,
                                  'last_purchase_date': None,
                                  'purchase_count': 7}])])
    def test_incorrect_count_item_id_by_one_purchase(self, item_id, mock_value_order, mock_value_purchase):
        orders_info = orders.create_client_and_add_one_order = Mock(return_value=mock_value_order)
        result = orders.count_item_id_from_orders(item_id=item_id, orders_info=orders_info.return_value)
        exp_result = purchases.client_purchase_by_item_id = Mock(return_value=mock_value_purchase)
        assert result == exp_result.return_value[0]['purchase_count']

    # проверка, что если в двух заказах успешно куплено ненулевое количество одного и того же товара,
    #                                               то итоговое количество равно их сумме;
    #           что если в одном заказе куплено ненулевое, а в другом заказе нулевое количество,
    #                                               то итоговое количество равно только количеству из ненулевого заказа.
    @pytest.mark.parametrize('item_id,mock_value_order,mock_value_purchase',
                             [('7800181', [{
                                 'order_number': '777777',
                                 'client_id': '256865',
                                 'items': [{
                                     'item_id': '7800181',
                                     'price': 500,
                                     'quantity': 5
                                 }
                                 ]
                             },
                                 {
                                     'order_number': '888888',
                                     'client_id': '256865',
                                     'items': [{
                                         'item_id': '7800181',
                                         'price': 500,
                                         'quantity': 15
                                     }
                                     ]
                                 }
                             ], [{'item_id': 7800181,
                                  'purchased': True,
                                  'last_order_number': 888888,
                                  'last_purchase_date': '2021-01-29 17:19:43',
                                  'purchase_count': 20}]),
                               ('7800184', [{
                                   'order_number': '777777',
                                   'client_id': '256865',
                                   'items': [{
                                       'item_id': '7800184',
                                       'price': 500,
                                       'quantity': 50
                                   }
                                   ]
                               },
                                   {
                                       'order_number': None,
                                       'client_id': '256865',
                                       'items': [{
                                           'item_id': '7800184',
                                           'price': None,
                                           'quantity': 0
                                       }
                                       ]
                                   }
                               ], [{'item_id': 7800184,
                                    'purchased': True,
                                    'last_order_number': 777777,
                                    'last_purchase_date': '2021-01-29 17:19:43',
                                    'purchase_count': 50}]
                                )])
    def test_count_item_id_by_several_purchase(self, item_id, mock_value_order, mock_value_purchase):
        # подменяю результат ответа функции с заказам, чтобы обработать заказ
        orders_info = orders.create_client_and_add_two_order = Mock(return_value=mock_value_order)
        # вычисляю сумму купленных товаров с одинаковым id в рамках нескольких заказов
        result = orders.count_item_id_from_orders(item_id=item_id, orders_info=orders_info.return_value)
        # подменяю ответ тестируемой функции, т.к. нет возможности её вызывать
        exp_result = purchases.client_purchase_by_item_id = Mock(return_value=mock_value_purchase)
        assert result == exp_result.return_value[0]['purchase_count']

    @pytest.mark.parametrize('item_id,mock_value_order,mock_value_purchase',
                             [('7800188', [{
                                 'order_number': '999999',
                                 'client_id': '356178',
                                 'last_purchase_date': '2021-01-26 14:12:43',
                                 'items': [{
                                     'item_id': '7800188',
                                     'price': 500,
                                     'quantity': 18
                                 }
                                 ]
                             },
                                 {
                                     'order_number': '111555',
                                     'client_id': '356178',
                                     'last_purchase_date': '2021-01-28 17:39:43',
                                     'items': [{
                                         'item_id': '7800187',
                                         'price': 800,
                                         'quantity': 34
                                     }
                                     ]
                                 },
                                 {
                                     'order_number': '237987',
                                     'client_id': '356178',
                                     'last_purchase_date': '2020-11-12 08:39:43',
                                     'items': [{
                                         'item_id': '7800188',
                                         'price': 700,
                                         'quantity': 34
                                     }
                                     ]
                                 }
                             ], [{'item_id': 7800188,
                                  'purchased': True,
                                  'last_order_number': '999999',
                                  'last_purchase_date': '2021-01-29 17:19:43',
                                  'purchase_count': 20}])])
    def test_last_order_number(self, item_id, mock_value_order, mock_value_purchase):
        # подменяю результат ответа функции с заказам, чтобы обработать заказ
        orders_info = orders.create_client_and_add_two_order = Mock(return_value=mock_value_order)
        # вычисляю номер последнего заказа
        result = orders.get_last_order_number(item_id=item_id, orders_info=orders_info.return_value)
        # подменяю ответ тестируемой функции, т.к. нет возможности её вызывать
        exp_result = purchases.client_purchase_by_item_id = Mock(return_value=mock_value_purchase)
        # в ответе ожидаем 999999, т.к. хоть заказ 111555 более поздний, но в нём был заказан продукт 7800187,
        # а не 7800188, который передан на вход
        assert result == exp_result.return_value[-1]['last_order_number']
