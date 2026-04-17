"""运行配置与命令行解析。"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass, fields, replace
from typing import Any, Dict, Optional


@dataclass
class RunConfig:
    """单次生成的完整参数（串行预处理输入 + 并行方法选择 + 后处理）。"""

    k: float = 100.0
    radius: float = 1.0
    square_hole_size: float = 0.2
    resolution: int = 4
    step: Optional[float] = None
    output: str = "output/luneburg.stl"
    no_metadata: bool = False
    unit_cell_method: str = "legacy_sphere_holes"
    lattice_method: str = "single"
    grid_nx: int = 1
    grid_ny: int = 1
    grid_pitch_scale: float = 1.0

    @property
    def diameter(self) -> float:
        return self.radius * 2.0

    @property
    def step_effective(self) -> float:
        if self.step is not None:
            return float(self.step)
        return self.diameter / 16.0

    def to_serializable_dict(self) -> Dict[str, Any]:
        """用于元数据与对比实验记录。"""
        d = asdict(self)
        return d


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate a Luneburg lens mesh (STL) using PyMesh（串-并-串管线）."
    )
    p.add_argument(
        "--k",
        type=float,
        default=100.0,
        help="Scale factor (mm), applied in postprocess (default: 100)",
    )
    p.add_argument(
        "--radius",
        type=float,
        default=1.0,
        help="Unscaled sphere radius in mm (default: 1.0)",
    )
    p.add_argument(
        "--square-hole-size",
        type=float,
        default=0.2,
        metavar="SIZE",
        help="Base square hole size length in mm (legacy 元胞) (default: 0.2)",
    )
    p.add_argument(
        "--resolution",
        type=int,
        default=4,
        help="Icosphere resolution (default: 4)",
    )
    p.add_argument(
        "--step",
        type=float,
        default=None,
        metavar="MM",
        help="Hole grid step in mm; omit to use diameter/16",
    )
    p.add_argument(
        "-o",
        "--output",
        type=str,
        default="output/luneburg.stl",
        help="Output STL path (default: output/luneburg.stl)",
    )
    p.add_argument(
        "--no-metadata",
        action="store_true",
        help="Do not write sidecar JSON next to the STL",
    )
    p.add_argument(
        "--unit-cell",
        dest="unit_cell_method",
        default="legacy_sphere_holes",
        metavar="NAME",
        help="元胞生成方法（默认: legacy_sphere_holes）",
    )
    p.add_argument(
        "--lattice",
        dest="lattice_method",
        default="single",
        metavar="NAME",
        help="晶格/阵列方法: single | grid_xy（默认: single）",
    )
    p.add_argument(
        "--grid-nx",
        type=int,
        default=1,
        help="grid_xy: X 方向元胞个数（默认: 1）",
    )
    p.add_argument(
        "--grid-ny",
        type=int,
        default=1,
        help="grid_xy: Y 方向元胞个数（默认: 1）",
    )
    p.add_argument(
        "--grid-pitch-scale",
        type=float,
        default=1.0,
        help="grid_xy: 间距 = 元胞包围盒尺寸 * 该系数（默认: 1.0）",
    )
    p.add_argument(
        "--from-config",
        type=str,
        default=None,
        metavar="PATH",
        help="JSON 配置文件，覆盖上述 CLI 默认值（便于批处理/对比）",
    )
    p.add_argument(
        "--list-methods",
        action="store_true",
        help="列出已注册的元胞与晶格方法后退出",
    )
    return p


def _merge_json_overlay(cfg: RunConfig, path: str) -> RunConfig:
    if not path:
        return cfg
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        raise ValueError("--from-config 必须是 JSON 对象")
    allowed = {f.name for f in fields(RunConfig)}
    kwargs = {}
    for key, val in raw.items():
        if key not in allowed:
            raise ValueError("未知配置键: %s（允许: %s）" % (key, ", ".join(sorted(allowed))))
        kwargs[key] = val
    return replace(cfg, **kwargs)


def config_from_args(ns: argparse.Namespace) -> RunConfig:
    cfg = RunConfig(
        k=ns.k,
        radius=ns.radius,
        square_hole_size=ns.square_hole_size,
        resolution=ns.resolution,
        step=ns.step,
        output=ns.output,
        no_metadata=ns.no_metadata,
        unit_cell_method=ns.unit_cell_method,
        lattice_method=ns.lattice_method,
        grid_nx=ns.grid_nx,
        grid_ny=ns.grid_ny,
        grid_pitch_scale=ns.grid_pitch_scale,
    )
    if getattr(ns, "from_config", None):
        p = ns.from_config
        if not os.path.isfile(p):
            raise FileNotFoundError("--from-config 文件不存在: %s" % p)
        cfg = _merge_json_overlay(cfg, p)
    return cfg
