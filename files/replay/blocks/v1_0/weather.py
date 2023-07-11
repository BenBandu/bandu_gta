import ctypes
from .block import ReplayBlock


class Weather(ReplayBlock):
	TYPE = 6
	_fields_ = (
		('old', ctypes.c_uint8),
		('new', ctypes.c_uint8),
		('blend', ctypes.c_float)
	)
