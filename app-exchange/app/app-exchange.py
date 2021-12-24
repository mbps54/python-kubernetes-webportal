#!/usr/bin/python3
import os
import requests
import redis


###########################    SYSTEM ENVIRONMENT   ############################
DB_NAME_IP = str(os.environ.get("DB_NAME_IP"))
if DB_NAME_IP == "None":
    DB_NAME_IP = "localhost"

API_KEY = str(os.environ.get("API_KEY"))
if DB_NAME_IP == "None":
    API_KEY = "ca0cdd8c332da1840ec1e46a16ece7"

###########################      MAIN FUNCTION      ############################
def get_rates():
    ###########################        GET RATES        ########################
    response = requests.get(
        f"http://api.currencylayer.com/live?access_key={API_KEY}&source=USD&currencies=RUB,TRY&format=1"
    )
    usdrub = ((response.json())["quotes"])["USDRUB"]
    usdtry = ((response.json())["quotes"])["USDTRY"]
    ex_rates = {"usdrub": usdrub, "usdtry": usdtry}

    ###########################    SEND RATES TO DB     ########################
    r = redis.StrictRedis(DB_NAME_IP, 6379, charset="utf-8", decode_responses=True)
    r.hmset("rates", ex_rates)


if __name__ == "__main__":
    get_rates()
