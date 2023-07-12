import ctypes
from .vehicle import Vehicle


class _Carriage(ctypes.LittleEndianStructure):
	_fields_ = (
		('previous', ctypes.c_uint32),
		('next', ctypes.c_uint32),
	)


class Train(Vehicle):
	TYPE = 18
	_fields_ = (
		('train_speed', ctypes.c_float),
		('track_distance', ctypes.c_float),
		('length', ctypes.c_float),
		('carriage', _Carriage),
		('track_id', ctypes.c_uint8)
	)
