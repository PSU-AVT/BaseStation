import joystick

class ControlJoystick(joystick.QJoystick):
	def __init__(self, conn_mgr, joystick_file):
		super(ControlJoystick, self).__init__(joystick_file)
		self.connection_manager = conn_mgr

	def joystickEvent(ev):
		if self.connection_manager.is_connected:
			pass

