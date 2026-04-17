"""元胞与晶格方法的注册表（「并」部分可扩展入口）。"""

from __future__ import annotations

from typing import Dict, List

from luneburg.methods import lattice_grid, lattice_single, unit_legacy

# 实例注册：名称 -> 实现
UNIT_CELL_REGISTRY: Dict[str, object] = {
    unit_legacy.LegacySphereHolesUnitCell.name: unit_legacy.LegacySphereHolesUnitCell(),
}

LATTICE_REGISTRY: Dict[str, object] = {
    lattice_single.SingleLattice.name: lattice_single.SingleLattice(),
    lattice_grid.GridXYLattice.name: lattice_grid.GridXYLattice(),
}


def list_unit_cell_methods() -> List[str]:
    return sorted(UNIT_CELL_REGISTRY.keys())


def list_lattice_methods() -> List[str]:
    return sorted(LATTICE_REGISTRY.keys())
