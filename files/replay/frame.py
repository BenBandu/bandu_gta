class Frame:
	def __init__(self, version):
		self._version = version
		self._frame_data = {}

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

	@property
	def size(self):
		size = 0
		for data in self._frame_data.values():
			if not data:
				continue

			if type(data) in (list, tuple):
				size += data[0].get_size() * len(data)
			else:
				size += data.get_size()

		return size
