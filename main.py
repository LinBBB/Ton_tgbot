import asyncio
import sys
import time

import loguru
import pytonconnect.exceptions
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, CommandStart
import json
import logging
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pytonconnect import TonConnect
from tonsdk.utils import Address

import config
from connector import get_connector
from messages import get_comment_message

logger = logging.getLogger(__file__)

dp = Dispatcher()
bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    chat_id = message.chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()

    mk_b = InlineKeyboardBuilder()
    if connected:
        mk_b.button(text="Send Transaction", callback_data="send_tr")
        mk_b.button(text="Disconnect", callback_data="disconnect")
        await message.answer(text='You are already connected!', reply_markup=mk_b.as_markup())
    else:
        wallets_list = TonConnect.get_wallets()
        loguru.logger.debug(wallets_list)
        for wallet in wallets_list:
            mk_b.button(text=wallet['name'], callback_data=f'connect:{wallet["name"]}')
        mk_b.adjust(1, )
        await message.answer(text='Choose wallet to connect', reply_markup=mk_b.as_markup())


async def connect_wallet(message: Message, wallet_name: str):

    connector = get_connector(message.chat.id)

    wallets_list = connector.get_wallets()
    wallet = None

    for w in wallets_list:
        if w["name"] == wallet_name:
            wallet = w

    if wallet is None:
        raise Exception(f"Unknown wallet: {wallet_name}")

    generated_url = await connector.connect(wallet=wallet)
    loguru.logger.info(f"wallet:{wallet};url:{generated_url}")
    mk_b = InlineKeyboardBuilder()
    mk_b.button(text="Connect", url=generated_url)

    await message.answer(text="Connect wallet within 3 minutes", reply_markup=mk_b.as_markup())

    mk_b = InlineKeyboardBuilder()
    mk_b.button(text="Start", callback_data="start")

    for i in range(1, 30):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                wallet_address = connector.account.address
                wallet_address = Address(wallet_address).to_string(is_bounceable=False)
                await message.answer(f'You are connected with address <code>{wallet_address}</code>',
                                     reply_markup=mk_b.as_markup())
                logger.info(f'Connected with address: {wallet_address}')
            return

    await message.answer(f'Timeout error!', reply_markup=mk_b.as_markup())


@dp.message(Command('transaction'))
async def send_transaction(message: Message):
    connector = get_connector(message.chat.id)
    connected = await connector.restore_connection()

    if not connected:
        await message.answer("Connect wallet first")
        return

    transaction = {
        "valid_until": int(time.time() + 3600),
        "messages": [
            get_comment_message(
                destination_address='0:0000000000000000000000000000000000000000000000000000000000000000',
                amount=int(0.01 * 10 ** 9),
                comment='hello world!'
            )
        ]
    }

    await message.answer(text="Approve transaction in your wallet app")

    try:
        await asyncio.wait_for(connector.send_transaction(
            transaction=transaction
        ),300)
    except asyncio.TimeoutError:
        await message.answer(text="Timeout error!")
    except pytonconnect.exceptions.UserRejectsError:
        await message.answer(text="You rejected the transaction!")
    except Exception as e:
        await message.answer(text=f"Unknown error: {e}")


async def disconnect_wallet(message: Message):
    connector = get_connector(message.chat.id)
    await connector.restore_connection()
    await connector.disconnect()
    await message.answer("You have been successfully disconnected!")


@dp.callback_query(lambda call: True)
async def main_callback_handler(call: CallbackQuery):
    await call.answer()
    message = call.message
    data = call.data
    if data == "start":
        await command_start_handler(message)
    elif data == "send_tr":
        await send_transaction(message)
    elif data == 'disconnect':
        await disconnect_wallet(message)
    else:
        data = data.split(':')
        if data[0] == 'connect':
            await connect_wallet(message, data[1])

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
