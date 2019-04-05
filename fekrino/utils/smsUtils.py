from kavenegar import *

from fekrino.settings import KAVENEGAR_API_KEY
from kavenegar import *


def send_sms(phone_number, token):
    try:
        api = KavenegarAPI(KAVENEGAR_API_KEY)
        params = {
            'receptor': phone_number,
            'template': 'fekrino',
            'token': token,
            'type': 'sms',
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
      print(e)
    except HTTPException as e:
      print(e)