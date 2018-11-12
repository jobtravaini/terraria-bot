import tshock.Server as Server
import util.ExternalIP as ExternalIP

_map = dict()

# [ SERVICE , IS_AUTHORIZATION_REQUIRED]
_map['!ip'] = [ExternalIP.get_my_external_ip, False]
_map['!status'] = [Server.server_status, False]
_map['!angler'] = [Server.server_clear_angler, False]
_map['!restart'] = [Server.server_restart, True]
_map['!save'] = [Server.save_world, True]
_map['!night'] = [Server.server_night_time, True]
_map['!day'] = [Server.server_day_time, True]
_map['!eclipse'] = [Server.server_eclipse, True]
_map['!fullmoon'] = [Server.server_full_moon, True]
_map['!bloodmoon'] = [Server.server_blood_moon, True]
_map['!rain'] = [Server.server_rain, True]
_map['!sandstorm'] = [Server.server_sandstorm, True]
_map['!help'] = [Server.server_help, True]


def get_command_map():
    return _map
