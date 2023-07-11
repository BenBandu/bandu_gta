import ctypes
import zlib
from .block import ReplayBlock


class _Models(ctypes.LittleEndianStructure):
	_fields_ = (
		('torso', ctypes.c_uint32),
		('head', ctypes.c_uint32),
		('hands', ctypes.c_uint32),
		('legs', ctypes.c_uint32),
		('feet', ctypes.c_uint32),
		('chain', ctypes.c_uint32),
		('watch', ctypes.c_uint32),
		('shades', ctypes.c_uint32),
		('hat', ctypes.c_uint32),
		('special', ctypes.c_uint32),
	)


class _Textures(ctypes.LittleEndianStructure):
	_fields_ = (
		('torso', ctypes.c_uint32),
		('head', ctypes.c_uint32),
		('legs', ctypes.c_uint32),
		('feet', ctypes.c_uint32),
		('tattoo_arm_upper_left', ctypes.c_uint32),
		('tattoo_arm_lower_left', ctypes.c_uint32),
		('tattoo_arm_upper_right', ctypes.c_uint32),
		('tattoo_arm_lower_right', ctypes.c_uint32),
		('tattoo_back', ctypes.c_uint32),
		('tattoo_chest_left', ctypes.c_uint32),
		('tattoo_chest_right', ctypes.c_uint32),
		('tattoo_stomach', ctypes.c_uint32),
		('tattoo_back_lower', ctypes.c_uint32),
		('chain', ctypes.c_uint32),
		('watch', ctypes.c_uint32),
		('shades', ctypes.c_uint32),
		('hat', ctypes.c_uint32),
		('special', ctypes.c_uint32),
	)


class Clothes(ReplayBlock):
	TYPE = 19
	_fields_ = (
		('_pad', ctypes.c_uint8 * 3),
		('models', _Models),
		('textures', _Textures),
		('fat', ctypes.c_uint16),
		('muscle', ctypes.c_uint16)
	)
