"""晶格：单个元胞直通（无阵列变换）。"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from luneburg.config import RunConfig


class SingleLattice:
    name = "single"

    def arrange(self, mesh: Any, cfg: RunConfig) -> Tuple[Any, Dict[str, Any]]:
        return mesh, {"lattice_replicas": 1}
