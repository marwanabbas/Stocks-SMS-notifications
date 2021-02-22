import requests
from twilio.rest import Client

SMS_FEATURE = True
TARGET_PHONE_NUMBER = "your targeted phone number"
TWILIO_PHONE_NUMBER = "your twilio phone number"

STOCK = "TSLA"
PERCENTAGE_CHANGE = 3

STOCKS_END_POINT = "https://www.alphavantage.co/query"
NEWS_END_POINT = "https://newsapi.org/v2/everything"

TWILIO_SID = "your twilio SID here"
TWILIO_AUTH_TOKEN = "your twilio auth token here"

NEWS_API_KEY = "Insert Your news api key here"
STOCKS_API_KEY = "Insert Your stocks api key here"

stocks_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCKS_API_KEY
}

news_parameters = {
    "q": STOCK,
    "apiKey": NEWS_API_KEY
}


def check_price_movement(one_day_ago, two_days_ago):

    if one_day_ago > two_days_ago:
        price_increase_amt = one_day_ago - two_days_ago
        return round((price_increase_amt / two_days_ago) * 100, 2)

    elif one_day_ago < two_days_ago:
        price_decrease_amt = two_days_ago - one_day_ago
        return round((price_decrease_amt / one_day_ago) * 100, 2)
    else:
        return 0


client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

stocks_response = requests.get(STOCKS_END_POINT, params=stocks_parameters)
stocks_response.raise_for_status()
stock_data = stocks_response.json()

news_response = requests.get(NEWS_END_POINT, news_parameters)
news_response.raise_for_status()
news_data = list(news_response.json()["articles"])
top_articles = (news_data[0], news_data[1], news_data[2])


days_list = list(stock_data["Time Series (Daily)"])
two_previous_days = (days_list[1], days_list[2])

yesterday_price = float(stock_data["Time Series (Daily)"][two_previous_days[0]]["4. close"])
day_before_yesterday_price = float(stock_data["Time Series (Daily)"][two_previous_days[1]]["4. close"])

print(yesterday_price)
print(day_before_yesterday_price)

percentage = check_price_movement(yesterday_price, day_before_yesterday_price)

if percentage > PERCENTAGE_CHANGE:
    print(f"{percentage}% change in {STOCK} stock price. Attempting to send a text-message now!")
    if SMS_FEATURE is True:
        message = client.messages.create(to=TARGET_PHONE_NUMBER, from_=TWILIO_PHONE_NUMBER,
                                         body=f"{STOCK}: {percentage}%\n{top_articles[0]['description']}")
        print(message.status)
else:
    print(f"{percentage}% change in {STOCK} stock price.")
