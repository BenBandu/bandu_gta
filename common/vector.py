import ctypes


class VectorBase(ctypes.LittleEndianStructure):
	_fields_ = []

	def as_list(self):
		length = ctypes.sizeof(self) // ctypes.sizeof(self._fields_[0][1])
		array = (ctypes.c_float * length).from_buffer_copy(self)
		return [v for v in array]

	def __getitem__(self, index):
		name, _type = self.__class__._fields_[index]
		return getattr(self, name)

	def __setitem__(self, index, value):
		name, _type = self.__class__._fields_[index]
		setattr(self, name, value)


class FVec3(VectorBase):
	_fields_ = (
		('x', ctypes.c_float), ('y', ctypes.c_float), ('z', ctypes.c_float),
	)


class FVec4(VectorBase):
	_fields_ = (
		('x', ctypes.c_float), ('y', ctypes.c_float), ('z', ctypes.c_float), ('w', ctypes.c_float),
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

	def as_list(self):
		length = ctypes.sizeof(self) // ctypes.sizeof(ctypes.c_int8)
		array = (ctypes.c_int8 * length).from_buffer_copy(self)
		return [v for v in array]


class SVec3(ctypes.LittleEndianStructure):
	_fields_ = (
		('x', ctypes.c_int16), ('y', ctypes.c_int16), ('z', ctypes.c_int16),
	)

	def as_list(self):
		length = ctypes.sizeof(self) // ctypes.sizeof(ctypes.c_int16)
		array = (ctypes.c_int16 * length).from_buffer_copy(self)
		return [v for v in array]
