import string
import sys
import logging
import json

from flask import Flask, jsonify, has_request_context, copy_current_request_context, request
from flask import Response, request
import requests

try :
    from secret_telegram import *
    from secret_account import *
    from secret_chat_id import *
except :
    from secrets1.secret_telegram_local import *
    from secrets1.secret_account_local import *
    from secrets1.secret_chat_id_local import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask("CLOUD-SQL")



# token = '6142841271:AAHuLlf0JvczVNTaw4k5hq3k29KZnzx4Ask'
token = telegram_token

@app.route('/', methods=['POST', 'GET'])
def index_handler():
    """ Handle a webhook post with no authentication method """
    print(request)
    print(request.values)
    for i in request.args :
        print(i)
    _message_sender(request.data)
    return Response("OK")

@app.route('/basic-auth', methods=['POST'])
def basic_auth_handler():
    """ Handle a webhook post with basic HTTP authentication """
    auth = request.authorization

    if not auth or not _check_basic_auth(auth.username, auth.password):
        error_msg = '401 Could not verify your access level for that URL. You have to login with proper credentials'
        logger.error(error_msg)
        # A correct 401 authentication challenge with the realm specified is required
        return Response(error_msg, 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        logger.info("auth success")
        return Response("OK")

@app.route('/hook', methods=['POST'])
def metrics_handler():
    """ Handle a webhook post with basic HTTP authentication """
    auth = request.authorization

    if not auth or not _check_basic_auth(auth.username, auth.password):
        error_msg = '401 Could not verify your access level for that URL. You have to login with proper credentials'
        logger.error(error_msg)
        # A correct 401 authentication challenge with the realm specified is required
        return Response(error_msg, 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        logger.info("auth success")
        print(request.data)
        print(request.headers)
        datas = request.data.replace(b'\n',b'').replace(b' ',b'').decode('utf-8')
        incident = json.loads(datas)['incident']
        if incident['condition_name'] == "CloudSQLDatabase-SQLServeragentjobs" :
            raw_alert = _data_formatter(incident)
            alert = '<b>☁️ GCP - Alert</b>' + "       " + '\n' + '       <code>Target</code>' + " : " + raw_alert['resource_display_name'] + '\n' + "       <code>description</code> : " + "SQL Server Agent Jobs <u>FAILED</u>"
            print(alert)
        elif incident['condition_name'] == 'Logmatchcondition' :
            raw_alert = _data_formatter_log(incident)
            # ['condition_name', 'policy_name', 'summary']
            alert = '<b>☁️ GCP - Alert</b>' + "       " + '\n' + '       <code>Condition</code>' + " : " + raw_alert['condition_name'] + '\n' + '       <code>Policy Name</code>' + " : " + raw_alert['policy_name'] + '\n' + '       <code>Summary</code>' + " : " + raw_alert['summary'] + '\n'
            print(alert)
        else :
            raw_alert = _data_formatter(incident)
            alert = '<b>☁️ GCP - Alert</b>' + "       " + '\n' + '       <code>Target</code>' + " : " + raw_alert['resource_display_name'] + '\n' + "       <code>description</code> : " + f"<u>{raw_alert['condition_name']}</u> is higher than" + f" <code>{int(float(raw_alert['threshold_value']) * 100)}</code> %" 
            print(alert)
        _message_sender(alert)
        return Response('GG')

# send request to telegram api sendMessage
def _message_sender(message : str) :
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'chat_id' : chat_id, 'text' : message ,'parse_mode' : "HTML"}
    payload2 = {'chat_id' : chat_id_livecheck, 'text' : message ,'parse_mode' : "HTML"}
    session = requests.session()
    session.get(
    f"https://api.telegram.org/bot{token}/sendMessage",
    headers=headers,
    params = payload,
    )
    session.get(
    f"https://api.telegram.org/bot{token}/sendMessage",
    headers=headers,
    params = payload2,
    )
    session.close()

def _data_formatter(incident:bytes):
    # remove '\n' & ' ' & transfer to string
    result = {}
    for key in incident.keys() :
        #if key == 'resource_type_display_name' : # CloudSQLDatabase
        #    result['resource_type_display_name'] = metrics_incident[key]
        if key == 'resource_display_name' : # wkingdb
            result['resource_display_name'] = incident[key]
        elif key == 'threshold_value' : # 0.05
            result['threshold_value'] = incident[key]
        elif key == 'condition_name' : # CloudSQLDatabase-CPUutilization
            result['condition_name'] = incident[key]
        else :
            pass
    return result

def _data_formatter_log(incident:bytes):
    # remove '\n' & ' ' & transfer to string
    result = {}
    main_features = ['condition_name', 'policy_name', 'summary']
    for feature in main_features :
        result[feature] = incident[feature]
    return result


def _check_basic_auth(username, password):
    """This function is called to check if a username / password combination is valid. """
    return username == username and password == password

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8443', debug=True)



