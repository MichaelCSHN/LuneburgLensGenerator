"""串行后处理：缩放、导出 STL、元数据与简单指标。"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import numpy as np

import modules.stl_generator_pymesh as stl_gen

from luneburg import __version__

METADATA_SCHEMA = "luneburg-lens-generator-run-v2"


def _parameters_block(cfg, *, diameter: float, step_effective: float, parallel_stats: Dict[str, Any]):
    params = cfg.to_serializable_dict()
    params["step_effective_mm"] = step_effective
    params["diameter_mm"] = diameter
    hc = parallel_stats.get("unit_cell", {}).get("hole_count")
    if hc is not None:
        params["hole_count"] = int(hc)
    return params


def _metadata_path_for_stl(stl_path: str) -> str:
    base, _ = os.path.splitext(stl_path)
    return base + ".json"


def _mesh_metrics(mesh: Any) -> Dict[str, int]:
    return {
        "vertex_count": int(len(mesh.vertices)),
        "face_count": int(len(mesh.faces)),
    }


def write_run_metadata(
    *,
    stl_path: str,
    cfg,
    diameter: float,
    step_effective: float,
    parallel_stats: Dict[str, Any],
    metrics: Dict[str, int],
) -> None:
    import pymesh

    meta_path = _metadata_path_for_stl(stl_path)
    meta_dir = os.path.dirname(os.path.abspath(meta_path))
    if meta_dir:
        os.makedirs(meta_dir, exist_ok=True)

    stl_size_bytes = None
    if os.path.isfile(stl_path):
        stl_size_bytes = os.path.getsize(stl_path)

    payload = {
        "schema": METADATA_SCHEMA,
        "generator_version": __version__,
        "generated_at_utc": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "pymesh_version": getattr(pymesh, "__version__", "unknown"),
        "numpy_version": np.__version__,
        "output_stl": stl_path,
        "output_stl_size_bytes": stl_size_bytes,
        "pipeline": {
            "serial_preprocess": {"validated": True},
            "parallel": parallel_stats,
            "serial_postprocess": {
                "scale_k": cfg.k,
                "metrics_after_scale": metrics,
            },
        },
        "parameters": _parameters_block(
            cfg, diameter=diameter, step_effective=step_effective, parallel_stats=parallel_stats
        ),
        "comparison_stub": {
            "note": "Phase 3 占位：后续可写入多方法批处理汇总路径与图表索引",
            "report_version": "0",
        },
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")

    print("Wrote metadata:", meta_path)


def run_postprocess(
    mesh: Any,
    cfg,
    *,
    diameter: float,
    step_effective: float,
    parallel_stats: Dict[str, Any],
) -> None:
    out_path = cfg.output
    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print("Scaling up...")
    scaled = stl_gen.scale_model(mesh=mesh, scale_factor=cfg.k)

    metrics = _mesh_metrics(scaled)

    print("Exporting model to .stl")
    stl_gen.export_to_stl(mesh=scaled, filename=out_path)

    if not cfg.no_metadata:
        write_run_metadata(
            stl_path=out_path,
            cfg=cfg,
            diameter=diameter,
            step_effective=step_effective,
            parallel_stats=parallel_stats,
            metrics=metrics,
        )
