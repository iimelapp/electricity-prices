import json
import requests
import dateutil.parser

def average_price(list, start, end):
    price_list = []

    for item in list:
        date_1 = dateutil.parser.isoparse(item["startDate"])
        date_2 = dateutil.parser.isoparse(item["endDate"])
        if  date_1 >= start and date_2 <= end:
            price_list.append(item["price"])
    return  sum(price_list) / len(price_list)


def main():
    response_api = requests.get('https://api.porssisahko.net/v1/latest-prices.json')
    data = response_api.text
    data_obj = json.loads(data)

    start = dateutil.parser.isoparse("2022-12-25T16:22:47Z")
    end = dateutil.parser.isoparse("2022-12-26T16:22:47Z")

    print(f"Average price within given time period {str(start)} - {str(end)} :")
    print(average_price(data_obj["prices"], start, end))

if __name__ == '__main__':
    main()