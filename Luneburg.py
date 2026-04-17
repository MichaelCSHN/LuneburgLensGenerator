"""入口脚本：解析 CLI / 配置，执行串-并-串管线。"""

from luneburg.config import build_parser, config_from_args
from luneburg.pipeline import run
from luneburg.registry import list_lattice_methods, list_unit_cell_methods


def main():
    parser = build_parser()
    ns = parser.parse_args()

    if ns.list_methods:
        print("Registered unit_cell methods:")
        for n in list_unit_cell_methods():
            print(" ", n)
        print("Registered lattice methods:")
        for n in list_lattice_methods():
            print(" ", n)
        return

    cfg = config_from_args(ns)
    run(cfg)


if __name__ == "__main__":
    main()
