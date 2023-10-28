import json

from pytonconnect import TonConnect

import config
from tc_storage import TcStorage


x = json.dumps({"url": "https://github.com/XaBbl4/pytonconnect","name": "PyTonConnect","iconUrl": "https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect.png"})

def get_connector(chat_id: int):
    return TonConnect(manifest_url=x, storage=TcStorage(chat_id=chat_id))






