import ctypes
from .block import ReplayBlock
from ..interfaces import IWeather


class Weather(ReplayBlock, IWeather):

	UNDEFINED           = -1
	LS_EXTRASUNNY       = 0
	LS_SUNNY            = 1
	LS_EXTRASUNNY_SMOG  = 2
	LS_SUNNY_SMOG       = 3
	LS_CLOUDY           = 4
	SF_SUNNY            = 5
	SF_EXTRASUNNY       = 6
	SF_CLOUDY           = 7
	SF_RAINY            = 8
	SF_FOGGY            = 9
	LV_SUNNY            = 10
	LV_EXTRASUNNY       = 11
	LV_CLOUDY           = 12
	COUNTRY_EXTRASUNNY  = 13
	COUNTRY_SUNNY       = 14
	COUNTRY_CLOUDY      = 15
	COUNTRY_RAINY       = 16
	DESERT_EXTRASUNNY   = 17
	DESERT_SUNNY        = 18
	DESERT_SANDSTORM    = 19
	MISC_UNDERWATER     = 20
	MISC_EXTRACOLOURS_1 = 21
	MISC_EXTRACOLOURS_2 = 22

	TYPE = 7
	_fields_ = (
		('old', ctypes.c_uint8),
		('new', ctypes.c_uint8),
		('blend', ctypes.c_float)
	)

	@classmethod
	def get_weather_types(cls):
		return {
			cls.UNDEFINED: "Undefined",
			cls.LS_EXTRASUNNY: "Los Santos: Extra Sunny",
			cls.LS_SUNNY: "Los Santos: Sunny",
			cls.LS_EXTRASUNNY_SMOG: "Los Santos: Extra Sunny Smog",
			cls.LS_SUNNY_SMOG: "Los Santos: Sunny Smog",
			cls.LS_CLOUDY: "Los Santos: Cloudy",
			cls.SF_SUNNY: "San Fierro: Sunny",
			cls.SF_EXTRASUNNY: "San Fierro: Extra Sunny",
			cls.SF_RAINY: "San Fierro: Rainy",
			cls.SF_FOGGY: "San Fierro: Foggy",
			cls.LV_SUNNY: "Las Venturas: Sunny",
			cls.LV_EXTRASUNNY: "Las Venturas: Extra Sunny",
			cls.LV_CLOUDY: "Las Venturas: Cloudy",
			cls.COUNTRY_EXTRASUNNY: "Countryside: Extra Sunny",
			cls.COUNTRY_SUNNY: "Countryside: Sunny",
			cls.COUNTRY_CLOUDY: "Countryside: Cloudy",
			cls.COUNTRY_RAINY: "Countryside: Rainy",
			cls.DESERT_EXTRASUNNY: "Desert: Extra Sunny",
			cls.DESERT_SUNNY: "Desert: Sunny",
			cls.DESERT_SANDSTORM: "Desert: Sandstorm",
			cls.MISC_UNDERWATER: "Misc: Underwater",
			cls.MISC_EXTRACOLOURS_1: "Misc: Colours 1",
			cls.MISC_EXTRACOLOURS_2: "Misc: Colours 2",
		}
