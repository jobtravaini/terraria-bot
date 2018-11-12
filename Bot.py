import time
import discord
import logging.config
import command.CommandMap as CommandMap

LOG_COMMAND_AUTHORIZATION_GRANTED = 'Service {0}: Authorization Granted'
LOG_COMMAND_AUTHORIZATION_DENIED = 'Service {0}: Authorization Denied'
AUTHORIZATION_DENIED_MESSAGE='You do not have the permission to use this command'
LOG_COMMAND_PATTERN = 'User {0} invoked {1} command'
LOG_LOGIN_MESSAGE = 'Logged in. Name: {0} - User ID: {1}'
TOKEN = 'YOUR_TOKEN_HERE'

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

command_map = CommandMap.get_command_map()
client = discord.Client()


def _check_authorization(roles):
    for role in roles:
        if role.name == 'TBotAdmin':
            return True

    return False


def _execute_command(message):
    if message.content in command_map:
        logger.info(LOG_COMMAND_PATTERN.format(message.author, message.content))
        service, is_authorization_required  = command_map.get(message.content)

        if is_authorization_required:
            return _execute_role_based_service(service, message.author.roles)
        else:
            return service()


def _execute_role_based_service(service, roles, *args):
    if _check_authorization(roles):
        logger.info(LOG_COMMAND_AUTHORIZATION_GRANTED.format(service.__name__))
        return service(*args)
    else:
        logger.info(LOG_COMMAND_AUTHORIZATION_DENIED.format(service.__name__))
        return AUTHORIZATION_DENIED_MESSAGE


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    result_message = _execute_command(message)

    if result_message:
        await client.send_message(message.channel, result_message)


@client.event
async def on_ready():
    logger.info(LOG_LOGIN_MESSAGE.format(client.user.name, client.user.id))


while True:
    try:
        client.loop.run_until_complete(client.start(TOKEN))
    except Exception:
        logger.info('Reconnecting...')
        time.sleep(5)
