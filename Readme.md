# POSE-ESTIMATION with OpenPose

**pose-estimation** is responsible for estimating the pose given a region with an operator. It uses the open-source pose
estimator [Openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) as its core engine.

This module has three core operations:

- Estimate
- Remove outsider operators
- Get pose position

### Estimate

Uses only one frame as input and returns the coordinates of every person in it, following a matrix of coordinates and
probabilities, using the following schema:

It returns two things:

#### Pose keypoints coordenates

A 21 * 3 matrix with each pose coordinate and accuracy for each person detected 
```
[[x, y, acc],
[x, y, acc], 
... ...
[x, y, acc],
[x, y, acc]]
```

![openpose_ids ](.github/media/openpose-ids.png)

## PREREQUISITES

* **Ubuntu** >= 18.04
* **Nvidia Driver** >= 410.68
* **Docker & Nvidia-docker** >=  20.10
* **docker-compose** >= 1.29.2
* **RabbitMQ** >= 3.11.17
* **Kombu** >= 5.1.0

## INSTALLATION

**Install nvidia-docker**

```
sudo su
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu22.04/nvidia-docker.list > /etc/apt/sources.list.d/nvidia-docker.list
apt update
apt -y install nvidia-container-toolkit nvidia-docker2
```

### Installation for manual testing

* First, install Docker.

* Clone repository:
  ```
   git clone https://github.com/fmorenovr/openpose.git
  ```

**Docker installation**

We use docker in order to test locally, goes to the repository dir `openpose`. Then, first we need to run:

```
sudo docker-compose -f docker-compose.yaml up --build -d
```

Test the environment:

```
sudo docker exec -it openpose bash
```

**Local Installation (Ubuntu 18.04)**

* First, Install main libs:

```
# cmake, usually already installed on Linux
# cmake, usually already installed on Linux, in other case:
sudo apt-get install cmake cmake-qt-gui
sudo apt-get install build-essential libssl-dev
# other libraries
sudo apt-get install libgoogle-glog-dev
sudo apt-get install protobuf-compiler libprotobuf-dev
sudo apt-get install libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libboost-filesystem1.74-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libcaffe-cuda-dev
sudo apt-get install libgtk2.0-dev
```

* Second, install OpenPose following the installation instructions from [here](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md).


Step 1, Clone the OpenPose repository:

```
git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git
cd openpose/
git submodule update --init --recursive --remote
```

Step-2, Config with CMAKE-GUI (local system only, not inside the docker):

```
mkdir build/
cd build/
cmake-gui ..
```

Step-2, Config CMAKE (terminal):

```
mkdir build/
cd build/
# CPU only
cmake -DBUILD_PYTHON=ON  -DGPU_MODE=CPU_ONLY .. && make -j `nproc`
# GPU 
cmake -DBUILD_PYTHON=ON  -DUSE_CuDNN .. && make -j `nproc`
```

Notes:
* You must ensure that BUILD_PYTHON is flagged on  
*  You can get the prototxt model files here.
    or just download models from:

    ```
    cd /app/openpose/models
    bash getModels.sh
    ```

Once you successfully installed OpenPose, copy the `openpose/` directory inside this directory one.

## Testing videos

Download test videos:

```
bash get_data.sh
python3 -m unittest discover -s ./openpose_test -p test_*.py
```

## REFERENCES

- Openpose repository
https://github.com/CMU-Perceptual-Computing-Lab/openpose
