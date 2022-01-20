import requests
import pprint
import json
apikey = "PUiYjInntAAZivBoQ1g2IQJtPPDHjH9t"

def get_full_data(searchterm):
    response = requests.get("https://app.ticketmaster.com/discovery/v2/attractions.json?keyword="+searchterm+"&apikey="+apikey)
    if response.json()['page']['totalElements']==0:
        return "error"
    else:
        attraction_id=response.json()['_embedded']['attractions'][0]['id']
        response2 = requests.get("https://app.ticketmaster.com/discovery/v2/events.json?locale=*&size=200&attractionId="+attraction_id+"&apikey="+apikey)
        return response2.json()
def filter_results(response):
    array_of_locations=[]
    i=0
    while i !=len(response['_embedded']['events']):
        try:
            city=(response['_embedded']['events'][i]['_embedded']['venues'][0]['city']['name'])
        except:
            city="null"

        try:
            venue=(response['_embedded']['events'][i]['_embedded']['venues'][0]['name'])
        except:
            venue="null"

        try:
            longitude=(response['_embedded']['events'][i]['_embedded']['venues'][0]['location']['longitude'])
        except:
            longitude="null"

        try:
            latitude=(response['_embedded']['events'][i]['_embedded']['venues'][0]['location']['latitude'])
        except:
            latitude:"null"

        try:
            date=[(response['_embedded']['events'][i]['dates']['start']['localDate'])]
        except:
            date=["null"]

        try:
            time=[(response['_embedded']['events'][i]['dates']['start']['localTime'])]
        except:
            time=["null"]

        try:
            url = [(response['_embedded']['events'][i]['url'])]
        except:
            url = ["null"]

        repeate=False
        repeate_pos=0
        for x in array_of_locations:
            if longitude==x['longitude']:
                repeate=True
                repeate_pos=array_of_locations.index(x)

        if repeate==False:
            thisdict = {
                "city": city,
                "venue": venue,
                "longitude": longitude,
                "latitude": latitude,
                "date":date,
                "time":time,
                "url":url,
            }
            array_of_locations.append(thisdict)
        else:
            array_of_locations[repeate_pos]["date"].append(date[0])
            array_of_locations[repeate_pos]["time"].append(time[0])
            array_of_locations[repeate_pos]["url"].append(url[0])

        i=i+1
    return array_of_locations

def get_data(name):
    fulldata=get_full_data(name)
    if  fulldata!="error":
        filted_data=filter_results(fulldata)
        return filted_data
    else:
        return fulldata
def create_local(name):
    fulldata=get_full_data(name)
    print(fulldata)
    if fulldata != "error":
        with open('data.txt', 'w') as outfile:
            json.dump(fulldata, outfile)
        with open('data.txt') as json_file:
            data = json.load(json_file)
        with open('data_for_map.txt', 'w') as outfile:
            json.dump(filter_results(data), outfile)
        return data
    else:
        return fulldata


if __name__== "__main__" :

    data=create_local("hans zimmer")
    #with open('data.txt') as json_file:
     #   data = json.load(json_file)
    #print(json.dumps(data['_embedded']['events'][0], indent=4, sort_keys=True))
    #for Y in data:
     #   print(Y['url'])
    #print(data['_embedded']['events'][0])
    #plz=filter_results(data)
