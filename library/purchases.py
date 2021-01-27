import random
from datetime import datetime, timedelta
from typing import Dict


def client_purchase_by_item_id(item_ids: list = None, client_id: str = None) -> Dict:
    """OAPI: Информация о покупах клиентом товаров {X} (service/v1/item/purchase/by-client)

    Args:
        item_ids: идентификаторы товаров.
        client_id: идентификатор клиента.

    Returns:
        Информация о количестве, дате и номер заказа или отсутствии покупки товара с таким item_ids.
    """
    # ниже закомментирован код функции, если бы она существовала на самом деле.
    # uri = "service/v1/item/purchase/by-client"
    # data = {
    #     'client_id': client_id,
    #     'item_ids': [item_ids]
    # }

    # response = post(alias=alias, uri=uri, data=data)
    # return response

    # имитация ответа функции
    response = {"items": []}

    for i in item_ids:
        purchased = random.randint(0, 1)
        if purchased:
            last_order_number = str(random.randint(1000, 5000))
            last_purchase_date = str(
                datetime.now().replace(microsecond=0) - timedelta(days=random.randint(7, 10),
                                                                  minutes=random.randint(1, 60)))
        else:
            last_order_number = None
            last_purchase_date = None

        response["items"].append({"item_id": i,
                                  "purchased": bool(purchased),
                                  "last_order_number": last_order_number,
                                  "last_purchase_date": last_purchase_date,
                                  "purchase_count": purchased * random.randint(1, 100)})
    return response
