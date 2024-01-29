import asyncio
import time
import datetime
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup
from telebot import types
from config import *
from asc_cloud import *
from parser import *
from markdownv2 import *
from sql_scripts import *


bot = AsyncTeleBot(telegram_token)


async def auto_scan(wallet_address):
    try:
        try:
            while True:
                first_point_info = first_pass_cycle(wallet_address)
                if first_point_info == "busy":
                    time.sleep(20)
                elif first_point_info[0] == "free":
                    result_private, result_standard = first_point(first_point_info[1], wallet_address)
                    break
            try:
                markdown_text_private = escape(result_private, flag=0)
            except Exception as error:
                print(error)
            try:
                markdown_text_standard = escape(result_standard, flag=0)
            except Exception as error:
                print(error)

            return markdown_text_private, markdown_text_standard
        except:
            return [], []
    except Exception as e:
        print(f"Error: {e}")


async def auto_contract(contract_address):
    try:
        try:
            while True:
                second_point_info = auto_second_pass_cycle(contract_address)
                if second_point_info == "busy":
                    time.sleep(20)
                elif second_point_info[0] == "free":
                    result_private, result_standard, wallet_addresses = auto_second_point(second_point_info[1], contract_address)
                    break
            try:
                markdown_text_private = escape(result_private, flag=0)
            except Exception as error:
                print(error)
            try:
                markdown_text_standard = escape(result_standard, flag=0)
            except Exception as error:
                print(error)

            return markdown_text_private, markdown_text_standard, wallet_addresses
        except:
            return [], [], []
    except Exception as e:
        print(f"Error: {e}")


async def auto_top(url, iteration):
    try:
        try:
            while True:
                third_point_info = auto_third_pass_cycle(url)
                if third_point_info == "busy":
                    await asyncio.sleep(20)
                elif third_point_info[0] == "free":
                    result_private, result_standard, contract_addresses = auto_third_point(third_point_info[1], iteration)
                    break
            try:
                markdown_text_private = escape(result_private, flag=0)
            except Exception as error:
                print(error)
            try:
                markdown_text_standard = escape(result_standard, flag=0)
            except Exception as error:
                print(error)

            return markdown_text_private, markdown_text_standard, contract_addresses
        except:
            return [], [], []
    except Exception as e:
        print(f"Error: {e}")


async def auto_posting_info():
    while True:
        try:
            time.sleep(10)
            off_driver_func()
            time.sleep(10)
            liq_urls = [
                "https://dexscreener.com/gainers?chainIds=ethereum&maxLiq=25000&min24HTxns=300&min24HSells=30&min24HVol=25000",
                "https://dexscreener.com/gainers?chainIds=ethereum&minLiq=25000&maxLiq=50000&min24HTxns=300&min24HSells=30&min24HVol=50000",
                "https://dexscreener.com/gainers?chainIds=ethereum&minLiq=50000&maxLiq=100000&min24HTxns=300&min24HSells=30&min24HVol=100000",
                "https://dexscreener.com/gainers?chainIds=ethereum&minLiq=100000&maxLiq=250000&min24HTxns=300&min24HSells=30&min24HVol=250000",
            ]
            iteration = 0
            for url in liq_urls:
                iteration += 1
                private_group_top, standard_group_top, contracts = await auto_top(url, iteration)

                private_bot = telebot.TeleBot(telegram_token)

                if len(private_group_top) == 0:
                    pass
                else:
                    try:
                        private_bot.send_message(chat_id=private_group_id, message_thread_id=14312, text=private_group_top, parse_mode="MarkdownV2")
                    except Exception as error:
                        print(error)
                    time.sleep(30)
                    for contract in contracts[:3]:
                        private_group_contract, standard_group_contract, wallet_addresses = await auto_contract(contract)
                        if len(private_group_contract) == 0:
                            pass
                        else:
                            try:
                                private_bot.send_message(chat_id=private_group_id, message_thread_id=14312, text=private_group_contract, parse_mode="MarkdownV2")
                            except Exception as error:
                                print(error)
                            time.sleep(30)
                            for wallet in wallet_addresses:
                                private_group_scan, standard_group_scan = await auto_scan(wallet)
                                if len(private_group_scan) == 0:
                                    pass
                                else:
                                    try:
                                        private_bot.send_message(chat_id=private_group_id, message_thread_id=14312, text=private_group_scan, parse_mode="MarkdownV2")
                                    except Exception as error:
                                        print(error)
                                    time.sleep(30)
                off_driver_func()
                time.sleep(3600)
        except Exception as error:
            print(error)


async def main():
    bot_task = asyncio.create_task(bot.polling(non_stop=True, request_timeout=500))
    auto_top_post = asyncio.create_task(auto_posting_info())
    await asyncio.gather(bot_task, auto_top_post)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
