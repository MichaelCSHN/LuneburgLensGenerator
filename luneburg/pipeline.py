"""串-并-串总编排。"""

from __future__ import annotations

from typing import Any, Dict

from luneburg.config import RunConfig
from luneburg.postprocess import run_postprocess
from luneburg.preprocess import preprocess
from luneburg.registry import LATTICE_REGISTRY, UNIT_CELL_REGISTRY


def run(cfg: RunConfig) -> None:
    cfg = preprocess(cfg)
    d = cfg.diameter
    step_eff = cfg.step_effective

    print("Started process...")

    uc = UNIT_CELL_REGISTRY[cfg.unit_cell_method]
    lat = LATTICE_REGISTRY[cfg.lattice_method]

    print("Parallel branch: unit_cell=%s" % cfg.unit_cell_method)
    mesh_uc, s_uc = uc.build(cfg)

    print("Parallel branch: lattice=%s" % cfg.lattice_method)
    mesh_lat, s_lat = lat.arrange(mesh_uc, cfg)

    print("Luneburg lens generated , scaling up...")

    parallel_stats: Dict[str, Any] = {
        "unit_cell": {"method": cfg.unit_cell_method, **s_uc},
        "lattice": {"method": cfg.lattice_method, **s_lat},
    }

    run_postprocess(
        mesh_lat,
        cfg,
        diameter=d,
        step_effective=step_eff,
        parallel_stats=parallel_stats,
    )
    print("Done!")
