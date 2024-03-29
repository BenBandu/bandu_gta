from ..replay_block_base import ReplayBlockBase


class ReplayBlock(ReplayBlockBase):
	VERSION = 2

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
	TYPE_FREEPLAY = 20

	@classmethod
	def get_vehicles_types(cls):
		return [cls.TYPE_VEHICLE, cls.TYPE_BIKE]

	@classmethod
	def get_required_types(cls):
		return [cls.TYPE_GENERAL, cls.TYPE_CLOCK, cls.TYPE_WEATHER, cls.TYPE_TIMER, cls.TYPE_MISC]

	@classmethod
	def get_singular_types(cls):
		return [cls.TYPE_GENERAL, cls.TYPE_CLOCK, cls.TYPE_WEATHER, cls.TYPE_TIMER, cls.TYPE_MISC, cls.TYPE_FREEPLAY]

	@classmethod
	def get_multi_types(cls):
		return [cls.TYPE_VEHICLE, cls.TYPE_PED_HEADER, cls.TYPE_PED, cls.TYPE_BULLET_TRACE, cls.TYPE_PARTICLE]
