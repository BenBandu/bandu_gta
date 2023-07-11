from frame import Frame


class Replay:

	VERSION_GTA3 = 1
	VERSION_GTAVC = 2
	VERSION_GTASA = 3

	VERSIONS = [
		VERSION_GTA3,
		VERSION_GTAVC,
		VERSION_GTASA
	]

	BUFFER_SIZE = 100_000
	BUFFER_COUNT = 8
	BUFFER_MAX_COUNT = 64

	def __init__(self, version):
		self._version = version
		self._frames = []

	@classmethod
	def create_from_file(cls, filepath):
		self = cls(0)
		self.read_from_file(filepath)

	def _get_version_header(self, version=None):
		if version is None:
			version = self._version

		if version == Replay.VERSION_GTA3:
			return b'gta3_7f\x00'
		if version == Replay.VERSION_GTAVC:
			return b'gtaVC7f\x00'
		if version == Replay.VERSION_GTASA:
			return b'gtaSA29\x00'

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
