"""元胞：原版球体 + 可变方孔（项目原始算法）。"""

from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np

import modules.stl_generator_pymesh as stl_gen

from luneburg.config import RunConfig


class LegacySphereHolesUnitCell:
    """球面 icosphere + XY 网格方孔 boolean 差集。"""

    name = "legacy_sphere_holes"

    def build(self, cfg: RunConfig) -> Tuple[Any, Dict[str, Any]]:
        d = cfg.diameter
        step = cfg.step_effective
        xs = np.arange(-d, d, step)
        ys = np.arange(-d, d, step)
        hole_count = int(len(xs) * len(ys))

        print("Sphere generated. Adding holes...")
        sphere = stl_gen.generate_sphere(radius=cfg.radius, resolution=cfg.resolution)
        for y in ys:
            for x in xs:
                hole_variability = (
                    (abs(x * x) + abs(y * y)) + cfg.square_hole_size * 3
                ) / 3.0
                A = cfg.square_hole_size * hole_variability
                sphere = stl_gen.add_square_hole_to_mesh(
                    L=d, A=A, xy_position=[x, y], mesh=sphere
                )
        stats = {"hole_count": hole_count}
        return sphere, stats
