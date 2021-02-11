
import requests
import sys
import json
import logging
import pymysql


# tm api
key = [tm api 키]
secret = [tm api secret 키]

# mysql 계정
host = 'localhost'
name = 'root'
password = [아이디]
database = [비번]
port = 3306


def main():

    # mysql 연결하기

    try :
        conn = pymysql.connect(host, user=name, passwd=password, db=database, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error("connect is not ableable")
        sys.exit(1)


    # attraction 데이터 넣기
    for page in range(0,50):
        tms = access_tm(key,page)
        attraction = tms['_embedded']['attractions']

        # print(attraction[19]['classifications'][0]['segment']['name'])

        attraction_list = []

        for size in range(0, 20):
            attraction[size]

            attraction_list.append({
            'name' : attraction[size]['name'],
            'id' : attraction[size]['id'],
            'segment' : attraction[size]['classifications'][0]['segment']['name'],
            'genre' : attraction[size]['classifications'][0]['genre']['name'],
            'sub_genre' : attraction[size]['classifications'][0]['subGenre']['name'],
            'sub_type' : attraction[size]['classifications'][0]['subType']['name'],
            'upcomming_event' : attraction[size]['upcomingEvents']['_total'],

            })
        print(attraction_list)

        # 테이블에 변수 넣기
        for content in attraction_list:
            insert_row(cursor, content, 'attraction')

            conn.commit()





# attraction 접속 및 정보 가져오기
def access_tm(keys, page):
    try:
        endpoint = "https://app.ticketmaster.com/discovery/v2/attractions.json?apikey={0}".format(keys)
        params = {
            'page' : page,
            'source' : 'ticketmaster'
        }

        r = requests.get(url=endpoint, params=params)
        tm_attraction = json.loads(r.text)
    except:
        logging.error('error is occured!')
        sys.exit(1)

    return tm_attraction


# mysql 에 넣을 insert 함수 생성
def insert_row(cursor, data, table):

    placeholder = ', '.join(['%s'] * len(data)) # '%s', '%s', '%s',
    columns = ', '.join(data.keys())
    key_placeholder = ', '.join(['{0}=%s'.format(k) for k in data.keys()])
    sql = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (table, columns, placeholder, key_placeholder)
    cursor.execute(sql, list(data.values())*2)






if __name__ == '__main__':
    main()
