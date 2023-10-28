

from pytonconnect import TonConnect


from tc_storage import TcStorage

def get_connector(chat_id: int):
    return TonConnect(manifest_url="https://github.com/LinBBB/Ton_tgbot/blob/main/manifest.json", storage=TcStorage(chat_id=chat_id))






