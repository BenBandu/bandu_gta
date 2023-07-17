import ctypes
from ..replay_block_base import ReplayBlockBase


class ReplayBlock(ReplayBlockBase):
	VERSION = 3

	TYPE_END = 0
	TYPE_VEHICLE = 1
	TYPE_BIKE = 2
	TYPE_PED_HEADER = 3
	TYPE_PED = 4
	TYPE_GENERAL = 5
	TYPE_CLOCK = 6
	TYPE_WEATHER = 7
	TYPE_FRAME_END = 8
	TYPE_TIMER = 9
	TYPE_BULLET_TRACE = 10
	TYPE_PARTICLE = 11
	TYPE_MISC = 12
	TYPE_VEHICLE_DELETED = 13
	TYPE_PED_DELETED = 14
	TYPE_BMX = 15
	TYPE_HELICOPTER = 16
	TYPE_PLANE = 17
	TYPE_TRAIN = 18
	TYPE_CLOTHES = 19

	@classmethod
	def get_vehicles_types(cls):
		return [cls.TYPE_VEHICLE, cls.TYPE_BIKE, cls.TYPE_BMX, cls.TYPE_HELICOPTER, cls.TYPE_PLANE, cls.TYPE_TRAIN]

	@classmethod
	def get_required_types(cls):
		return [cls.TYPE_GENERAL, cls.TYPE_CLOCK, cls.TYPE_WEATHER, cls.TYPE_TIMER, cls.TYPE_MISC]

	def get_as_block_type(self):
		for cls in self.__class__.__subclasses__():
			if cls.TYPE == self.block_type:
				return self.cast_to_class(cls)
			elif cls.TYPE == self.TYPE_VEHICLE:
				for vehicle_cls in cls.__subclasses__():
					if vehicle_cls.TYPE == self.block_type:
						return self.cast_to_class(vehicle_cls)

		raise TypeError(F'Unkown replay block type: {self.block_type}')
