from .frame import Frame
from . import VERSION_GTA3, VERSION_GTAVC, VERSION_GTASA, VERSION_STEAM_GTASA
from . import REPLAY_BUFFER_SIZE


class Replay:
	VERSIONS = [
		VERSION_GTA3,
		VERSION_GTAVC,
		VERSION_GTASA,
		VERSION_STEAM_GTASA
	]

	def __init__(self, version):
		self._version = version
		self._frames = []

	@classmethod
	def create_from_file(cls, filepath):
		self = cls(0)
		self.read_from_file(filepath)

		return self

	def _get_header(self):
		if self._version == VERSION_GTA3:
			return b'gta3_7f\x00'
		if self._version == VERSION_GTAVC:
			return b'gtaVC7f\x00'
		if self._version in [VERSION_GTASA, VERSION_STEAM_GTASA]:
			return b'GtaSA29\x00'

	def _get_remaining_buffer_size(self, size):
		return REPLAY_BUFFER_SIZE - (size % REPLAY_BUFFER_SIZE)

	def _handle_potential_steam_version(self, file):
		"""
		Change the version of the replay from GTASA to STEAM_GTASA if we believe the replay comes from steam.

		Replay frames often start with the following blocks: General > Clock > Weather > Timer.
		Because of this we can figure out if the replay we are reading is from the steam copy of san andreas by
		placing the file pointer at byte 96. In a normal SA Replay byte 96 will be the start of the Clock block,
		and so the next value we read should be 6 as that's the Clock block type id, however in the steam version
		the General block seems to be padded by 4 extra bytes.
		"""

		if self._version != VERSION_GTASA:
			return

		file_position = file.tell()

		file.seek(96)
		if file.read(1) != b'\x06':
			self._version = VERSION_STEAM_GTASA

		file.seek(file_position)

	def read_from_file(self, filepath):
		with open(filepath, 'rb') as file:
			file.seek(0, 2)
			file_size = file.tell()
			file.seek(0)

			header = file.read(8)
			for version in Replay.VERSIONS:
				self._version = version
				if header == self._get_header():
					self._handle_potential_steam_version(file)
					break
			else:
				raise TypeError('Unknown replay format')

			while file.tell() < file_size:
				frame = Frame(self._version)
				frame.read(file)

				self._frames.append(frame)

	def write_to_file(self, filepath):
		with open(filepath, 'wb') as file:
			file.write(self._get_header())

			for frame in self._frames:
				is_last_frame = frame is self._frames[-1]
				frame.write(file, is_last_frame)

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
