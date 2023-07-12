import ctypes
from .vehicle import Vehicle


class Bmx(Vehicle):
	TYPE = 15
	_fields_ = (
		('lean', ctypes.c_uint8),
		('steer', ctypes.c_uint8),
	)

