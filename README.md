# Luneburg Lens Genarator


Python script for generating a Luneburg Lens programatically without the use of 3D modeling software based on the [Pymesh](https://github.com/PyMesh/PyMesh) platform

This program was developed for the subject "Medidas electronicas 2" for the UTN FRBA university in the year 2023.

For more information check our [white paper](https://github.com/jboirazian/LuneburgLensGenerator/blob/main/white-paper.pdf)

> [!NOTE]  
> This project is a precursor to [LuneForge](https://github.com/jboirazian/LuneForge)


## How to run it:

You will need [Docker](https://www.docker.com/) for this project.

Clone the project, then build the image (default base image is reachable from many CN networks; override if you pull from Docker Hub directly):

    docker build -t luneburg-gen .

    # Optional (e.g. outside China): use upstream PyMesh image
    # docker build -t luneburg-gen --build-arg BASE_IMAGE=pymesh/pymesh:py3.7-slim .

Run the generator (mount the repo so `output/` is written on your host). Default STL path is `output/luneburg.stl`:

    docker run --rm -v "$(pwd)":/app -w /app luneburg-gen

CLI parameters (examples):

    docker run --rm -v "$(pwd)":/app -w /app luneburg-gen python3 -u Luneburg.py --help

    docker run --rm -v "$(pwd)":/app -w /app luneburg-gen python3 -u Luneburg.py \
      --k 100 --radius 1.0 --square-hole-size 0.2 --resolution 4 -o output/luneburg.stl

Quick smoke (few holes, fast; writes `output/smoke.stl`):

    docker run --rm -v "$(pwd)":/app -w /app luneburg-gen python3 -u Luneburg.py \
      --resolution 2 --step 5.0 --k 10 -o output/smoke.stl

Or run `./scripts/smoke_docker.sh` (expects image `luneburg-gen` already built).

### Run metadata (JSON)

Each successful run writes a **sidecar JSON** next to the STL (same basename):
`output/luneburg.stl` → `output/luneburg.json`. Schema **v2** records full
`parameters`, effective step / diameter, `hole_count` (when applicable),
`pipeline.parallel` (unit_cell + lattice stats), mesh metrics after scaling,
PyMesh/NumPy versions, UTC time, and STL size. Disable with `--no-metadata`.

### Performance notes

Runtime is dominated by **PyMesh boolean differences** repeated for each grid hole.
Rough hole count is about `(2 * diameter / step)^2` (see `hole_count` in the JSON).
Increasing `--resolution` grows the base icosphere and STL size quickly. Start with
defaults; use a larger `--step` or smoke settings when iterating.

### Dependencies

- **Runtime:** Docker image `pymesh/pymesh:py3.7-slim` (or CN mirror via `BASE_IMAGE`).
- **Pinned Python deps** (for reference / optional local tooling): `requirements.txt`
  and `pyproject.toml` (NumPy only; PyMesh comes from the image).

### CI

GitHub Actions workflow `.github/workflows/ci.yml` builds with Docker Hub’s PyMesh
image and runs the same smoke command, checking STL + JSON.

### Pipeline architecture (Phase 3: 串-并-串)

- **串 1（预处理）** `luneburg/preprocess.py`：参数校验、方法名存在性检查。
- **并（可插拔方法）**  
  - **元胞** `luneburg/methods/unit_*.py`，注册表 `UNIT_CELL_REGISTRY`（当前：`legacy_sphere_holes`）。  
  - **晶格/阵列** `luneburg/methods/lattice_*.py`，注册表 `LATTICE_REGISTRY`（`single` 直通；`grid_xy` XY 平移复制 + 顶点合并占位，便于后续换焊接/周期等实现）。
- **串 2（后处理）** `luneburg/postprocess.py`：整体缩放、导出 STL、侧车 JSON、简单网格指标（顶点/面数）。  
- **编排** `luneburg/pipeline.py`；**对比占位** `luneburg/compare.py`（批处理汇总壳）。

列出已注册方法：

    docker run --rm -v "$(pwd)":/app -w /app luneburg-gen python3 -u Luneburg.py --list-methods

用 JSON 覆盖默认参数（便于批处理与多方法对比；文件中出现的键覆盖 CLI）：

    docker run --rm -v "$(pwd)":/app -w /app luneburg-gen python3 -u Luneburg.py \
      --from-config examples/run_smoke.json

阵列示例（2×2，间距按元胞包围盒 × 系数）：

    docker run --rm -v "$(pwd)":/app -w /app luneburg-gen python3 -u Luneburg.py \
      --lattice grid_xy --grid-nx 2 --grid-ny 2 --grid-pitch-scale 1.05 \
      --resolution 2 --step 5.0 --k 10 -o output/grid_smoke.stl

批处理占位脚本（需已挂载仓库且已构建镜像）：

    chmod +x scripts/batch_compare_stub.sh
    ./scripts/batch_compare_stub.sh

侧车 JSON 的 `schema` 为 `luneburg-lens-generator-run-v2`，含 `pipeline.parallel`
（元胞/晶格统计）与 `comparison_stub` 占位字段。

# Example of use:

We designed and builded a Luneburg Lens that operated in Band X (8-12 Ghz). We also wanted to use a commercial FDM 3D printer and PLA filament.

Our design parameters were the following:

    k=100 ## Scale factor
    radius = 1.0 ## Unscaled sphere radious
    square_hole_size = 0.2 ## Square hole size lenght
    resolution = 4 ## sphere resolution (4 is fine , for highier resolution increase it , keeping in mind that it will increase the .stl model size)
    step = diameter/16 ## square holes resolution
    hole_variability=(((abs(x*x)+abs(y*y)))+square_hole_size*3)/3

If you want to print this lens , keep in mind to use 100% infill when printing the lens.

You can find this lens on the [Releases section](https://github.com/jboirazian/LuneburgLensGenerator/releases/tag/v1)

## Our results:

Before printing we runned some simulations in CST Studio and confirmed that there was a substantial increase in gain and directivity with our Lens

![cst1](https://github.com/jboirazian/LuneburgLensGenerator/blob/main/imgs/cst1.jpeg)

![cst2](https://github.com/jboirazian/LuneburgLensGenerator/blob/main/imgs/cst2.jpeg)


We were able to run multiple tests in our setup with VNA and 2 horn antennas (one as a transmitter and one as a reciver) and we successfully confimed our Simulations in CST Studio. We dramatically saw a gain in the S12 and S21 parameters of 6 db and more directivity in the beam

![lens1](https://github.com/jboirazian/LuneburgLensGenerator/blob/main/imgs/lens-1.jpeg)
![lens2](https://github.com/jboirazian/LuneburgLensGenerator/blob/main/imgs/lens-2.jpeg)
![lens3](https://github.com/jboirazian/LuneburgLensGenerator/blob/main/imgs/lens-3.jpeg)
![lens4](https://github.com/jboirazian/LuneburgLensGenerator/blob/main/imgs/lens-4.jpeg)





# Contact information:

+ [Juan Agustín Boirazian](https://www.linkedin.com/in/juan-boirazian/)

+ [Juan Ignacio Falabella](https://www.linkedin.com/in/juan-ignacio-falabella-8ba659161/)
