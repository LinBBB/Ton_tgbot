import asyncio
from pytonconnect import TonConnect

async def main():
    connector = TonConnect(manifest_url='https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect-manifest.json')
    is_connected = await connector.restore_connection()
    print('is_connected:', is_connected)

    wallets_list = connector.get_wallets()

    print(wallets_list)
    generated_url = await connector.connect(wallets_list[0])
    print(wallets_list[0])
    print('generated_url:', generated_url)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())