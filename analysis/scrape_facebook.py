import re, sys, requests, datetime, csv

sys.path.append('/home/david/facebook-scraper')

import facebook_scraper

usgs_base_url = 'http://waterservices.usgs.gov/nwis/iv/?site=14123500&format=json'

with open('gauge_data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['datetime','husum_ft','usgs_ft','usgs_cfs'])
    for post in facebook_scraper.get_posts('whitesalmonriverathusum', pages=1000):
        # Find the five characters before various represnetation of feet
        # (Note that this will only find the first instance in the post)
        text_before_feet = post['text']
        foot_markers = ['\'','’','ish','ft','Ft','FT','feet','Feet','FEET','on the stick']
        for foot_marker in foot_markers:
            text_before_feet = text_before_feet.split(foot_marker)[0]
        text_before_feet = text_before_feet[-5:]
        # Find sequences of integers within that text
        numbers = re.findall("([0-9]+)", text_before_feet)
        if len(numbers) < 1:
            print('No height found in post')
            print(post['text'])
            continue
        elif len(numbers) == 1:
            height_ft = float(numbers[0])
        elif len(numbers) == 2:
            height_ft = float(numbers[0]+ '.' + numbers[1])
        else:
            print('Error: invalid post format')
            print(post['text'])
            continue
        if (height_ft > 10.0):
            print('invalid height - too high')
            continue
        elif (height_ft < 0.2):
            print('invalid height - too low')
            continue
    
        time = post['time']
        try:
            request_datetime = '&startDT=' + time.isoformat() + '&endDT=' + (time + datetime.timedelta(hours=6.0)).isoformat()
            request_string = usgs_base_url + request_datetime
            r = requests.get(request_string)
            usgs_json = r.json()['value']['timeSeries']
            for data_series in usgs_json:
                if data_series['variable']['variableCode'][0]['value'] == '00060':
                    usgs_cfs = data_series['values'][0]['value'][0]['value']
                elif data_series['variable']['variableCode'][0]['value'] == '00065':
                    usgs_height_ft = data_series['values'][0]['value'][0]['value']
            print(time,height_ft,usgs_height_ft,usgs_cfs)
            writer.writerow([time,height_ft,usgs_height_ft,usgs_cfs])
        except Exception as e:
            print(e)