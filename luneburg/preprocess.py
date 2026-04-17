"""串行预处理：参数校验、方法存在性检查。"""

from __future__ import annotations

from luneburg.config import RunConfig
from luneburg.registry import LATTICE_REGISTRY, UNIT_CELL_REGISTRY


def preprocess(cfg: RunConfig) -> RunConfig:
    if cfg.radius <= 0:
        raise ValueError("radius 必须 > 0")
    if cfg.resolution < 1:
        raise ValueError("resolution 必须 >= 1")
    if cfg.k == 0:
        raise ValueError("k 不能为 0")
    if cfg.square_hole_size <= 0:
        raise ValueError("square_hole_size 必须 > 0")
    if cfg.step_effective <= 0:
        raise ValueError("有效 step 必须 > 0")
    if cfg.unit_cell_method not in UNIT_CELL_REGISTRY:
        raise ValueError(
            "未知元胞方法 %r；可用: %s"
            % (cfg.unit_cell_method, ", ".join(UNIT_CELL_REGISTRY))
        )
    if cfg.lattice_method not in LATTICE_REGISTRY:
        raise ValueError(
            "未知晶格方法 %r；可用: %s"
            % (cfg.lattice_method, ", ".join(LATTICE_REGISTRY))
        )
    if cfg.grid_pitch_scale <= 0:
        raise ValueError("grid_pitch_scale 必须 > 0")
    return cfg
