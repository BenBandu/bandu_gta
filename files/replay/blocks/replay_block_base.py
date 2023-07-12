import ctypes


class ReplayBlockBase(ctypes.LittleEndianStructure):
	TYPE = None
	TYPE_END = None
	TYPE_VEHICLE = None
	TYPE_BIKE = None
	TYPE_PED_HEADER = None
	TYPE_PED = None
	TYPE_GENERAL = None
	TYPE_CLOCK = None
	TYPE_WEATHER = None
	TYPE_FRAME_END = None
	TYPE_TIMER = None
	TYPE_BULLET_TRACE = None
	TYPE_PARTICLE = None
	TYPE_MISC = None
	TYPE_VEHICLE_DELETED = None
	TYPE_PED_DELETED = None
	TYPE_BMX = None
	TYPE_HELICOPTER = None
	TYPE_PLANE = None
	TYPE_TRAIN = None
	TYPE_CLOTHES = None

	_fields_ = (
		('block_type', ctypes.c_uint8),
	)

	def __init__(self, *args, **kw):
		super().__init__(*args, **kw)
		self.block_type = self.TYPE

	@classmethod
	def create_from_buffer(cls, buffer, offset):
		block = cls.from_buffer(buffer, offset)
		return block.get_as_block_type()

	def get_as_block_type(self):
		for cls in self.__class__.__subclasses__():
			if cls.TYPE == self.block_type:
				return ctypes.cast(ctypes.pointer(self), ctypes.POINTER(cls)).contents

		raise TypeError(F'Unkown replay block type: {self.block_type}')

	def get_size(self):
		return ctypes.sizeof(self.__class__)
