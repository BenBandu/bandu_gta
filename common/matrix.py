import ctypes
from numpy import cross
from .vector import FVec4, FVec3, BVec3


class FMatrix(ctypes.LittleEndianStructure):
	_fields_ = (
		('right', FVec4),
		('forward', FVec4),
		('up', FVec4),
		('location', FVec4)
	)

	@classmethod
	def from_compressed_matrix(cls, matrix):
		self = cls()
		self.right.x = matrix.right.x / 127
		self.right.y = matrix.right.y / 127
		self.right.z = matrix.right.z / 127
		self.forward.x = matrix.up / 127
		self.forward.x = matrix.up / 127
		self.forward.x = matrix.up / 127
		self.up = FVec3(cross(matrix.right.as_list(), matrix.forward.as_list()))
		self.location = matrix.location
		return self

	def compress(self):
		matrix = CompressedMatrix()
		matrix.right.x = 127.0 * self.right.x
		matrix.right.y = 127.0 * self.right.y
		matrix.right.z = 127.0 * self.right.z
		matrix.up.x = 127.0 * self.forward.x
		matrix.up.y = 127.0 * self.forward.y
		matrix.up.z = 127.0 * self.forward.z
		matrix.location = self.location
		return matrix

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

	@classmethod
	def from_matrix(cls, matrix):
		self = cls()
		self.right.x = 127.0 * matrix.right.x
		self.right.y = 127.0 * matrix.right.y
		self.right.z = 127.0 * matrix.right.z
		self.up.x = 127.0 * matrix.forward.x
		self.up.y = 127.0 * matrix.forward.y
		self.up.z = 127.0 * matrix.forward.z
		self.location = matrix.location
		return

	def decompress(self):
		matrix = FMatrix()
		matrix.right.x = self.right.x / 127
		matrix.right.y = self.right.y / 127
		matrix.right.z = self.right.z / 127
		matrix.forward.x = self.up.x / 127
		matrix.forward.y = self.up.y / 127
		matrix.forward.z = self.up.z / 127

		right = matrix.right.as_list()[:3]
		forward = matrix.forward.as_list()[:3]
		up = cross(right, forward).tolist()
		matrix.up = FVec4(*up)

		matrix.location.x = self.location.x
		matrix.location.y = self.location.y
		matrix.location.z = self.location.z
		return matrix
