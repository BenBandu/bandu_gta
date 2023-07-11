import ctypes
from .vector import FVec4, FVec3, BVec3


class FMatrix(ctypes.LittleEndianStructure):
	_fields_ = (
		('right', FVec4),
		('forward', FVec4),
		('up', FVec4),
		('location', FVec4)
	)

	def from_compressed_matrix(self, matrix):
		pass

	def as_compressed_matrix(self):
		pass


class CompressedMatrix(ctypes.LittleEndianStructure):
	_fields_ = (
		('location', FVec3),
		('right', BVec3),
		('up', BVec3)
	)

	def from_matrix(self, matrix):
		pass

	def as_matrix(self):
		pass
