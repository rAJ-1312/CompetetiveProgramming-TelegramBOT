import requests
import os
from dotenv import load_dotenv
import time
from get_Time import returnTime,find_remaining_time,startTimeLocal
from datetime import datetime


load_dotenv()

API = os.getenv('API_KEY')

base_url = "https://clist.by/api/v2/contest/"


codes_rid = {
    1: 'Codeforces',
    2: 'Codechef',
    102: 'Leetcode',
    93: 'AtCoder',
    12: 'TopCoder',
    73: 'HackerEarth',
    63: 'HackerRank',
    26: 'Spoj',
    126: 'GeeksforGeeks',
    136: 'CodingNinja'
}



def fetch_data_for_a_resourceID(resource_id):

    # print(type(resource_id))

    global response
    my_headers =   {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/46.0.2490.80'
        } 

    iso_current_date, iso_end_date = returnTime()

    query_params = {
        'username' : '___r___a___j',
        'api_key' : API,
        'resource_id' : resource_id,
        'start__gte' :  iso_current_date,
        'start__lte' :  iso_end_date,
        'format' : 'json'
    }


    flag = True


    while flag:
        try:
            response = requests.get(base_url, params=query_params, headers=my_headers)
            # print(response.status_code)
            data = response.json()
        except Exception:
            # print('Kindly wait for 1 minute.')
            wait = 60
            if(response.status_code==429):
                wait = response.headers['Retry-After']
            time.sleep(int(wait))
        else:
            break


    if data['objects']:
        output = []

        for item in data['objects']:
            stime = startTimeLocal(item['start'])
            temp = datetime.fromisoformat(stime)
            remaining_time = find_remaining_time(temp)
            seconds = item['duration']
            duration = time.strftime('%H:%M', time.gmtime(seconds))
            link = item['href']

            temp = {
                'name' : item['event'],
                'start_time' : stime,
                'starts_in' : remaining_time,
                'duration' :  duration,
                'link' : link
            }

            output.append(temp)

        return output, codes_rid[resource_id]

    else:
        return [], codes_rid[resource_id]


# fetch_data_for_a_resourceID(1)
