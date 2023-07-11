import ctypes
from .vehicle import Vehicle


class Bike(Vehicle):
	TYPE = 2
	_fields_ = (
		('lean_angle', ctypes.c_uint8),
		('steer_angle', ctypes.c_uint8),
		('_pad2', ctypes.c_uint8 * 2),
	)
