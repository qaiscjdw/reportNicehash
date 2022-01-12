import colorama, os, requests , json , datetime, arrow, sys
from time import sleep
from bs4 import BeautifulSoup
from colorama import Fore, Style
from telethon import TelegramClient, client

os.system('cls' if os.name=='nt' else 'clear')
colorama.init(autoreset=True)
hijau = Style.RESET_ALL+Style.BRIGHT+Fore.GREEN
hijau2 = Style.NORMAL+Fore.GREEN
putih = Style.RESET_ALL
abu = Style.DIM+Fore.WHITE
ungu = Style.RESET_ALL+Style.BRIGHT+Fore.MAGENTA
ungu2 = Style.NORMAL+Fore.MAGENTA
yellow = Style.RESET_ALL+Style.BRIGHT+Fore.YELLOW
yellow2 = Style.NORMAL+Fore.YELLOW
red = Style.RESET_ALL+Style.BRIGHT+Fore.RED
red2 = Style.NORMAL+Fore.RED


file = open("config.json")
data = json.loads(file.read())
wallet = data["wallet"]
tidur = data["sleep"]
pastUnpaid = 0
strUnpaid = ""

while(1):
    try:
        os.system('cls' if os.name=='nt' else 'clear')
        print(hijau+"#####################################")
        print(hijau+"###                               ###")
        print(hijau+"###   Script Balance Nicehash     ###")
        print(hijau+"###      Script by qaiscjdw       ###")
        print(hijau+"###                               ###")
        print(hijau+"#####################################")

        now = datetime.datetime.now()
        date = now.strftime("%H:%M:%S")
        print(abu+"Time : "+str(date)+"\n")

        url = "https://api2.nicehash.com/main/api/v2/mining/external/"+wallet+"/rigs2"
        c = requests.session()
        ua = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }
        r = c.get(url, headers=ua)

        soup = BeautifulSoup(r.text, "html.parser")
        titip = str(soup)
        data = json.loads(titip)
        profitability = data["totalProfitability"]
        nextPayout = data["nextPayoutTimestamp"]
        wallet = data["btcAddress"]
        unpaid = data["unpaidAmount"]
        worker = data["miningRigs"]
        total = 0

        z = arrow.get(nextPayout[0:-1])
        utc = arrow.utcnow()
        local = z.to('local')


        print(yellow+"Wallet\t\t : "+putih+wallet)
        print(yellow+"Unpaid\t\t : "+putih+unpaid+" BTC")
        print(yellow+"Next Payout\t : "+putih+local.format('YYYY-MM-DD HH:mm:ss'))
        print(yellow+"Worker\t\t : "+putih+str(len(worker))+"\n")


        print(hijau+"############### WORKER ##############\n")
        for wrkr in worker:
            nama = wrkr["name"]
            worker_status = wrkr["minerStatus"]
            speed = wrkr["stats"][0]["speedAccepted"]
            total += speed
            print(yellow+'{:<14}'.format(nama)+hijau+worker_status+"\t"+ungu+str(speed)[:5]+" Mh")
        print(hijau+"Total\t\t\t"+ungu+str(total)[:5]+" Mh\n")
        if float(unpaid) >= float(pastUnpaid):
            pastUnpaid = unpaid
            strUnpaid = str(unpaid)
        else:
            api_id = 1100964
            api_hash = '7f34186fba8e8349c5b32712ff698b29'
            phone_number = "+6283871633028"
            titip = str(pastUnpaid)
            client: TelegramClient = TelegramClient('session/'+phone_number,api_id,api_hash)
            async def main():
                await client.connect()
                await client.send_message(entity="@suckbtcmtfk", message='Setoran Masuk '+strUnpaid+" BTC")
                # await client.send_message(entity="@qaiscjdw", message='Setoran Masuk '+titip+" BTC")
            with client:
                client.loop.run_until_complete(main())
                client.disconnect()
            pastUnpaid = 0
            strUnpaid = ""
        tmp = tidur
        for ulang in range(tidur):
            sys.stdout.write('\r{}'.format(hijau) + "Get new data in "+str(tmp)+" second...")
            sleep(1)
            tmp -= 1
    except Exception as e:
        os.system('cls' if os.name=='nt' else 'clear')
        print(red+e)
        sys.stdout.write('\r{}'.format(hijau) + "Get new data in "+str(tidur)+" second...")
        sleep(tidur)