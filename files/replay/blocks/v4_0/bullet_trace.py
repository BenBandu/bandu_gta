import ctypes
from .block import ReplayBlock
from .....common.vector import FVec3


class BulletTrace(ReplayBlock):
	TYPE = 10
	_fields_ = (
		('_pad', ctypes.c_uint8 * 2),
		('index', ctypes.c_uint8),
		('start', FVec3),
		('end', FVec3),
	)
