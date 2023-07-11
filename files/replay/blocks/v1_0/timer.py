import ctypes
from .block import ReplayBlock


class Timer(ReplayBlock):
	TYPE = 8
	_fields_ = (
		('timer', ctypes.c_uint32),
	)

