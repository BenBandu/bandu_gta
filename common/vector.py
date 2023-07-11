import ctypes


class FVec3(ctypes.LittleEndianStructure):
	_fields_ = (
		('x', ctypes.c_float), ('y', ctypes.c_float), ('z', ctypes.c_float),
	)


class FVec4(FVec3):
	_fields_ = (
		('w', ctypes.c_float),
	)


class RGB(ctypes.LittleEndianStructure):
	_fields_ = (
		('r', ctypes.c_uint8), ('g', ctypes.c_uint8), ('b', ctypes.c_uint8)
	)


class RGBA(RGB):
	_fields_ = (
		('a', ctypes.c_uint8),
	)


class BVec3(ctypes.LittleEndianStructure):
	_fields_ = (
		('x', ctypes.c_int8), ('y', ctypes.c_int8), ('z', ctypes.c_int8),
	)


class SVec3(ctypes.LittleEndianStructure):
	_fields_ = (
		('x', ctypes.c_int16), ('y', ctypes.c_int16), ('z', ctypes.c_int16),
	)