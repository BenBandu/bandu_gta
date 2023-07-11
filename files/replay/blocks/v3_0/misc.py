import ctypes
from .block import ReplayBlock


class Misc(ReplayBlock):
	TYPE = 12
	_fields_ = (
		('camera_shake_start', ctypes.c_uint32),
		('camera_shake_strength', ctypes.c_float),
		('current_area', ctypes.c_uint8),
		('camera_video', ctypes.c_uint8, 1),
		('camera_lift', ctypes.c_uint8, 1),
	)
