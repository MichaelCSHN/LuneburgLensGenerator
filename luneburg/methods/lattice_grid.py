"""晶格：XY 平移复制并顶点合并（占位级阵列，便于后续换布尔焊接/周期边界等）。"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from luneburg.config import RunConfig
from luneburg.meshutil import bbox_extents, merge_meshes, translate_mesh


class GridXYLattice:
    name = "grid_xy"

    def arrange(self, mesh: Any, cfg: RunConfig) -> Tuple[Any, Dict[str, Any]]:
        nx = int(cfg.grid_nx)
        ny = int(cfg.grid_ny)
        if nx < 1 or ny < 1:
            raise ValueError("grid_xy 要求 grid_nx、grid_ny >= 1")
        if nx == 1 and ny == 1:
            return mesh, {
                "lattice_replicas": 1,
                "grid_nx": nx,
                "grid_ny": ny,
                "note": "1x1 等价于 single",
            }

        print("Lattice (grid_xy): arranging %d x %d copies..." % (nx, ny))
        ext = bbox_extents(mesh)
        px = float(ext[0]) * float(cfg.grid_pitch_scale)
        py = float(ext[1]) * float(cfg.grid_pitch_scale)
        px = max(px, 1e-9)
        py = max(py, 1e-9)

        copies = []
        for j in range(ny):
            for i in range(nx):
                offset = [i * px, j * py, 0.0]
                copies.append(translate_mesh(mesh, offset))
        merged = merge_meshes(copies)
        return merged, {
            "lattice_replicas": nx * ny,
            "grid_nx": nx,
            "grid_ny": ny,
            "pitch_mm_xy": [px, py],
            "grid_pitch_scale": float(cfg.grid_pitch_scale),
        }
