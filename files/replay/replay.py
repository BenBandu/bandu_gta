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

	BLOCKS = {
		VERSION_III: blocks.v1_0,
		VERSION_VICE_CITY: blocks.v2_0,
		VERSION_SAN_ANDREAS: blocks.v3_0,
		VERSION_SAN_ANDREAS_STEAM: blocks.v4_0,
	}

	def __init__(self, version):
		self._version = version
		self._buffers = []
		self._frames = []
		self._dirty = False
		self.blocks = Replay.BLOCKS[self._version]

	@classmethod
	def create_from_file(cls, filepath):
		self = cls(1)
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

		version = self._get_version_from_identifier(identifier)
		self._update_version(version)
		self._create_frames_from_buffers()

		self._dirty = False

	def save(self, filepath):
		if self._dirty:
			self._rebuild_buffers()

		with open(filepath, 'wb') as file:
			file.write(self._get_identifier_from_version())
			for buffer in self._buffers:
				file.write(buffer)

	def _create_frames_from_buffers(self):
		frame = Frame(self._version)
		for buffer in self._buffers:
			offset = 0

			while offset <= Replay.BUFFER_SIZE - 16:
				block = self.blocks.ReplayBlock.create_from_buffer(buffer, offset)
				offset += block.get_size()

				if block.TYPE == self.blocks.ReplayBlock.TYPE_END:
					break
				elif block.TYPE == self.blocks.ReplayBlock.TYPE_FRAME_END:
					self._frames.append(frame)
					frame = Frame(self._version)
				else:
					frame.set_block(block.TYPE, block)

	def _is_steam_version(self):
		"""
		Determine if the current replay is the steam version of San Andreas.
		"""
		if not self._buffers:
			raise ValueError('Can not determine if replay is steam version, as there is no data in the buffer')

		# Read the data as the normal San Andreas version, as it will allow us to detect any deviations
		ReplayBlock = Replay.BLOCKS[Replay.VERSION_SAN_ANDREAS].ReplayBlock
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

	def _rebuild_buffers(self):
		if not self._frames:
			self._buffers = []
			return

		new_buffers = [bytearray()]
		for frame in self._frames:
			framebuffer = new_buffers[-1]
			if len(framebuffer) + frame.get_size() > Replay.BUFFER_SIZE - 16:
				# Frame can't fit in the current buffer, so we finish writing it by adding an end block
				# and adding the remaining size, so it becomes the correct buffer size
				framebuffer += self.blocks.End()
				framebuffer += bytearray(Replay.BUFFER_SIZE - len(framebuffer))

				# Then we create a new buffer
				new_buffers.append(bytearray())
				framebuffer = new_buffers[-1]

			frame_data = frame.get_frame_data()

			framebuffer += frame_data.get_block(self.blocks.ReplayBlock.TYPE_GENERAL, self.blocks.General())
			framebuffer += frame_data.get_block(self.blocks.ReplayBlock.TYPE_CLOCK, self.blocks.Clock())
			framebuffer += frame_data.get_block(self.blocks.ReplayBlock.TYPE_WEATHER, self.blocks.Weather())
			framebuffer += frame_data.get_block(self.blocks.ReplayBlock.TYPE_TIMER, self.blocks.Timer())

			for vehicle_type in self.blocks.ReplayBlock.get_vehicles_types():
				for vehicle_block in frame_data.get_block(vehicle_type, []):
					framebuffer += vehicle_block

			header_map = {}
			for header_block in frame_data.get_block(self.blocks.ReplayBlock.TYPE_PED_HEADER, []):
				header_map[header_block.index] = header_block

			for ped_block in frame_data.get_block(self.blocks.ReplayBlock.TYPE_PED, []):
				if ped_block.index in header_map:
					framebuffer += header_map[ped_block.index]
				framebuffer += ped_block

			for trace_block in frame_data.get_block(self.blocks.ReplayBlock.TYPE_BULLET_TRACE, []):
				framebuffer += trace_block

			if self._version >= Replay.VERSION_VICE_CITY:
				framebuffer += frame_data.get_block(self.blocks.ReplayBlock.TYPE_MISC, self.blocks.Misc())

				for particle_block in frame_data.get_block(self.blocks.ReplayBlock.TYPE_PARTICLE, []):
					framebuffer += particle_block

				if self._version >= Replay.VERSION_SAN_ANDREAS:

					for vehicle_deleted_block in frame_data.get_block(self.blocks.ReplayBlock.TYPE_VEHICLE_DELETED, []):
						framebuffer += vehicle_deleted_block

					for ped_deleted_block in frame_data.get_block(self.blocks.ReplayBlock.TYPE_PED_DELETED, []):
						framebuffer += ped_deleted_block

					for clothes_block in frame_data.get_block(self.blocks.ReplayBlock.TYPE_CLOTHES, []):
						framebuffer += clothes_block

			framebuffer += self.blocks.FrameEnd()

		self._frames = []
		self._buffers = new_buffers
		self._create_frames_from_buffers()

	def _update_version(self, version):
		self._version = version
		self.blocks = self.BLOCKS[version]

	def get_version(self):
		return self._version

	def get_size(self):
		return len(self._buffers) * Replay.BUFFER_SIZE + 8

	def get_frames(self):
		return self._frames
