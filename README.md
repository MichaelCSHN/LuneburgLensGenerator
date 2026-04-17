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
`output/luneburg.stl` → `output/luneburg.json`. It records CLI parameters, effective
step, estimated hole count, PyMesh/NumPy versions, UTC time, and STL size — for
reproducibility and later method comparison. Disable with `--no-metadata`.

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
