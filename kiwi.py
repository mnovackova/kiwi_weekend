import requests
import click
from datetime import datetime
from pprint import pprint
from bs4 import BeautifulSoup

#python kiwi.py --from Brno --to Prague --date 2017-07-22

@click.command()
@click.option('--from', 'from_')
@click.option('--to', 'to' )
@click.option('--date', 'date', help='2017-12-20')
def url(from_, date, to):
    '''Preparing request.'''
    date_parsed =  datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')
    session = requests.Session()
    r = session.get('https://www.regiojet.com/en/')
    print(r.status_code)
    print(r.headers['content-type'])

    id_cities_get = session.get('https://www.studentagency.cz/data/wc/ybus-form/destinations-en.json')
    id_cities_json = id_cities_get.json()

    for destination in id_cities_json['destinations']:
        for city in destination['cities']:
            if city['name'] == from_:
                print(city['id'], city['name'])
                from_id = city['id']

    for destination in id_cities_json['destinations']:
        for city in destination['cities']:
            if city['name'] == to:
                print(city['id'], city['name'])
                to_id = city['id']

    #url = 'https://jizdenky.regiojet.cz/Booking/from/10202002/to/10202003/tarif/REGULAR/departure/20170722/retdep/20170722/return/false?0'
    url = 'https://jizdenky.regiojet.cz/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false?0'.format(from_id, to_id, date_parsed, date_parsed)
    r = session.get(url)
    #url = 'https://jizdenky.regiojet.cz/Booking/from/10202002/to/10202003/tarif/REGULAR/departure/20170722/retdep/20170722/return/false?0-1.IBehaviorListener.0-mainPanel-routesPanel&_=0'
    url = 'https://jizdenky.regiojet.cz/Booking/from/{}/to/{}/tarif/REGULAR/departure/{}/retdep/{}/return/false?0-1.IBehaviorListener.0-mainPanel-routesPanel&_=0'.format(from_id, to_id, date_parsed, date_parsed)
    r = session.get(url)
    print(r.status_code)
    print(r.headers['content-type'])
    print(url)
    #print(r.headers['content-type'])

    print(r.text)

    soup = BeautifulSoup(r.text, 'html.parser')
    time_departure = soup.find_all('div', class_="col_depart gray_gradient", limit=1)
    print(time_departure)
    import pdb; pdb.set_trace()


'''
[{
  "departure": "2017-12-20 12:45:00",
  "arrival": "2017-12-20 15:00:00",
  "from": "Praha",
  "to": "Ostrava",
  "free_seats": 40,
  "price": 100.0,
  "type": "train", # optional (train/bus)
  "from_id": 47374743, # optional (student agency id)
  "to_id": 26383230 # optional (student agency id)
}]
'''


if __name__ == '__main__':
    url()
