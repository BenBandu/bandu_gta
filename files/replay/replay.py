from .frame import Frame
from .blocks import ReplayBlockBase


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

	MAX_VEHICLE_COUNT = 110
	MAX_PED_COUNT = 140

	def __init__(self, version):
		self._version = version
		self._buffers = []
		self._frames = []
		self._dirty = False
		self._block = ReplayBlockBase.get_version(version)

	@classmethod
	def create_from_file(cls, filepath):
		self = cls(1)
		self.load(filepath)

		return self

	@classmethod
	def create_from_buffers(cls, buffers, version):
		self = cls(version)
		self._buffers = buffers
		self._create_frames_from_buffers()

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
				block = self._block.create_from_buffer(buffer, offset)
				offset += block.get_size()

				if block.TYPE == self._block.TYPE_END:
					break
				elif block.TYPE == self._block.TYPE_FRAME_END:
					self._frames.append(frame)
					frame = Frame(self._version)
				else:
					frame.set_block(block)

	def _is_steam_version(self):
		"""
		Determine if the current replay is the steam version of San Andreas.
		"""
		if not self._buffers:
			raise ValueError('Can not determine if replay is steam version, as there is no data in the buffer')

		# Read the data as the normal San Andreas version, as it will allow us to detect any deviations
		ReplayBlock = ReplayBlockBase.get_version(Replay.VERSION_SAN_ANDREAS)
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

		buffers = []
		buffer = bytearray()
		for frame in self._frames:
			buffer_size = len(buffer)
			if buffer_size + frame.get_size() > Replay.BUFFER_SIZE - 16:
				buffer += bytearray(Replay.BUFFER_SIZE - buffer_size)
				buffers.append(buffer)
				buffer = bytearray()

			frame.write_frame_to_buffer(buffer)

		self._frames = []
		self._buffers = buffers
		self._create_frames_from_buffers()

	def _update_version(self, version):
		self._version = version
		self._block = ReplayBlockBase.get_version(version)

	def get_version(self):
		return self._version

	def get_size(self):
		return len(self._buffers) * Replay.BUFFER_SIZE + 8

	def get_frames(self):
		return self._frames

	def set_dirty(self):
		self._dirty = True

	def get_frame(self, index):
		return self._frames[index]

	def get_buffers(self):
		if self._dirty:
			self._rebuild_buffers()

		return self._buffers

	def add_frame(self, frame):
		self._frames.append(frame)
		self._dirty = True

	def merge_replays(self, other, offset=0, filters=[]):
		if other.get_version() != self.get_version():
			return

		# if the offset is below 0, we technically want the replay to start with the other replay first
		# so instead of doing something fancy, we just call this function on the other replay with this replay
		# as the parameter, and an inverted offset
		if offset < 0:
			return other.merge_replays(self, -offset)

		index_maps = [
			{'vehicles': [], 'peds': []},
			{'vehicles': [], 'peds': []}
		]

		vehicle_counter = 0
		ped_counter = 0

		self_frame_count = len(self._frames)

		other_frames = other.get_frames()
		other_frame_count = len(other_frames)

		merged_replay = Replay(self.get_version())
		for frame_idx in range(max(self_frame_count, other_frame_count)):
			new_frame = Frame(self._version)

			base_frames = [
				self._frames[frame_idx] if frame_idx < self_frame_count else None,
				other_frames[frame_idx] if other_frame_count > frame_idx >= offset else None
			]

			for i, old_frame in enumerate(base_frames):
				if old_frame is None:
					continue

				index_map = index_maps[i]
				filter_map = filters[i]

				if new_frame.get_block(self._block.TYPE_GENERAL) is None:
					for block_type in self._block.get_required_types():
						new_frame.set_block(old_frame.get_block(block_type))

				for vehicle_type in self._block.get_vehicles_types():
					for vehicle in old_frame.get_block(vehicle_type, []):
						old_index = vehicle.index
						if old_index not in filter_map['vehicles']:
							continue

						if old_index in index_map['vehicles']:
							new_index = index_map['vehicles'][old_index]
						else:
							new_index = vehicle_counter
							vehicle_counter += 1
							index_map['vehicles'][old_index] = new_index

						vehicle.index = new_index
						new_frame.set_block(vehicle)

				for ped in old_frame.get_block(self._block.TYPE_PED, []):
					old_index = ped.index
					if old_index not in filter_map['peds']:
						continue

					if old_index in index_map['peds']:
						new_index = index_map['peds'][old_index]
					else:
						new_index = ped_counter
						ped_counter += 1
						index_map['peds'][old_index] = new_index

					ped.index = new_index
					if ped.vehicle_index and ped.vehicle_index in index_map['vehicles']:
						ped.vehicle_index = index_map['vehicles'][ped.vehicle_index]

					new_frame.set_block(ped)

				for ped_header in old_frame.get_block(self._block.TYPE_PED_HEADER, []):
					old_index = ped_header.index
					if old_index not in filter_map['peds']:
						continue

					if old_index in index_map['peds']:
						new_index = index_map['peds'][old_index]
					else:
						new_index = ped_counter
						ped_counter += 1
						index_map['peds'][old_index] = new_index

					ped_header.index = new_index
					new_frame.set_block(ped_header)

				if self._version >= Replay.VERSION_VICE_CITY:
					for particle in old_frame.get_block(self._block.TYPE_PARTICLE, []):
						new_frame.set_block(particle)

			merged_replay.add_frame(new_frame)

		return merged_replay
