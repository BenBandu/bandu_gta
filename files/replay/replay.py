from .frame import Frame
from . import blocks


class Replay:

	VERSION_III               = 1
	VERSION_VICE_CITY         = 2
	VERSION_SAN_ANDREAS       = 3
	VERSION_SAN_ANDREAS_STEAM = 4

	IDENTIFIER_III               = b'gta3_7f\x00'
	IDENTIFIER_VICE_CITY         = b'gtaVC7f\x00'
	IDENTIFIER_SAN_ANDREAS       = b'GtaSA29\x00'
	IDENTIFIER_SAN_ANDREAS_STEAM = IDENTIFIER_SAN_ANDREAS

	BUFFER_SIZE        = 100_000
	BUFFER_DEFAULT_MAX = 8
	BUFFER_MODDED_MAX  = 64

	def __init__(self, version):
		self._version = version
		self._buffers = []
		self._frames = []
		self._dirty = False

	@classmethod
	def create_from_file(cls, filepath):
		self = cls(0)
		self.load(filepath)

		return self

	def _get_identifier_from_version(self):
		if self._version == self.VERSION_III:
			return self.IDENTIFIER_III
		if self._version == self.VERSION_VICE_CITY:
			return self.IDENTIFIER_VICE_CITY
		if self._version == self.VERSION_SAN_ANDREAS:
			return self.IDENTIFIER_SAN_ANDREAS
		if self._version == self.VERSION_SAN_ANDREAS_STEAM:
			return self.IDENTIFIER_SAN_ANDREAS_STEAM

	def _get_version_from_identifier(self, identifier):
		if identifier == self.IDENTIFIER_III:
			return self.VERSION_III
		elif identifier == self.IDENTIFIER_VICE_CITY:
			return self.VERSION_VICE_CITY
		elif identifier == self.IDENTIFIER_SAN_ANDREAS:
			if self._is_steam_version():
				return self.VERSION_SAN_ANDREAS_STEAM

			return self.VERSION_SAN_ANDREAS

		raise TypeError('Unknown replay format')

	def load(self, filepath):
		with open(filepath, 'rb') as file:
			file.seek(0, 2)
			file_size = file.tell()
			file.seek(0)

			identifier = file.read(8)
			while file.tell() < file_size:
				data = file.read(Replay.BUFFER_SIZE)
				self._buffers.append(bytearray(data))

		self._version = self._get_version_from_identifier(identifier)
		self._create_frames_from_buffers()

		self._dirty = False

	def save(self, filepath):
		with open(filepath, 'wb') as file:
			file.write(self._get_identifier_from_version())
			for buffer in self._buffers:
				file.write(buffer)

	def _create_frames_from_buffers(self):
		ReplayBlock = blocks.ReplayBlockBase.get_version(self._version)
		frame = Frame(self._version)
		for buffer in self._buffers:
			offset = 0

			while offset <= Replay.BUFFER_SIZE - 16:
				block = ReplayBlock.create_from_buffer(buffer, offset)
				offset += block.get_size()

				frame.set(block.TYPE, block)

				if block.TYPE == ReplayBlock.TYPE_FRAME_END:
					self._frames.append(frame)
					frame = Frame(self._version)
				elif block.TYPE == ReplayBlock.TYPE_END:
					break

	def _is_steam_version(self):
		"""
		Determine if the current replay is the steam version of San Andreas.
		"""
		if not self._buffers:
			raise ValueError('Can not determine if replay is steam version, as there is no data in the buffer')

		# Read the data as the normal San Andreas version, as it will allow us to detect any deviations
		ReplayBlock = blocks.ReplayBlockBase.get_version(Replay.VERSION_SAN_ANDREAS)
		buffer = self._buffers[0]
		offset = 0

		# To determine if it is the steam version, we have to find the first General block in our data and read past it.
		is_general_block = False
		while not is_general_block:
			block = ReplayBlock.create_from_buffer(buffer, offset)
			offset += block.get_size()

			is_general_block = block.TYPE == ReplayBlock.TYPE_GENERAL

		# Since the general block is 4 bytes longer in the steam version, we can determine which version we have by
		# checking if the Clock block immediately follows. If it doesn't, this is the steam version.
		block = ReplayBlock.create_from_buffer(buffer, offset)
		return block.TYPE != ReplayBlock.TYPE_CLOCK


	@property
	def version(self):
		return self._version

	@version.setter
	def version(self, value):
		# TODO: Implement some sort of conversion?
		pass

	@property
	def size(self):
		return len(self._buffers) * Replay.BUFFER_SIZE + 8
