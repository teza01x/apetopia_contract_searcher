import asyncio
from bs4 import BeautifulSoup
from config import *
from asc_cloud import *


def clean_text(text):
    split_terms = ["Represents", "Shows", "Presents", "Indicates"]
    for term in split_terms:
        if term in text:
            return text.split(term)[0].strip()
    return text


def first_point(html, wallet_address):
    soup = BeautifulSoup(html, 'html.parser')

    header = list()
    body = list()
    index = 0

    labels = [
        "PNL:",
        "Trading Volume(90D) :",
        "Total Trades(90D) :",
        "Balance:"
    ]

    for label in labels:
        element = soup.select_one(f'p:-soup-contains("{label}")')
        if element:
            value = element.get_text(strip=True).replace(label, '')
            cleaned_value = clean_text(value)
            header.append(f"**{label}** {cleaned_value}")

    trade_elements = soup.select('.table-row__desktop_grid a[href^="/app/eth/chart/"]')

    if len(trade_elements) > 3:
        for trade_element in trade_elements[:3]:
            trade_name = trade_element.select_one('p.text-white').get_text()
            try:
                try:
                    trade_value = trade_element.find_next('p',
                                                          class_='self-center text-center text-[#16c784] font-extrabold').get_text()
                except:
                    try:
                        trade_value = trade_element.find_next('p',
                                                              class_='self-center text-center text-[#16c784] font-bold').get_text()
                    except:
                        trade_value = trade_element.find_next('p',
                                                              class_='self-center text-center text-[#16c784] font-semibold').get_text()
            except:
                trade_value = trade_element.find_next('p', class_='self-center text-center text-[#16c784]').get_text()
            trade_percentage = trade_element.find_next('p', class_='self-center text-center text-white').get_text()
            body.append(f"**{trade_name}:** {trade_value} - {trade_percentage}")
    else:
        for trade_element in trade_elements:
            trade_name = trade_element.select_one('p.text-white').get_text()
            try:
                try:
                    trade_value = trade_element.find_next('p',
                                                          class_='self-center text-center text-[#16c784] font-extrabold').get_text()
                except:
                    try:
                        trade_value = trade_element.find_next('p',
                                                              class_='self-center text-center text-[#16c784] font-bold').get_text()
                    except:
                        trade_value = trade_element.find_next('p',
                                                              class_='self-center text-center text-[#16c784] font-semibold').get_text()
            except:
                trade_value = trade_element.find_next('p', class_='self-center text-center text-[#16c784]').get_text()
            trade_percentage = trade_element.find_next('p', class_='self-center text-center text-white').get_text()
            body.append(f"**{trade_name}:** {trade_value} - {trade_percentage}")

    # risk calculation
    for label in labels:
        element = soup.select_one(f'p:-soup-contains("{label}")')
        if element:
            value = element.get_text(strip=True).replace(label, '')
            cleaned_value = clean_text(value)
            if label == "PNL:":
                pnl_value = float(cleaned_value[1:].replace(",", ''))
            elif label == "Trading Volume(90D) :":
                trading_volume_value = float(cleaned_value[1:].replace(",", ''))

    pnl_percentage = (pnl_value / trading_volume_value) * 100

    if pnl_percentage > 50:
        risk = "🟢"
    elif 30 <= pnl_percentage <= 49:
        risk = "🟠"
    else:
        risk = "🔴"

    new_header = list()
    for point in header:
        index += 1
        if index == 1:
            new_header.append("💰" + point)
        elif index == 2:
            new_header.append("📊" + point)
        elif index == 3:
            new_header.append("#️⃣" + point)

    index = 0
    new_body = list()
    for point in body:
        index += 1
        if index == 1:
            new_body.append("🥇" + point)
        elif index == 2:
            new_body.append("🥈" + point)
        elif index == 3:
            new_body.append("🥉" + point)


    private_group = "**Wallet:** `{}`\n\n{}\n\n🔥**3 Highest Profit/ROI:**🔥\n{}\n\n**Risk:** {}".format(wallet_address, "\n".join(new_header), "\n".join(new_body), risk)

    standard_group = "**Wallet:** `0x..(Upgrade to Premium to see full address)`\n\n{}\n\n🔥**3 Highest Profit/ROI:**🔥\n{}\n\n**Risk:** {}".format("\n".join(header), "\n".join(body), risk)

    return private_group, standard_group


def second_point(html, contract_address):
    soup = BeautifulSoup(html, 'html.parser')

    private_template = list()
    standard_template = list()

    coin_pair_element = soup.find('h2', class_='chakra-heading custom-hvdbl1')

    coin_pair = coin_pair_element.text
    coin_pair = coin_pair.replace("Copy token address", "")


    block_txns = soup.find('div', class_='custom-17mi4hx')

    txns = block_txns.find_all('div', class_='custom-kfd3si')

    index = 0
    for txn in txns:
        href = txn.find('a')['href']
        wallet = href.split('/')[-1]
        try:
            bought = txn.find('span', class_="chakra-text custom-rcecxm").get_text().strip()
            try:
                txs = txn.find_all('span', class_="chakra-text custom-13ppmr2")[0].get_text().strip()
                bought_txns = "({})".format(txs.split()[0].split('/')[-1] + " txns")
            except:
                bought_txns = ''
        except:
            bought = "N/A"
            bought_txns = ''

        try:
            sold = txn.find('span', class_="chakra-text custom-dv3t8y").get_text().strip()
        except:
            sold = "N/A"
        try:
            if bought == "N/A":
                try:
                    txs = txn.find_all('span', class_="chakra-text custom-13ppmr2")[0].get_text().strip()
                    sold_txns = "({})".format(txs.split()[0].split('/')[-1] + " txns")
                except:
                    sold_txns = ''
            else:
                txs = txn.find_all('span', class_="chakra-text custom-13ppmr2")[1].get_text().strip()
                sold_txns = "({})".format(txs.split()[0].split('/')[-1] + " txns")
        except:
            sold_txns = ''

        try:
            pnl = txn.find('div', class_="custom-1e9y0rl").get_text().strip()
        except:
            pnl = "N/A"

        try:
            unrealized = txn.find('div', class_="custom-1hd7h4r").get_text().strip()
            if unrealized == "-":
                unrealized = "N/A"
        except:
            unrealized = "N/A"

        try:
            balance_element = txn.find('div', class_="custom-1cicvqe").get_text().strip()
            balance = " of ".join(balance_element.split("of"))
        except:
            balance = "Unknown"


        if bought == "N/A" or sold == "N/A":
            pass
        else:
            check_bought = bought.replace("$", "").replace(",", ".").replace("<", "").replace(">", "")
            check_sold = sold.replace("$", "").replace(",", ".").replace("<", "").replace(">", "")

            if "K" in check_bought:
                check_bought = float(check_bought.replace("K", "")) * 1000
            else:
                check_bought = float(check_bought)
            if "K" in check_sold:
                check_sold = float(check_sold.replace("K", "")) * 1000
            else:
                check_sold = float(check_sold)


            difference = abs(check_bought - check_sold)
            threshold_20_percent = 0.2 * min(check_bought, check_sold)

            if difference > threshold_20_percent:
                index += 1
                if index == 1:
                    private_template.append(f"🥇**Wallet:** `{wallet}`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                    standard_template.append(f"🥇**Wallet:** `0x..(Upgrade to Premium)`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                elif index == 2:
                    private_template.append(f"🥈**Wallet:** `{wallet}`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                    standard_template.append(f"🥈**Wallet:** `0x..(Upgrade to Premium)`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                elif index == 3:
                    private_template.append(f"🥉**Wallet:** `{wallet}`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                    standard_template.append(f"🥉**Wallet:** `0x..(Upgrade to Premium)`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                else:
                    private_template.append(f"**RANK #{index}**\n**Wallet:** `{wallet}`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                    standard_template.append(f"**RANK #{index}**\n**Wallet:** `0x..(Upgrade to Premium)`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
            else:
                pass

    private_group = f"`${coin_pair}`\n\n📄Contract:\n`{contract_address}`\n\n" + f"📈 Chart: [Dextools](https://www.dextools.io/app/en/ether/pair-explorer/{contract_address}) | [Dexscreener](https://dexscreener.com/ethereum/{contract_address})\n\n" + "\n".join(private_template[:5])
    standard_group = f"`${coin_pair}`\n\n📄Contract:\n`0x..(Upgrade to Premium to see full address)`\n\n" + "\n".join(standard_template[:5])

    return private_group, standard_group


def third_point(html, iteration):
    soup = BeautifulSoup(html, 'html.parser')

    body = list()
    body_standard = list()
    hrefs = list()
    result = list()
    result_standard = list()
    contract_addresses = list()

    table_div = soup.find('div', class_='ds-dex-table ds-dex-table-top')
    a_elements = table_div.find_all('a', class_='ds-dex-table-row ds-dex-table-row-top')


    for a_element in a_elements[:5]:
        chain = a_element.find('img', class_='ds-dex-table-row-chain-icon')['title']
        pair = a_element.find('span', class_='ds-dex-table-row-base-token-symbol').get_text()
        pair += "/" + a_element.find('span', class_='ds-dex-table-row-quote-token-symbol').get_text()

        daily_percentage_change = a_element.find_all('div', class_='ds-table-data-cell ds-dex-table-row-col-price-change')
        try:
            price_changes = daily_percentage_change[-1].find_all('span', class_='ds-change-perc ds-change-perc-pos')
            price_change = price_changes[-1].get_text()
        except:
            price_changes = daily_percentage_change[-1].find_all('span', class_='ds-change-perc ds-change-perc-neg')
            price_change = "({})".format(price_changes[-1].get_text())

        address = a_element['href'].split('/')[-1]


        body.append(f"{pair} - {price_change} - `{address}`\n" + f"📈 Chart: [Dextools](https://www.dextools.io/app/en/ether/pair-explorer/{address}) | [Dexscreener](https://dexscreener.com/ethereum/{address})\n\n")
        body_standard.append(f"{pair} - {price_change} - `0x..(Upgrade to Premium)`")
        hrefs.append("https://dexscreener.com" + a_element['href'])


    for index, item in enumerate(body, 1):
        if index == 1:
            result.append(f"🥇{item}")
        elif index == 2:
            result.append(f"🥈{item}")
        elif index == 3:
            result.append(f"🥉{item}")
        else:
            result.append(f"**{index})** {item}")

    for index, item in enumerate(body_standard, 1):
        if index == 1:
            result_standard.append(f"🥇{item}")
        elif index == 2:
            result_standard.append(f"🥈{item}")
        elif index == 3:
            result_standard.append(f"🥉{item}")
        else:
            result_standard.append(f"**{index})** {item}")

    if iteration == 1:
        private_group = "🔥 **ETH TOP 5 ~ 25K** 🔥\n\n" + "\n\n".join(result)
        standard_group = "🔥 **ETH TOP 5 ~ 25K** 🔥\n\n" + "\n".join(result_standard)
    elif iteration == 2:
        private_group = "🔥 **ETH TOP 5 ~ 50K** 🔥\n\n" + "\n\n".join(result)
        standard_group = "🔥 **ETH TOP 5 ~ 50K** 🔥\n\n" + "\n".join(result_standard)
    elif iteration == 3:
        private_group = "🔥 **ETH TOP 5 ~ 100K** 🔥\n\n" + "\n\n".join(result)
        standard_group = "🔥 **ETH TOP 5 ~ 100K** 🔥\n\n" + "\n".join(result_standard)
    elif iteration == 4:
        private_group = "🔥 **ETH TOP 5 ~ 250K** 🔥\n\n" + "\n\n".join(result)
        standard_group = "🔥 **ETH TOP 5 ~ 250K** 🔥\n\n" + "\n".join(result_standard)

    return private_group, standard_group


def auto_third_point(html, iteration):
    soup = BeautifulSoup(html, 'html.parser')

    body = list()
    body_standard = list()
    hrefs = list()
    result = list()
    result_standard = list()
    contract_addresses = list()

    table_div = soup.find('div', class_='ds-dex-table ds-dex-table-top')
    a_elements = table_div.find_all('a', class_='ds-dex-table-row ds-dex-table-row-top')


    for a_element in a_elements[:5]:
        chain = a_element.find('img', class_='ds-dex-table-row-chain-icon')['title']
        pair = a_element.find('span', class_='ds-dex-table-row-base-token-symbol').get_text()
        pair += "/" + a_element.find('span', class_='ds-dex-table-row-quote-token-symbol').get_text()

        daily_percentage_change = a_element.find_all('div', class_='ds-table-data-cell ds-dex-table-row-col-price-change')
        try:
            price_changes = daily_percentage_change[-1].find_all('span', class_='ds-change-perc ds-change-perc-pos')
            price_change = price_changes[-1].get_text()
        except:
            price_changes = daily_percentage_change[-1].find_all('span', class_='ds-change-perc ds-change-perc-neg')
            price_change = "({})".format(price_changes[-1].get_text())

        address = a_element['href'].split('/')[-1]


        body.append(f"{pair} - {price_change} - `{address}`\n" + f"📈 Chart: [Dextools](https://www.dextools.io/app/en/ether/pair-explorer/{address}) | [Dexscreener](https://dexscreener.com/ethereum/{address})\n")
        contract_addresses.append(address)
        body_standard.append(f"{pair} - {price_change} - `0x..(Upgrade to Premium)`")
        hrefs.append("https://dexscreener.com" + a_element['href'])


    for index, item in enumerate(body, 1):
        if index == 1:
            result.append(f"🥇{item}")
        elif index == 2:
            result.append(f"🥈{item}")
        elif index == 3:
            result.append(f"🥉{item}")
        else:
            result.append(f"**{index})** {item}")

    for index, item in enumerate(body_standard, 1):
        if index == 1:
            result_standard.append(f"🥇{item}")
        elif index == 2:
            result_standard.append(f"🥈{item}")
        elif index == 3:
            result_standard.append(f"🥉{item}")
        else:
            result_standard.append(f"**{index})** {item}")

    if iteration == 1:
        private_group = "🔥 **ETH TOP 5 ~ 25K** 🔥\n\n" + "\n\n".join(result)
        standard_group = "🔥 **ETH TOP 5 ~ 25K** 🔥\n\n" + "\n".join(result_standard)
    elif iteration == 2:
        private_group = "🔥 **ETH TOP 5 ~ 50K** 🔥\n\n" + "\n\n".join(result)
        standard_group = "🔥 **ETH TOP 5 ~ 50K** 🔥\n\n" + "\n".join(result_standard)
    elif iteration == 3:
        private_group = "🔥 **ETH TOP 5 ~ 100K** 🔥\n\n" + "\n\n".join(result)
        standard_group = "🔥 **ETH TOP 5 ~ 100K** 🔥\n\n" + "\n".join(result_standard)
    elif iteration == 4:
        private_group = "🔥 **ETH TOP 5 ~ 250K** 🔥\n\n" + "\n\n".join(result)
        standard_group = "🔥 **ETH TOP 5 ~ 250K** 🔥\n\n" + "\n".join(result_standard)

    return private_group, standard_group, contract_addresses


def auto_second_point(html, contract_address):
    soup = BeautifulSoup(html, 'html.parser')

    private_template = list()
    standard_template = list()
    wallet_addresses = list()

    coin_pair_element = soup.find('h2', class_='chakra-heading custom-hvdbl1')

    coin_pair = coin_pair_element.text
    coin_pair = coin_pair.replace("Copy token address", "")

    block_txns = soup.find('div', class_='custom-17mi4hx')

    txns = block_txns.find_all('div', class_='custom-kfd3si')

    index = 0
    for txn in txns:
        href = txn.find('a')['href']
        wallet = href.split('/')[-1]
        try:
            bought = txn.find('span', class_="chakra-text custom-rcecxm").get_text().strip()
            try:
                txs = txn.find_all('span', class_="chakra-text custom-13ppmr2")[0].get_text().strip()
                bought_txns = "({})".format(txs.split()[0].split('/')[-1] + " txns")
            except:
                bought_txns = ''
        except:
            bought = "N/A"
            bought_txns = ''

        try:
            sold = txn.find('span', class_="chakra-text custom-dv3t8y").get_text().strip()
        except:
            sold = "N/A"
        try:
            if bought == "N/A":
                try:
                    txs = txn.find_all('span', class_="chakra-text custom-13ppmr2")[0].get_text().strip()
                    sold_txns = "({})".format(txs.split()[0].split('/')[-1] + " txns")
                except:
                    sold_txns = ''
            else:
                txs = txn.find_all('span', class_="chakra-text custom-13ppmr2")[1].get_text().strip()
                sold_txns = "({})".format(txs.split()[0].split('/')[-1] + " txns")
        except:
            sold_txns = ''

        try:
            pnl = txn.find('div', class_="custom-1e9y0rl").get_text().strip()
        except:
            pnl = "N/A"

        try:
            unrealized = txn.find('div', class_="custom-1hd7h4r").get_text().strip()
            if unrealized == "-":
                unrealized = "N/A"
        except:
            unrealized = "N/A"

        try:
            balance_element = txn.find('div', class_="custom-1cicvqe").get_text().strip()
            balance = " of ".join(balance_element.split("of"))
        except:
            balance = "Unknown"

        if bought == "N/A" or sold == "N/A":
            pass
        else:
            check_bought = bought.replace("$", "").replace(",", ".").replace("<", "").replace(">", "")
            check_sold = sold.replace("$", "").replace(",", ".").replace("<", "").replace(">", "")

            if "K" in check_bought:
                check_bought = float(check_bought.replace("K", "")) * 1000
            else:
                check_bought = float(check_bought)
            if "K" in check_sold:
                check_sold = float(check_sold.replace("K", "")) * 1000
            else:
                check_sold = float(check_sold)


            difference = abs(check_bought - check_sold)
            threshold_20_percent = 0.2 * min(check_bought, check_sold)

            if difference > threshold_20_percent:
                wallet_addresses.append(wallet)
                index += 1
                if index == 1:
                    private_template.append(f"🥇**Wallet:** `{wallet}`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                    standard_template.append(f"🥇**Wallet:** `0x..(Upgrade to Premium)`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                elif index == 2:
                    private_template.append(f"🥈**Wallet:** `{wallet}`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                    standard_template.append(f"🥈**Wallet:** `0x..(Upgrade to Premium)`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                elif index == 3:
                    private_template.append(f"🥉**Wallet:** `{wallet}`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                    standard_template.append(f"🥉**Wallet:** `0x..(Upgrade to Premium)`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                else:
                    private_template.append(f"**RANK #{index}**\n**Wallet:** `{wallet}`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
                    standard_template.append(f"**RANK #{index}**\n**Wallet:** `0x..(Upgrade to Premium)`\n\n🔥**Bought:** {bought} {bought_txns}\n❌**Sold:** {sold} {sold_txns}\n📊**PNL:** {pnl}\n🚀**Unrealized:** {unrealized}\n💰**Balance:** {balance}\n")
            else:
                pass

    private_group = f"`${coin_pair}`\n\n📄Contract:\n`{contract_address}`\n\n" + f"📈 Chart: [Dextools](https://www.dextools.io/app/en/ether/pair-explorer/{contract_address}) | [Dexscreener](https://dexscreener.com/ethereum/{contract_address})\n\n" + "\n".join(private_template[:3])
    standard_group = f"`${coin_pair}`\n\n📄Contract:\n`0x..(Upgrade to Premium to see full address)`\n\n" + "\n".join(standard_template[:3])

    return private_group, standard_group, wallet_addresses[:3]
