class Frame:
	def __init__(self, version):
		self._version = version
		self._frame_data = {}

	def get_frame_data(self):
		return self._frame_data

	def get_block(self, block_type, default=None):
		return self._frame_data.get(block_type, default)

	def set_block(self, block):
		if block.TYPE in block.get_required_types():
			self._frame_data[block.TYPE] = block
		else:
			if block.TYPE not in self._frame_data:
				self._frame_data[block.TYPE] = []

			self._frame_data[block.TYPE].append(block)

	def get_size(self):
		size = 0
		for data in self._frame_data.values():
			if not data:
				continue

			if type(data) in (list, tuple):
				size += data[0].get_size() * len(data)
			else:
				size += data.get_size()

		return size
