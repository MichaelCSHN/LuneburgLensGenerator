import argparse
import json
import os
from datetime import datetime, timezone

import numpy as np

import modules.stl_generator_pymesh as stl_gen

# 与 pyproject.toml [project].version 保持一致
GENERATOR_VERSION = "0.2.0"
METADATA_SCHEMA = "luneburg-lens-generator-run-v1"


def _build_parser():
    p = argparse.ArgumentParser(
        description="Generate a Luneburg lens mesh (STL) using PyMesh."
    )
    p.add_argument(
        "--k",
        type=float,
        default=100.0,
        help="Scale factor (mm), applied to the final mesh (default: 100)",
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
        help="Base square hole size length in mm (default: 0.2)",
    )
    p.add_argument(
        "--resolution",
        type=int,
        default=4,
        help="Icosphere resolution (higher = finer mesh, larger STL) (default: 4)",
    )
    p.add_argument(
        "--step",
        type=float,
        default=None,
        metavar="MM",
        help="Grid step for hole placement in mm; omit to use diameter/16",
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
        help="Do not write sidecar JSON next to the STL (default: write)",
    )
    return p


def _metadata_path_for_stl(stl_path):
    base, _ = os.path.splitext(stl_path)
    return base + ".json"


def _write_run_metadata(
    *,
    stl_path,
    args_namespace,
    diameter,
    step_effective,
    hole_count,
):
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
        "generator_version": GENERATOR_VERSION,
        "generated_at_utc": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "pymesh_version": getattr(pymesh, "__version__", "unknown"),
        "numpy_version": np.__version__,
        "output_stl": stl_path,
        "output_stl_size_bytes": stl_size_bytes,
        "parameters": {
            "k": args_namespace.k,
            "radius": args_namespace.radius,
            "square_hole_size": args_namespace.square_hole_size,
            "resolution": args_namespace.resolution,
            "step": args_namespace.step,
            "step_effective_mm": step_effective,
            "diameter_mm": diameter,
            "hole_count": int(hole_count),
        },
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")

    print("Wrote metadata:", meta_path)


def main():
    args = _build_parser().parse_args()

    k = args.k
    radius = args.radius
    square_hole_size = args.square_hole_size
    diameter = radius * 2.0
    resolution = args.resolution
    step = args.step if args.step is not None else diameter / 16.0
    out_path = args.output

    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    xs = np.arange(-diameter, diameter, step)
    ys = np.arange(-diameter, diameter, step)
    hole_count = len(xs) * len(ys)

    print("Started process...")
    sphere = stl_gen.generate_sphere(radius=radius, resolution=resolution)

    print("Sphere generated. Adding holes...")

    for y in ys:
        for x in xs:
            hole_variability = (
                (abs(x * x) + abs(y * y)) + square_hole_size * 3
            ) / 3.0
            A = square_hole_size * hole_variability
            sphere = stl_gen.add_square_hole_to_mesh(
                L=diameter, A=A, xy_position=[x, y], mesh=sphere
            )

    print("Luneburg lens generated , scaling up...")
    scaled_sphere = stl_gen.scale_model(mesh=sphere, scale_factor=k)

    print("Exporting model to .stl")
    stl_gen.export_to_stl(mesh=scaled_sphere, filename=out_path)

    if not args.no_metadata:
        _write_run_metadata(
            stl_path=out_path,
            args_namespace=args,
            diameter=diameter,
            step_effective=step,
            hole_count=hole_count,
        )

    print("Done!")


if __name__ == "__main__":
    main()
