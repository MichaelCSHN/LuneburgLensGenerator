# 国内可直接拉取的基础镜像；海外可覆盖：docker build --build-arg BASE_IMAGE=pymesh/pymesh:py3.7-slim .
ARG BASE_IMAGE=docker.1panel.live/pymesh/pymesh:py3.7-slim
FROM ${BASE_IMAGE}
WORKDIR /app
COPY Luneburg.py ./
COPY modules/ ./modules/
CMD ["python3", "-u", "Luneburg.py"]