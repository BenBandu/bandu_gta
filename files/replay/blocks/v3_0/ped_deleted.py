import ctypes
from .block import ReplayBlock


class PedDeleted(ReplayBlock):
	TYPE = 14
	_fields_ = (
		('_pad', ctypes.c_uint8),
		('index', ctypes.c_int16)
	)
