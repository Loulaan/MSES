# Introduction

This directory contains PyTorch YOLOv3 software developed by Ultralytics LLC, and **is freely available for redistribution under the GPL-3.0 license**. For more information please visit https://www.ultralytics.com.  
YOLOv3 was taken from [here](https://github.com/ultralytics/yolov3), and was upgraded for the emergency venicle detection and tracking task.

# Requirements

Python 3.7 or later with the following `pip3 install -U -r requirements.txt` packages:

- `cython`
- `numpy`
- `torch >= 1.1.0`
- `opencv-python`
- `tqdm`
- `numba`
- `scikit-learn`
- `scikit-image`
- `filterpy`

And may be smth else :)


# Docker

[DockerHub repository](https://hub.docker.com/repository/docker/morememes/emergancy-tracker)

### Image

Downloading docker image from dockerhub: `docker push morememes/emergancy-tracker:tagname`

Building docker image from dockerfile: `docker build -t morememes/emergancy-tracker:latest .`

### Container

Run container: `docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all -v $(pwd)/weights:/MSES/weights -v $(pwd)/newData:/MSES/newData -it -p 6006:6006 -p 8888:8888 morememes/emergancy-tracker:latest`

`--runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all` - gpu visibility in the container.

`-v localDir:containerDir` - mapping directories.

`-p localPort:containerPort` - mapping network ports.

Use `bash create_dirs.sh` for fast creating directories.

### Fast install

```bash
bash create_dirs.sh && docker build -t morememes/emergancy-tracker:latest . && docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all -v $(pwd)/weights:/MSES/weights -v $(pwd)/newData:/MSES/newData -it -p 6006:6006 -p 8888:8888 morememes/emergancy-tracker:latest
```

# Training
Any information that you may need to train placed also [here](https://github.com/ultralytics/yolov3) as well as the way to use this software to `transfer-learning`, `resume training` and ect.

# Inference

`detect.py` runs inference on any sources:

```bash
python3 detect.py --source ...
```

- Image:  `--source file.jpg`
- Video:  `--source file.mp4`
- Directory:  `--source dir/`
- Webcam:  `--source 0`
- RTSP stream:  `--source rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa`
- HTTP stream:  `--source http://wmccpinetop.axiscam.net/mjpg/video.mjpg`

To run a model with track objects you just need to add `--track`:

**YOLOv3:** `python3 detect.py --cfg cfg/yolov3.cfg --weights weights/best.pt --source newData/inference/ --track`  
<img src="https://sun9-47.userapi.com/c856028/v856028577/145171/1i6d4UnfrZQ.jpg" width="500">


# Pretrained Weights and Dataset

Download from:  
[Weights](https://yadi.sk/d/OgioXcWDZN7LwA)  
[Dataset](https://yadi.sk/d/jyaTM7cd6-DV0Q)


# Literature
- [YOLOv3](https://arxiv.org/pdf/1804.02767.pdf) 
- [SORT](https://arxiv.org/pdf/1602.00763.pdf)
