from typing import Any, cast

from .distributed import global_leader_only
from .logging import setup_logging
from .utils import save_mels, tree_map

try:  # Optional in inference-only installs
	from .engine import Engine as _Engine, gather_attribute as _gather_attribute
	from .train_loop import TrainLoop as _TrainLoop, is_global_leader as _is_global_leader
except Exception:  # pragma: no cover
	_Engine = None
	_TrainLoop = None

	def _gather_attribute(*args: Any, **kwargs: Any) -> Any:
		raise RuntimeError(
			"gather_attribute is unavailable (DeepSpeed dependency failed to import)."
		)

	def _is_global_leader() -> bool:
		return True

Engine = cast(Any, _Engine)
TrainLoop = cast(Any, _TrainLoop)
gather_attribute = cast(Any, _gather_attribute)
is_global_leader = cast(Any, _is_global_leader)
