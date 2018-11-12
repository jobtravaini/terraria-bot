import requests

# BASE
TOKEN = None
USERNAME = 'tbot'
PASSWORD = 'admin'

# SERVICES
SERVER_URL = 'http://127.0.0.1:7878'

RESTART_SERVER_SERVICE = SERVER_URL + '/v2/server/off'
PLAYER_LIST_SERVICE = SERVER_URL + '/v2/players/list'
TEST_TOKEN_SERVICE = SERVER_URL + '/tokentest'
SAVE_WORLD_SERVICE = SERVER_URL + '/v2/world/save'
RAW_CMD_SERVICE = SERVER_URL + '/v3/server/rawcmd'
STATUS_SERVICE = SERVER_URL + '/status'
LOGIN_SERVICE = SERVER_URL + '/v2/token/create'

# MESSAGING
SERVER_RESTARTING_MESSAGE = 'The Server is restarting...'
CRITICAL_ERROR_MESSAGE = 'Error. Please, validate with your server provider'
EMPTY_SERVER_MESSAGE = 'Empty Server'
WORLD_SAVED_MESSAGE = 'World Saved'
NIGHT_TIME_MESSAGE = 'Setting Server time to Night (19:30 PM)'
BLOOD_MOON_MESSAGE = 'The Server is now running a Blood Moon Event'
FULL_MOON_MESSAGE = 'The Server is now Full Moon Phase'
SANDSTORM_MESSAGE = 'Sandstorm: {0}'
DAY_TIME_MESSAGE = 'Setting Server time to Day (04:30 AM)'
ECLIPSE_MESSAGE = 'The Server is now running an Eclipse Event'
RESTART_MESSAGE = 'The Server will be restarted'
ANGLER_MESSAGE = 'Angler has new quests now'
GENERIC_ERROR = 'Error. Please, restart the server'
RAIN_MESSAGE = 'Raining: {0}'
STATUS_MESSAGE = 'Server Name: {0}\n' \
                 'Players: {1}\n' \
                 'Running for: {2}'

# Help Message
HELP_SERVICE_MESSAGE = 'Services:\n' \
                       '!ip - returns the Server IP\n' \
                       '!status - returns the Server Status\n' \
                       '!angler - reset Angler\'s Quest\n' \
                       '\n' \
                       'Admin Services:\n' \
                       '!bloodmoon - invoke Blood Moon event\n' \
                       '!sandstorm - create sandstorms\n' \
                       '!eclipse - invoke Eclipse event\n' \
                       '!restart - restart the Server\n' \
                       '!night - set the time to Night Time (19:30 PM)\n' \
                       '!save - save the World\n' \
                       '!rain - set weather to Rain\n' \
                       '!day - set time to Day Time (04:30 AM)'

# Server State
rain_state = False
sandstorm_state = False


def _consume_service(url, parameters=None):
    if parameters:
        return requests.get(url, params=parameters).json()
    else:
        return requests.get(url, params=_get_token()).json()


def _validate_response(response):
    if response and 'status' in response and response['status'] == '200':
        return True
    else:
        return False


def _get_token():
    global TOKEN

    if TOKEN and _validate_token():
        return {'token': TOKEN}
    else:
        TOKEN = _consume_service(url=LOGIN_SERVICE, parameters={'username': USERNAME, 'password': PASSWORD})['token']
        return {'token': TOKEN}


def _validate_token():
    response = _consume_service(TEST_TOKEN_SERVICE, parameters={'token': TOKEN})

    if _validate_response(response):
        return True
    else:
        return False


def _get_player_list():
    response = _consume_service(PLAYER_LIST_SERVICE)

    if _validate_response(response):
        player_list = list()
        players = response['players']

        for player in players:
            player_list.append(player['nickname'])

        if len(player_list) > 0:
            return ', '.join(player_list)
        else:
            return EMPTY_SERVER_MESSAGE
    else:
        return GENERIC_ERROR


def server_status():
    response = _consume_service(STATUS_SERVICE)

    if _validate_response(response):
        return STATUS_MESSAGE.format(response['world'], _get_player_list(), response['uptime'])
    else:
        return GENERIC_ERROR


def save_world():
    response = _consume_service(SAVE_WORLD_SERVICE)

    if _validate_response(response):
        return WORLD_SAVED_MESSAGE
    else:
        return GENERIC_ERROR


def server_restart():
    token_parameter = _get_token()
    server_parameter = {'confirm': True, 'message': RESTART_MESSAGE, 'nosave': False}
    parameters = {**token_parameter, **server_parameter}

    response = _consume_service(url=RESTART_SERVER_SERVICE, parameters=parameters)

    if _validate_response(response):
        return SERVER_RESTARTING_MESSAGE
    else:
        return CRITICAL_ERROR_MESSAGE


def _invoke_raw_command(server_parameter):
    token_parameter = _get_token()
    parameters = {**token_parameter, **server_parameter}

    return _consume_service(RAW_CMD_SERVICE, parameters=parameters)


def server_night_time():
    server_parameter = {'cmd': '/time 19:30'}
    response = _invoke_raw_command(server_parameter=server_parameter)

    if _validate_response(response):
        return NIGHT_TIME_MESSAGE
    else:
        return CRITICAL_ERROR_MESSAGE


def server_day_time():
    server_parameter = {'cmd': '/time 04:30'}
    response = _invoke_raw_command(server_parameter=server_parameter)

    if _validate_response(response):
        return DAY_TIME_MESSAGE
    else:
        return CRITICAL_ERROR_MESSAGE


def server_eclipse():
    server_parameter = {'cmd': '/eclipse'}
    response = _invoke_raw_command(server_parameter=server_parameter)

    if _validate_response(response):
        return ECLIPSE_MESSAGE
    else:
        return CRITICAL_ERROR_MESSAGE


def server_full_moon():
    server_parameter = {'cmd': '/fullmoon'}
    response = _invoke_raw_command(server_parameter=server_parameter)

    if _validate_response(response):
        return FULL_MOON_MESSAGE
    else:
        return CRITICAL_ERROR_MESSAGE


def server_rain():
    global rain_state

    if rain_state:
        command = 'stop'
    else:
        command = 'start'

    server_parameter = {'cmd': '/rain {0}'.format(command)}
    response = _invoke_raw_command(server_parameter=server_parameter)

    if _validate_response(response):
        rain_state = not rain_state
        return RAIN_MESSAGE.format(rain_state)
    else:
        return CRITICAL_ERROR_MESSAGE


def server_sandstorm():
    global sandstorm_state

    if sandstorm_state:
        command = 'stop'
    else:
        command = 'start'

    server_parameter = {'cmd': '/sandstorm {0}'.format(command)}
    response = _invoke_raw_command(server_parameter=server_parameter)

    if _validate_response(response):
        sandstorm_state = not sandstorm_state
        return SANDSTORM_MESSAGE.format(sandstorm_state)
    else:
        return CRITICAL_ERROR_MESSAGE


def server_blood_moon():
    server_parameter = {'cmd': '/bloodmoon'}
    response = _invoke_raw_command(server_parameter=server_parameter)

    if _validate_response(response):
        return BLOOD_MOON_MESSAGE
    else:
        return CRITICAL_ERROR_MESSAGE


def server_clear_angler():
    server_parameter = {'cmd': '/clearangler'}
    response = _invoke_raw_command(server_parameter=server_parameter)

    if _validate_response(response):
        return ANGLER_MESSAGE
    else:
        return CRITICAL_ERROR_MESSAGE


def server_help():
    return HELP_SERVICE_MESSAGE
