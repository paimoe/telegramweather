from flask import Flask, jsonify
app = Flask(__name__)
import requests, json
from botconfig import BASE_URL

@app.route('/')
def hello_world():
    url = BASE_URL + '/getUpdates?offset=991742799'
    r = requests.get(url, headers={'Accept': 'application/json'})
    j = r.json()
    a = j['result'][0]
    for a in j['result']:
        update_id = a['update_id']
        next_update_id = update_id + 1
        msg = a['message']['text']
        reply_to = a['message']['message_id']
        reply_to_user = a['message']['from']['id']

        getweather = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=bc9ef656213e63e9deef18bbfb9068b9&units=metric'.format(msg)
        wr = requests.get(getweather)
        wj = wr.json()
        temp = wj['main']['temp'] # in C

        reply_msg = '{}C in {}, {}'.format(temp, wj['name'], wj['sys']['country'])

        #send reply
        url2 = BASE_URL + '/sendMessage'
        mdata = {'chat_id': reply_to_user, 'text': reply_msg, 'reply_to_message_id': reply_to}
        ismsg = requests.post(url2, data=mdata)

    # Call thing to show that we saw the message
    #return msg
    return jsonify(**j)

if __name__ == '__main__':
    app.run(debug=True)
