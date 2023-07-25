import ctypes
from .....common.vector import BVec3
from .....common.matrix import CompressedMatrix
from .block import ReplayBlock
from ..common import Panels, Wheel, Colors


class Vehicle(ReplayBlock):
	TYPE = 1
	_fields_ = (
		('index', ctypes.c_uint8),
		('health', ctypes.c_uint8),
		('speed', ctypes.c_uint8),
		('matrix', CompressedMatrix),
		('door_angles', ctypes.c_int8 * 2),
		('model_id', ctypes.c_uint16),
		('panels', Panels),
		('velocity', BVec3),
		('wheel', Wheel),
		('door_status', ctypes.c_uint8),
		('colors', Colors),
	)