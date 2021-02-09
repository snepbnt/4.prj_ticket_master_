
import requests
import sys
import json
import logging
from pymongo import MongoClient


# tm api
key = [부여받은 인증키]
secret = [부여받은 시크릿]

def main():

    # mongoDB 연결
    try:
        mongo = MongoClient("mongodb://localhost:27017/")
        # my_mongo = mongo.list_database_names()
    except:
        logging.error("Can not connect MongoDB")
        sys.exit(1)

    # mongodb 테이블 생성
    my_events = mongo['tm_events']
    my_cols = my_events['events']

    # collections 에 데이터 생성
    event_tbl = my_cols.insert_one(events[0])
    print(event_tbl.inserted_id)

    # 데이터 추가하기

    # rest-api 데이터 가져오기
    for page in range(0, 50):
        tms = access_event(key,page)

        events = tms['_embedded']['events']

        # 중복 데이터를 제외한 다른 새로운 데이터 update 하기
        for size in range(0, 20):
            events[size]
            print(events[size])

            my_cols.update(events[size],events[size], upsert=True)








# events 접속 및 정보 가져오기
def access_event(keys, page):
    try:
        endpoint = "https://app.ticketmaster.com/discovery/v2/events.json?apikey={0}".format(key)
        params = {
            'source' : 'ticketmaster',
            'page' : page
        }
        r = requests.get(url=endpoint, params=params)
        tm_events = json.loads(r.text)
    except:
        logging.error('error is occured!')
        sys.exit(1)

    return tm_events

if __name__ == '__main__':
    main()




