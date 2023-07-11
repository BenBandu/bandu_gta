import ctypes
from .block import ReplayBlock
from common.vector import FVec3
from common.matrix import FMatrix


class General(ReplayBlock):
	TYPE = 4
	_fields_ = (
		('in_rc_vehicle', ctypes.c_uint8),
		('camera', FMatrix),
		('attachment', ctypes.c_uint32),    # Pointer to attachment matrix I think? - part of CMatrix
		('has_rw_matrix', ctypes.c_uint8),  # Check if game owns this matrix? - part of CMatrix
		('player', FVec3)
	)
