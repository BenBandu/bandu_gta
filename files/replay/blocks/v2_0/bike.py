import ctypes
from .block import ReplayBlock
from .....common.matrix import CompressedMatrix
from .....common.vector import BVec3
from ..common import Wheel, Colors


class Bike(ReplayBlock):
	TYPE = 2
	_fields_ = (
		('index', ctypes.c_uint8),
		('health', ctypes.c_uint8),
		('speed', ctypes.c_uint8),
		('matrix', CompressedMatrix),
		('door_angles', ctypes.c_int8 * 2),
		('model_id', ctypes.c_uint16),
		('velocity', BVec3),
		('wheel', Wheel),
		('colors', Colors),
		('lean_angle', ctypes.c_int8),
		('steer_angle', ctypes.c_int8),
	)