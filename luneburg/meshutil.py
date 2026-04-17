"""网格工具：合并、包围盒等（供晶格阵列等方法复用）。"""

from __future__ import annotations

from typing import List

import numpy as np
import pymesh


def axis_aligned_bbox(mesh: pymesh.Mesh):
    """返回 (min_xyz, max_xyz)。"""
    v = mesh.vertices
    return v.min(axis=0), v.max(axis=0)


def bbox_extents(mesh: pymesh.Mesh):
    mn, mx = axis_aligned_bbox(mesh)
    return mx - mn


def translate_mesh(mesh: pymesh.Mesh, offset):
    off = np.asarray(offset, dtype=float).reshape(1, 3)
    v = mesh.vertices + off
    return pymesh.form_mesh(v, mesh.faces)


def merge_meshes(meshes: List[pymesh.Mesh]) -> pymesh.Mesh:
    """按顶点拼接多个网格（不焊接接缝；适合阵列占位与导出）。"""
    if not meshes:
        raise ValueError("merge_meshes: 空列表")
    if len(meshes) == 1:
        return meshes[0]
    verts = []
    faces = []
    offset = 0
    for m in meshes:
        verts.append(m.vertices)
        faces.append(m.faces + offset)
        offset += len(m.vertices)
    v = np.vstack(verts)
    f = np.vstack(faces)
    return pymesh.form_mesh(v, f)
