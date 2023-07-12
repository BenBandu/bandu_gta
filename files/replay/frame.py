from . import blocks
from . import VERSION_GTA3, VERSION_GTAVC, VERSION_GTASA
from . import REPLAY_BUFFER_SIZE, REPLAY_NUM_BUFFERS, REPLAY_MAX_BUFFERS


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

		if self._version > VERSION_GTA3:
			frame_data.update({
				block.TYPE_BIKE: [],
				block.TYPE_PARTICLE: [],
				block.TYPE_MISC: self.blocks.Misc(),
			})

		if self._version > VERSION_GTAVC:
			frame_data.update({
				block.TYPE_VEHICLE_DELETED: [],
				block.TYPE_PED_DELETED: [],
				block.TYPE_BMX: [],
				block.TYPE_HELICOPTER: [],
				block.TYPE_PLANE: [],
				block.TYPE_TRAIN: [],
				block.TYPE_CLOTHES: [],
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

	def write(self, file):
		buffer_offset = (file.tell() - 8) & REPLAY_BUFFER_SIZE
		buffer_size = REPLAY_BUFFER_SIZE - buffer_offset
		buffer_count = (buffer_offset // REPLAY_BUFFER_SIZE)

		if self.get_size() > buffer_size:
			file.seek(buffer_size, 1)
			buffer_count += 1

		if buffer_count == REPLAY_NUM_BUFFERS:
			print('Replay exceeds the max replay size allowed by default in the game')
		elif buffer_count == REPLAY_MAX_BUFFERS:
			print('Replay exceeds the max replay size allowed in Dannye\'s longer replays mod')

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
		start_pos = file.tell()
		buffer_offset = (start_pos - 8) % REPLAY_BUFFER_SIZE
		buffer_size = REPLAY_BUFFER_SIZE - buffer_offset
		buffer = bytearray(file.read(buffer_size))

		offset = 0
		while offset <= len(buffer) - 16:
			block = self.blocks.ReplayBlock.create_from_buffer(buffer, offset)
			offset += block.get_size()

			if isinstance(block, self.blocks.FrameEnd):
				file.seek(start_pos + offset)
				break
			elif isinstance(block, self.blocks.End):
				start_pos = file.tell()
				buffer = bytearray(file.read(REPLAY_BUFFER_SIZE))
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
