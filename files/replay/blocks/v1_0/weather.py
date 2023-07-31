import ctypes
from .block import ReplayBlock
from ..interfaces import IWeather


class Weather(ReplayBlock, IWeather):

	RANDOM      = -1
	SUNNY       = 0
	CLOUDY      = 1
	RAINY       = 2
	FOGGY       = 3

	TYPE = 6
	_fields_ = (
		('old', ctypes.c_uint8),
		('new', ctypes.c_uint8),
		('blend', ctypes.c_float)
	)

	@classmethod
	def get_weather_types(cls):
		return {
			cls.SUNNY: "Sunny",
			cls.CLOUDY: "Cloudy",
			cls.RAINY: "Rainy",
			cls.FOGGY: "Foggy",
		}
