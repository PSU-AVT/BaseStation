
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
		'On': 7}

	response_id = {
		'Pong': 1
	}

