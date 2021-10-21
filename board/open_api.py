import os
import requests
from datetime import datetime


def call_open_api():
    url = "http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList"
    query_params = {
        'p_product_cls_code': "01",
        'p_regday': datetime.now().date(),
        'p_convert_kg_yn': "N",
        'p_item_category_code': "100",
        'p_cert_key': os.environ['OPENAPI_KEY'],
        'p_cert_id': os.environ['OPENAPI_ID'],
        'p_returntype': "json"
    }
    api_res = requests.get(url, params=query_params)
    return api_res.json()
