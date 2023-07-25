import ctypes
from .block import ReplayBlock
from .....common.matrix import CompressedMatrix


class _StoredAnimationState(ctypes.LittleEndianStructure):
	_fields_ = (
		('first_anim_id', ctypes.c_uint8),
		('first_time', ctypes.c_uint8),
		('first_speed', ctypes.c_uint8),
		('second_anim_id', ctypes.c_uint8),
		('second_time', ctypes.c_uint8),
		('second_speed', ctypes.c_uint8),
		('second_blend', ctypes.c_uint8),
		('third_anim_id', ctypes.c_uint8),
		('third_time', ctypes.c_uint8),
		('third_speed', ctypes.c_uint8),
		('third_blend', ctypes.c_uint8),
	)


class Ped(ReplayBlock):
	TYPE = 3
	_fields_ = (
		('index', ctypes.c_uint8),
		('heading', ctypes.c_int8),
		('vehicle_index', ctypes.c_int8),
		('animation_state', _StoredAnimationState),
		('matrix', CompressedMatrix),
		('group_id', ctypes.c_int8),
		('weapon_model', ctypes.c_uint8),
	)
