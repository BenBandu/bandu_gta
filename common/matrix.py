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

	def as_list(self, column_major=False):

		if column_major:
			return [
				[self.right.x, self.forward.x, self.up.x, self.location.x],
				[self.right.y, self.forward.y, self.up.y, self.location.y],
				[self.right.z, self.forward.z, self.up.z, self.location.z],
				[self.right.w, self.forward.w, self.up.w, self.location.w],
			]

		return [
			self.right.as_list(),
			self.forward.as_list(),
			self.up.as_list(),
			self.location.as_list(),
		]


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
