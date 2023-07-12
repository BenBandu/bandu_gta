import ctypes
from .block import ReplayBlock
from common.vector import BVec3, SVec3, RGBA


class Particle(ReplayBlock):
	TYPE = 11
	_fields_ = (
		('type', ctypes.c_uint8),
		('direction', BVec3),
		('color', RGBA),
		('position', SVec3),
		('size', ctypes.c_float)
	)
