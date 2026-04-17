"""多方法对比与批处理汇总占位（后续接表格/图表/外部仿真指标）。"""

from __future__ import annotations

from typing import Any, Dict, List


def build_comparison_placeholder(
    *,
    run_summaries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    run_summaries: 多条运行侧车 JSON 的 dict（或精简字段），返回统一对比壳。
    当前仅占位，便于 Phase 3+ 接入真实指标与可视化。
    """
    return {
        "schema": "luneburg-comparison-stub-v0",
        "runs": len(run_summaries),
        "items": run_summaries,
        "note": "实现批处理后将写入 vertex_count、方法名、耗时等对比列",
    }
