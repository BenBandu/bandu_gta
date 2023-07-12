import ctypes
from .vehicle import Vehicle


class Plane(Vehicle):
	TYPE = 17
	_fields_ = (
		('propeller_speed', ctypes.c_float),
		('unkn', ctypes.c_float),
	)
