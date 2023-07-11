import blocks


class Frame:

	def __init__(self, version):
		self._version = version
		self.blocks = blocks.version_mapping[version]
		self._frame_data = self._init_frame_data()

	def _init_frame_data(self):
		block = self.blocks.ReplayBlock
		frame_data = {
			block.TYPE_VEHICLE: [],
			block.TYPE_PED_HEADER: [],
			block.TYPE_PED: [],
			block.TYPE_GENERAL: self.blocks.General(),
			block.TYPE_CLOCK: self.blocks.Clock(),
			block.TYPE_WEATHER: self.blocks.Weather(),
			block.TYPE_TIMER: self.blocks.Timer(),
			block.TYPE_BULLET_TRACE: []
		}

		if self._version > Replay.VERSION_GTA3:
			frame_data.update({
				block.TYPE_BIKE: [],
				block.TYPE_PARTICLE: [],
				block.TYPE_MISC: self.blocks.Misc(),
			})

		if self._version > Replay.VERSION_GTAVC:
			frame_data.update({
				block.TYPE_VEHICLE_DELETED: [],
				block.TYPE_PED_DELETED: [],
				block.TYPE_BMX: [],
				block.TYPE_HELICOPTER: [],
				block.TYPE_PLANE: [],
				block.TYPE_TRAIN: [],
				block.TYPE_CLOTHES: self.blocks.Clothes()
			})

		return frame_data

	def get(self, key):
		return self._frame_data.get(key, None)

	def set(self, key, value):
		data = self.get(key)
		if data is None:
			return

		if type(value) == type(data):
			self._frame_data[key] = value
		else:
			self._frame_data[key].append(value)

	def _handle_file_position(self, file):
		file_position = file.tell()
		buffer_count = (file_position // Replay.BUFFER_SIZE)
		buffer_offset = file_position % Replay.BUFFER_SIZE
		buffer_excess = Replay.BUFFER_SIZE - buffer_offset

		if self.get_size() > buffer_excess:
			if buffer_count == Replay.BUFFER_COUNT:
				print('Replay exceeds the max replay size allowed by default in the game')
			if buffer_count == Replay.BUFFER_MAX_COUNT:
				print('Replay exceeds the max replay size allowed in Dannye\'s longer replays mod')
			file.seek(buffer_excess, 1)

	def write(self, file):
		buffer_offset = (file.tell() - 8) & Replay.BUFFER_SIZE
		buffer_size = Replay.BUFFER_SIZE - buffer_offset
		buffer_count = (buffer_offset // Replay.BUFFER_SIZE)

		if self.get_size() > buffer_size:
			file.seek(buffer_size, 1)

		for data in self._frame_data.values():
			if not data:
				continue

			if type(data) in (list, tuple):
				for value in data:
					file.write(value)
			else:
				file.write(data)

		file.write(self.blocks.FrameEnd())

	def read(self, file):
		buffer_offset = (file.tell() - 8) % Replay.BUFFER_SIZE
		buffer_size = Replay.BUFFER_SIZE - buffer_offset

		buffer = bytearray(file.read(buffer_size))
		offset = 0

		while offset <= len(buffer) - 16:
			block = self.blocks.ReplayBlock.from_buffer(buffer, offset)
			offset += block.get_size()

			if isinstance(block, self.blocks.FrameEnd):
				break
			elif isinstance(block, self.blocks.End):
				buffer = bytearray(file.read(Replay.BUFFER_SIZE))
				offset = 0
			else:
				self.set(block.TYPE, block)

	def get_size(self):
		size = 0
		for data in self._frame_data.values():
			if not data:
				continue

			if type(data) in (list, tuple):
				size += data[0].get_size() * len(data)
			else:
				size += data.get_size()

		return size + self.blocks.FrameEnd().get_size()


from files.replay.replay import Replay


