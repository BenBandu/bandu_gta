import ctypes
from .block import ReplayBlock


class Freeplay(ReplayBlock):
	TYPE = 20
	_fields_ = (
		('index', ctypes.c_uint8),
		('fov', ctypes.c_float),
	)