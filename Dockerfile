FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu18.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    libopencv-dev git \
    python3 python3-dev python3-pip python3-setuptools \
    g++ wget make \
    libprotobuf-dev protobuf-compiler \
    libopencv-dev \
    libgoogle-glog-dev libboost-all-dev \
    libcaffe-cuda-dev libhdf5-dev libatlas-base-dev \
    libgtk2.0-dev \
    vim iputils-ping htop unzip

RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.0/cmake-3.16.0-Linux-x86_64.tar.gz && \
    tar xzf cmake-3.16.0-Linux-x86_64.tar.gz -C /opt && rm cmake-3.16.0-Linux-x86_64.tar.gz
ENV PATH="/opt/cmake-3.16.0-Linux-x86_64/bin:${PATH}"

RUN apt-get -y clean

WORKDIR /app
ADD . /app/
RUN rm -rf openpose
RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git
WORKDIR /app/openpose
RUN git submodule update --init --recursive --remote
#RUN git checkout a42b63902192e6aa17ff9f3cc6652c69636a29c3

#build it
WORKDIR /app/openpose/build
#RUN cmake-gui ..
RUN cmake -DBUILD_PYTHON=ON  \ 
#  -DGPU_MODE=CPU_ONLY .. \
    -DUSE_CUDNN=OFF \ 
    -DDOWNLOAD_BODY_25_MODEL=OFF \
    -DDOWNLOAD_BODY_COCO_MODEL=OFF \
    -DDOWNLOAD_BODY_MPI_MODEL=OFF \ 
    -DDOWNLOAD_FACE_MODEL=OFF \ 
    -DDOWNLOAD_HAND_MODEL=OFF \
    .. \
    && make -j `nproc`

WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN bash setup.sh
RUN mkdir -p outputs
RUN chmod +x runcode.sh

#WORKDIR /app/openpose/models/
#RUN bash getModels.sh
