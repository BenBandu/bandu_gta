from . import v1_0
from . import v2_0
from . import v3_0
from . import v4_0
from .. import VERSION_GTA3, VERSION_GTAVC, VERSION_GTASA, VERSION_STEAM_GTASA

version_mapping = {
	VERSION_GTA3: v1_0,
	VERSION_GTAVC: v2_0,
	VERSION_GTASA: v3_0,
	VERSION_STEAM_GTASA: v4_0,
}
