import ctypes
import math


class Panels(ctypes.LittleEndianStructure):
	_fields_ = (
		('front_left', ctypes.c_uint32, 4),
		('front_right', ctypes.c_uint32, 4),
		('rear_left', ctypes.c_uint32, 4),
		('rear_right', ctypes.c_uint32, 4),
		('windshield', ctypes.c_uint32, 4),
		('front_bumper', ctypes.c_uint32, 4),
		('rear_bumper', ctypes.c_uint32, 4)
	)


class Wheel(ctypes.LittleEndianStructure):
	_fields_ = (
		('angle', ctypes.c_int8),
		('suspension', ctypes.c_uint8 * 4),
		('rotation', ctypes.c_uint8 * 4),
	)

	def get_steering_angle(self):
		return self.angle / 50.0

	def get_suspension(self, index):
		return self.suspensnion[index] / 50.0

	def get_rotation_as_angle(self, index):
		return self.rotation[index] * math.pi / 128.0


class Colors(ctypes.LittleEndianStructure):
	_fields_ = (
		('primary', ctypes.c_uint8),
		('secondary', ctypes.c_uint8),
	)
