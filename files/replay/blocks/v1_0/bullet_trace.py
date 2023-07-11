import ctypes
from .block import ReplayBlock
from common.vector import FVec3


class BulletTrace(ReplayBlock):
	TYPE = 9
	_fields_ = (
		('frames', ctypes.c_uint8),
		('lifetime', ctypes.c_uint8),
		('index', ctypes.c_uint8),
		('start', FVec3),
		('end', FVec3),
	)
