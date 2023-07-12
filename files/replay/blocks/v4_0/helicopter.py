import ctypes
from .vehicle import Vehicle


class Helicopter(Vehicle):
	TYPE = 16
	_fields_ = (
		('rotor_speed', ctypes.c_float),
	)
