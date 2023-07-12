from .frame import Frame
from . import VERSION_GTA3, VERSION_GTAVC, VERSION_GTASA
from . import REPLAY_BUFFER_SIZE


class Replay:
	VERSIONS = [
		VERSION_GTA3,
		VERSION_GTAVC,
		VERSION_GTASA
	]

	def __init__(self, version):
		self._version = version
		self._frames = []

	@classmethod
	def create_from_file(cls, filepath):
		self = cls(0)
		self.read_from_file(filepath)

		return self

	def _get_version_header(self, version=None):
		if version is None:
			version = self._version

		if version == VERSION_GTA3:
			return b'gta3_7f\x00'
		if version == VERSION_GTAVC:
			return b'gtaVC7f\x00'
		if version == VERSION_GTASA:
			return b'GtaSA29\x00'

	def _get_remaining_buffer_size(self, size):
		return REPLAY_BUFFER_SIZE - (size % REPLAY_BUFFER_SIZE)

	def read_from_file(self, filepath):
		with open(filepath, 'rb') as file:
			file.seek(0, 2)
			file_size = file.tell()
			file.seek(0)

			header = file.read(8)
			for version in Replay.VERSIONS:
				if header == self._get_version_header(version):
					self._version = version
					break
			else:
				raise TypeError('Unknown replay format')

			while file.tell() < file_size:
				frame = Frame(self._version)
				frame.read(file)

				self._frames.append(frame)

	def write_to_file(self, filepath):
		with open(filepath, 'wb') as file:
			file.write(self._get_version_header())

			for frame in self._frames:
				frame.write(file)

			offset = self._get_remaining_buffer_size(file.tell())
			file.seek(offset, 1)

	def get_version(self):
		return self._version

	def get_size(self):
		size = 0
		for frame in self._frames:
			size += frame.get_size()

		# Get the remaining bytes to round to the next buffer

		return size + self._get_remaining_buffer_size(size) + 8
