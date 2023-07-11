import ctypes
from .block import ReplayBlock


class Clock(ReplayBlock):
	TYPE = 5
	_fields_  = (
		('hours', ctypes.c_uint8),
		('minutes', ctypes.c_uint8),
		('_pad1', ctypes.c_uint8),
	)
