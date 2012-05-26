
class ControlGw(object):
	port = 8091
	bind_hostname = 'localhost'

	command_id = {
		'SetRoll': 1,
		'SetPitch': 2,
		'Ping': 3,
		'SetY': 4,
		'SetYaw': 5,
		'Off': 6,
		'On': 7,
		'SetPGains': 8,
		'SetIGains': 9,
		'SetDGains': 10,
		'SetAttenSetpoint': 11,
		'SetLogLevel': 12,
		'SetStateSendInterval': 13,
		'SetSetpoint': 14,
		}

	response_id = {
		'Pong': 1
	}

max_atten = 1.0

