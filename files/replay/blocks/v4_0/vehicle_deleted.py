import ctypes
from .block import ReplayBlock


class VehicleDeleted(ReplayBlock):
	TYPE = 13
	_fields_ = (
		('_pad', ctypes.c_uint8),
		('index', ctypes.c_int16)
	)
