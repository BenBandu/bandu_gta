import ctypes
from .block import ReplayBlock


class PedHeader(ReplayBlock):
	TYPE = 3
	_fields_ = (
		('index', ctypes.c_uint8),
		('model_id', ctypes.c_uint16),
		('type', ctypes.c_uint32, 8),
	)
