import ctypes
from .block import ReplayBlock
from common.matrix import CompressedMatrix


class _AnimationData(ctypes.LittleEndianStructure):
	_fields = {
		('id', ctypes.c_uint8),
		('time', ctypes.c_uint8),
		('speed', ctypes.c_uint8),
		('group_id1', ctypes.c_uint8),
		('group_id2', ctypes.c_uint8),
	}


class _StoredAnimationState(ctypes.LittleEndianStructure):
	_fields_ = (
		('first', _AnimationData),
		('second', _AnimationData),
		('third', _AnimationData),
	)


class _Flags(ctypes.LittleEndianStructure):
	_fields_ = (
		('is_talking', ctypes.c_uint8, 1),
		('on_valid_poly', ctypes.c_uint8, 1),
		('uses_collision', ctypes.c_uint8, 1),
	)


class Ped(ReplayBlock):
	TYPE = 4
	_fields_ = (
		('index', ctypes.c_uint8),
		('heading', ctypes.c_int8),
		('vehicle_index', ctypes.c_int8),
		('animation_state', _StoredAnimationState),
		('_pad1', ctypes.c_uint8 * 2),
		('matrix', CompressedMatrix),
		('weapon_model', ctypes.c_uint16),
		('group_id', ctypes.c_uint16),
		('contact_brightness', ctypes.c_uint8),
		('flags', _Flags),
		('_pad2', ctypes.c_uint8 * 2),
	)