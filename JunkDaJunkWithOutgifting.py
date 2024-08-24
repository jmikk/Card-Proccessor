import requests
from time import sleep
from bs4 import BeautifulSoup
import csv
import os
from colorama import init, Fore, Back, Style
import sys


print("Version 3")

Password = "************"
cardid = ""
season = ""
from2 = ""
UserAgent = "9003"
giftto = "9006"


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
#this is a blank spreadsheet you can replace with your own if you want to send certain cards to certain places.
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRzOEHnUceACPdpzIWFFOZZmQX4bVNHc_FEu-eN9XsbagcJa9hzm1XaCBaUXy5j71vk1YZI0avQjiph/pub?gid=0&single=true&output=csv"

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
                            f"https://www.nationstates.net/nation={each}/page=ajax3/a=junkcard/card={cardid}/season={season}/User_agent={UserAgent}/Script=JunkDaJunk/Generated_by=JunkDaJunk/Author_Email=NSWA9002@gmail.com/Author_discord=9003/Author_main_nation=9003/autoclose=1"
                            + "\n"
                        )
                    else:
                        print(
                            f"{Fore.GREEN}SELL card with a MV of: {MARKET_VALUE}, highest_bid: {highest_bid}, rarity:{CATEGORY}"
                        )
                        print(Style.RESET_ALL)
                        s.writelines(
                            f"https://www.nationstates.net/nation={each}/card={cardid}/season={season}/User_agent={UserAgent}Script=JunkDaJunk/Author_Email=NSWA9002@gmail.com/Author_discord=9003/Author_main_nation=9003/"
                            + "\n"
                        )
