import requests
import time
from config import api_key, bot_token, chat_id 

threshold = 3000
time_interval = 5 * 60 

def get_doge_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }
    
    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()

    # extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']

def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the msg
    requests.get(url)

def main():
    price_list = []

    while True:
        price = get_doge_price()
        price_list.append(price)

        if price < threshold:
            send_message(chat_id=chat_id, msg=f'BTC Price Drop Alert: {price}')   

        if len(price_list) > 6:
            send_message(chat_id=chat_id, msg=f'latest prices: {price_list}')

            price_list = []

            time.sleep(time_interval)

if __name__ == '__main__':
    main()