from ..replay_block_base import ReplayBlockBase


class ReplayBlock(ReplayBlockBase):
	VERSION = 1

	TYPE_END = 0
	TYPE_VEHICLE = 1
	TYPE_PED_HEADER = 2
	TYPE_PED = 3
	TYPE_GENERAL = 4
	TYPE_CLOCK = 5
	TYPE_WEATHER = 6
	TYPE_FRAME_END = 7
	TYPE_TIMER = 8
	TYPE_BULLET_TRACE = 9

	@classmethod
	def get_vehicles_types(cls):
		return [cls.TYPE_VEHICLE]
