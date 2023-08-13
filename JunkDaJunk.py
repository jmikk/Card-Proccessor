import requests
from time import sleep
from bs4 import BeautifulSoup
import csv
import os
from colorama import init, Fore, Back, Style

import sys


print("Version 1")

Password = "************"
cardid = ""
season = ""
giftto = "9006"
from2 = ""

UserAgent=input("Please enter your main nation's name: ")
giftto = input("Enter the nation you want to giftto or if you are unsure send it to 9006")
filename="puppet.csv"

names=[]
password=[]
sell_list=[]


#starts color text mode
init()

NewListOfCards="junk_list.txt"
NewListOfsellCards="sell_list.txt"
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
count=-1
with open(NewListOfCards,"a+") as f:
    for each in names:
        count=count+1
        if each == "9003" or each == "9006" or each == "9001":
            input("STOOOOPPPPPPP")
            continue

        r = requests.get('https://www.nationstates.net/cgi-bin/api.cgi/', headers={'User-Agent': UserAgent}, params={'nationname':each, 'q':'cards+deck'})
        print(f"{Fore.BLUE}Grabbing {each}+{Style.RESET_ALL}")
        sleep(.7)
        soup = BeautifulSoup(r.content, "xml")
        for card in soup.find_all("CARD"):
            cardid = card.find("CARDID").text
            season = card.find("SEASON").text
           # print(f"{Fore.BLUE}Card ID: {cardid}, Season: {season}")


            r2 = requests.get('https://www.nationstates.net/cgi-bin/api.cgi/', headers={'User-Agent': UserAgent}, params={'cardid':cardid,'season':season, 'q':'card+markets'})
            sleep(.7)
            soup2 = BeautifulSoup(r2.content, "xml")

            for stuff in soup2.find_all("CARD"):
                CATEGORY = stuff.find("CATEGORY").text
                MARKET_VALUE = stuff.find("MARKET_VALUE").text

                highest_bid = 0
                markets = soup2.find_all('MARKET')
                for market in markets:
                    if market.TYPE.string == 'bid' and float(market.PRICE.string) > highest_bid:
                        highest_bid = float(market.PRICE.string)
                    print('The highest bid is:', highest_bid)

                isJunk = False
                print("Checking for junk")
                if CATEGORY == "common" and float(highest_bid) < .50:
                    isJunk=True 
                elif CATEGORY == "uncommon" and float(highest_bid) < 1:
                    isJunk=True 
                elif CATEGORY == "rare" and float(highest_bid) < 1:
                    isJunk=True 
                elif CATEGORY == "ultra-rare" and float(highest_bid) < 1:
                    isJunk=True 
                elif CATEGORY == "epic" and float(highest_bid) < 1:
                    isJunk=True 
                if float(MARKET_VALUE) >= 10:
                    isJunk=False

                if isJunk:
                    print(f"{Fore.RED}{cardid} Junk with a MV of: {MARKET_VALUE}, highest_bid: {highest_bid}, rarity:{CATEGORY}")
                    print(Style.RESET_ALL)
                    f.writelines(f"https://www.nationstates.net/nation={each}/page=ajax3/a=junkcard/card={cardid}/season={season}/Script=JunkDaJunk/Author_Email=NSWA9002@gmail.com/Author_discord=9003/Author_main_nation=9003/autoclose=1"+"\n")
                else:
                    print(f"{Fore.GREEN}SELL card with a MV of: {MARKET_VALUE}, highest_bid: {highest_bid}, rarity:{CATEGORY}")
                    print(Style.RESET_ALL)
                    z = requests.get('https://www.nationstates.net/cgi-bin/api.cgi/', headers={'User-Agent': UserAgent, 'X-Password':password[count]}, params={'nation':each,'cardid':cardid,'season':season, 'to':giftto,'mode':"prepare" ,'c':'giftcard'})
                    #print(r.headers)
                    #input(z.text)
                    soup = BeautifulSoup(z.content, "xml")
                    #ERROR No Space text based error in <ERROR> tags
                    #ERROR You need <b>0.10</b> to pay the transfer fee to gift this card
                    #ERROR Oh no! {nationName} cannot receive your gift as they have no deck capacity.
                    try:
                        giftToken = soup.find("SUCCESS").text
                    except AttributeError,TypeError:
                        print(r.status_code)
                        print(f"ERROR {r.content}")
                        with open(NewErrorSheet,"a+") as a:
                            a.writelines(r.content+"\n")
                        continue
                    #print(r.headers["x-pin"])

                    z2 = requests.get('https://www.nationstates.net/cgi-bin/api.cgi/', headers={'User-Agent': UserAgent, 'X-pin':z.headers["x-pin"]}, params={'nation':each,'cardid':cardid,'season':season, 'token':giftToken,'to':giftto,'mode':"execute" ,'c':'giftcard'})
                    if str(z2.status_code) == "200":
                        print(f"{Fore.GREEN} Gifted to {giftto}")
                        print(Style.RESET_ALL)
                        with open(NewListOfsellCards,"a+") as h:
                            h.writelines(f"https://www.nationstates.net/page=deck/nation={giftto}/card={cardid}/season={season}?sellmode=1" + "\n")
                    #200 is good





