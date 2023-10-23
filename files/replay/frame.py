from .blocks import ReplayBlockBase


class Frame:
	def __init__(self, version):
		self._version = version
		self._block = ReplayBlockBase.get_version(version)
		self._blocks = []
		self._block_map = {}

	def get_block(self, block_type, default=None):
		result = self._block_map.get(block_type, default)
		if result is default:
			return default

		if type(result) in (list, tuple):
			return [block for idx, block in enumerate(self._blocks) if idx in result]

		return self._blocks[result]

	def set_block(self, block):
		self._blocks.append(block)
		idx = len(self._blocks) - 1

		# Map block we just added to its type for easy retrieval
		if block.TYPE in block.get_singular_types():
			self._block_map[block.TYPE] = idx
		else:
			if block.TYPE not in self._block_map:
				self._block_map[block.TYPE] = []

			self._block_map[block.TYPE].append(idx)

	def get_size(self):
		return len(b''.join(self._blocks)) + 4

	def rebuild_map(self):
		blocks = self._blocks

		self._blocks = []
		self._block_map = {}

		for block in blocks:
			self.set_block(block)

	def write_frame_to_buffer(self, buffer):
		buffer += b''.join(self._blocks)
		buffer += self._block.create_from_type(self._block.TYPE_FRAME_END)
