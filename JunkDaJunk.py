import requests
from time import sleep
import csv
import os
from colorama import init, Fore, Back, Style
from bs4 import BeautifulSoup

import sys


print("Version 3")

Password = "************"
cardid = ""
season = ""
from2 = ""

UserAgent=input("Please enter your main nation's name: ")+"JunkDaJunk written by 9003, Email: NSWA9002@gmail.com, discord 9003, NS nation: 9003"
giftto = input("Enter the nation you want to giftto or if you are unsure send it to 9006")


filename = "puppet.csv"

names = []
password = []
sell_list = []

# starts color text mode
init()

NewListOfCards = "junk_list.txt"
NewListOfsellCards = "sell_list.txt"
NewErrorSheet = "Error_.txt"


with open("puppet.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        names.append(row[0])
        password.append(row[1])

if os.path.exists(NewListOfCards):
    os.remove(NewListOfCards)
if os.path.exists(NewErrorSheet):
    os.remove(NewErrorSheet)
if os.path.exists(NewListOfsellCards):
    os.remove(NewListOfsellCards)

count = -1

csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT9_527lS9_zLqNhFlRF31X8CDT9bpOlA32exvoNDMNzAP9QOiwO1ZQ7VhRN2K_eGrfQ2Tn38Or-QR8/pub?gid=0&single=true&output=csv"

response = requests.get(csv_url)

card_request_id = []
card_request_season = []
giftie_request = []

with open("dump.csv", "w") as f:
    f.write(response.text)


with open("dump.csv", newline="") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        giftie_request.append(row[0])
        card_request_id.append(row[1])
        card_request_season.append(row[2])

with open(NewListOfCards, "a+") as f:
    with open(NewListOfsellCards, "a+") as s:
        for each in names:
            giftto = "9006"
            firstTime=False
            count = count + 1
            if each == "9003" or each == "9006" or each == "9001":
                input("STOOOOPPPPPPP")
                continue

            r = requests.get(
                "https://www.nationstates.net/cgi-bin/api.cgi/",
                headers={"User-Agent": UserAgent},
                params={"nationname": each, "q": "cards+deck+info"},
            )
            print(f"{Fore.BLUE}Grabbing {each}+{Style.RESET_ALL}")
            sleep(0.7)
            soup = BeautifulSoup(r.content, "html.parser")
            for card in soup.find_all("card"):
                print(card)
                cardid = card.find("cardid").text
                season = card.find("season").text
                # print(f"{Fore.BLUE}Card ID: {cardid}, Season: {season}")

                r2 = requests.get(
                    "https://www.nationstates.net/cgi-bin/api.cgi/",
                    headers={"User-Agent": UserAgent},
                    params={"cardid": cardid, "season": season, "q": "card+markets"},
                )
                sleep(0.7)
                soup2 = BeautifulSoup(r2.content, "html.parser")

                for stuff in soup2.find_all("card"):
                    CATEGORY = stuff.find("category").text
                    MARKET_VALUE = stuff.find("market_value").text
                    REGION = stuff.find("region")

                    highest_bid = 0
                    markets = soup2.find_all("market")
                    for market in markets:
                        if (
                            market.type.string == "bid"
                            and float(market.price.string) > highest_bid
                        ):
                            highest_bid = float(market.price.string)
                        print("The highest bid is:", highest_bid)

                    isJunk = False
                    print("Checking for junk")
                    if CATEGORY == "common" and float(highest_bid) < 0.50:
                        isJunk = True
                    elif CATEGORY == "uncommon" and float(highest_bid) < 1:
                        isJunk = True
                    elif CATEGORY == "rare" and float(highest_bid) < 1:
                        isJunk = True
                    elif CATEGORY == "ultra-rare" and float(highest_bid) < 1:
                        isJunk = True
                    elif CATEGORY == "epic" and float(highest_bid) < 1:
                        isJunk = True
                    if float(MARKET_VALUE) >= 10:
                        isJunk = False
                    if REGION is not None:
                        REGION = REGION.text
                        # if REGION == "Herta Space Station"
                        # isJunk=False
                        # if REGION == "Testregionia":
                        # isJunk=False

                    # card_request_id = []
                    # card_request_season = []
                    # giftie_request = []
                    card_count_request = 0
                    for each_request in card_request_id:
                        print("Checking requests")
                        print(each_request)
                        print(cardid)
                        if (
                            each_request == cardid
                            and season == card_request_season[card_count_request]
                        ):
                            print(card_count_request)
                            print(giftie_request[card_count_request])
                            giftto = giftie_request[card_count_request]

                    if isJunk:
                        print(
                            f"{Fore.RED}{cardid} Junk with a MV of: {MARKET_VALUE}, highest_bid: {highest_bid}, rarity:{CATEGORY}"
                        )
                        print(Style.RESET_ALL)
                        f.writelines(
                            f"https://www.nationstates.net/nation={each}/page=ajax3/a=junkcard/card={cardid}/season={season}/User_agent={UserAgent}Script=JunkDaJunk/Author_Email=NSWA9002@gmail.com/Author_discord=9003/Author_main_nation=9003/autoclose=1"
                            + "\n"
                        )
                    else:
                        print(
                            f"{Fore.GREEN}SELL card with a MV of: {MARKET_VALUE}, highest_bid: {highest_bid}, rarity:{CATEGORY}"
                        )
                        print(Style.RESET_ALL)
                        if not firstTime:
                            z = requests.get(
                            "https://www.nationstates.net/cgi-bin/api.cgi/",
                            headers={
                                "User-Agent": UserAgent,
                                "X-Password": password[count],
                            },
                            params={
                                "nation": each,
                                "cardid": cardid,
                                "season": season,
                                "to": giftto,
                                "mode": "prepare",
                                "c": "giftcard",
                            })
                            xpin=z.headers["x-pin"]

                            firstTime=True
                        else:
                            z = requests.get(
                            "https://www.nationstates.net/cgi-bin/api.cgi/",
                            headers={
                                "User-Agent": UserAgent,
                                "X-Pin": xpin,
                            },
                            params={
                                "nation": each,
                                "cardid": cardid,
                                "season": season,
                                "to": giftto,
                                "mode": "prepare",
                                "c": "giftcard",
                            },
                            )
                        # print(r.headers)
                        # input(z.text)
                        soup = BeautifulSoup(z.content, "html.parser")
                        # ERROR No Space text based error in <ERROR> tags
                       # ERROR You need <b>0.10</b> to pay the transfer fee to gift this card
                        # ERROR Oh no! {nationName} cannot receive your gift as they have no deck capacity.
                        try:
                            giftToken = soup.find("success").text
                        except (AttributeError, TypeError):
                            print(r.status_code)
                            print(f"ERROR {z.content}")
                            with open(NewErrorSheet, "a+") as a:
                                a.writelines(r.content + "\n")
                            continue
                         # print(r.headers["x-pin"])

                        z2 = requests.get(
                            "https://www.nationstates.net/cgi-bin/api.cgi/",
                            headers={
                                "User-Agent": UserAgent,
                                "X-pin": xpin,
                            },
                            params={
                                "nation": each,
                                "cardid": cardid,
                                "season": season,
                                "token": giftToken,
                                "to": giftto,
                                "mode": "execute",
                                "c": "giftcard",
                            },
                        )
                        if str(z2.status_code) == "200":
                            print(f"{Fore.GREEN} Gifted to {giftto}")
                            print(Style.RESET_ALL)
                            with open(NewListOfsellCards, "a+") as h:
                                h.writelines(
                                    f"https://www.nationstates.net/page=deck/nation={giftto}/card={cardid}/season={season}?sellmode=1"
                                    + "\n"
                                )
                        # 200 is good

