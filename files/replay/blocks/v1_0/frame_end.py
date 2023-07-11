import ctypes
from .block import ReplayBlock


class FrameEnd(ReplayBlock):
	TYPE = 7
	_fields_ = (
		('_pad', ctypes.c_uint8 * 3),
	)
