import os
import requests
from .models import OpenApi


def call_open_api(date, category):
    url = "http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList"
    query_params = {
        'p_product_cls_code': "01",
        'p_regday': date,
        'p_convert_kg_yn': "N",
        'p_item_category_code': str(category),
        'p_cert_key': os.environ['OPENAPI_KEY'],
        'p_cert_id': os.environ['OPENAPI_ID'],
        'p_returntype': "json"
    }
    api_res = requests.get(url, params=query_params)
    return api_res.json()


def put_data_to_api_table(date, category):
    json_res = call_open_api(date, category)
    try:
        items = json_res['data']['item']
    except:
        return
    open_api_list = [
        OpenApi(
            item_name=item['item_name'],
            kind_name=item['kind_name'],
            rank=item['rank'],
            unit=item['unit'],
            date=date,
            price=item['dpr1'],
            average_price=item['dpr7'],
        )
        for item in items
    ]
    OpenApi.objects.bulk_create(open_api_list)
