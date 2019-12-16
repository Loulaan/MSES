import argparse
from sys import platform

from models import *  # set ONNX_EXPORT in models.py
from utils.datasets import *
from utils.utils import *

from sort import *
import numpy as np

import warnings

warnings.filterwarnings("ignore")

timeCutoffTrafficControl = 3 * 60  # 3 min cutoff before throwing another signal to proper traffic control
v1 = [-100, 100]  # Vector of the first direction of the road
v2 = [100, -100]  # Vector of the second direction of the road
outputDirection = ""

cfg = 'cfg/yolov3.cfg'
data = 'newData/newData.data'
weights = 'weights/best.pt'
out = 'WEB_DATA/out/'
half = False
img_size = 416
conf_thres = 0.3
nms_thres = 0.5
fourcc = 'avc1'
view_img = False
webcam = False

# Initialize
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if not os.path.exists(out):
    os.makedirs(out)  # delete output folder

# Initialize model
model = Darknet(cfg, img_size)

# Load weights
attempt_download(weights)
model.load_state_dict(torch.load(weights, map_location=device)['model'])

# Eval mode
model.to(device).eval()

# Set Dataloader
vid_path, vid_writer = None, None

# Get classes and colors
classes = load_classes(parse_data_cfg(data)['names'])
colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))]

# Initilize SORT object
mot_tracker = Sort()


def inference(source, save_txt=False, save_img=False):
    global vid_path
    global vid_writer
    dataset = LoadImages(source, img_size=img_size, half=half)
    # Run inference
    tracksUniqueObj = dict()
    cutoffTrafficControl = 0
    for path, img, im0s, vid_cap in dataset:
        # Get detections
        img = torch.from_numpy(img).to(device)
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, nms_thres)

        # Process detections
        for det in pred:  # detections per image
            p, _, im0 = path, '', im0s

            # Handle cutoff before throwing another command to traffic control
            if cutoffTrafficControl != 0:
                if cutoffTrafficControl % timeCutoffTrafficControl == 0:
                    cutoffTrafficControl = 0
                cutoffTrafficControl += 1

            save_path = str(Path(out) / Path(p).name)
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                tracked_objects = mot_tracker.update(det.cpu())
                for *xyxy, obj_id, cls_pred in tracked_objects:
                    obj_id = int(obj_id)
                    xyxy = [int(c) for c in xyxy]
                    if obj_id in tracksUniqueObj.keys():
                        tracksUniqueObj[obj_id].append([xyxy])
                    else:
                        tracksUniqueObj[obj_id] = [[xyxy]]

                    if len(tracksUniqueObj[obj_id]) == 10:
                        x1, y1 = tracksUniqueObj[obj_id][4][0][2:]
                        x2, y2 = tracksUniqueObj[obj_id][9][0][2:]
                        u = [x2 - x1, y2 - y1]
                        angle1 = np.arccos(np.clip(np.dot(u, v1) / np.linalg.norm(u) / np.linalg.norm(v1), -1, 1))
                        angle2 = np.arccos(np.clip(np.dot(u, v2) / np.linalg.norm(u) / np.linalg.norm(v2), -1, 1))
                        if angle1 < angle2:
                            outputDirection = 'left'
                        else:
                            outputDirection = 'right'
                        cutoffTrafficControl += 1

                    cls = classes[int(cls_pred)]
                    color = colors[int(obj_id) % len(colors)]
                    label = '%s - %d' % (cls, int(obj_id))
                    plot_one_box(xyxy, im0, label=label, color=color)

        # Save results (image with detections)
        if vid_path != save_path:  # new video
            vid_path = save_path
            if isinstance(vid_writer, cv2.VideoWriter):
                vid_writer.release()  # release previous video writer

            fps = vid_cap.get(cv2.CAP_PROP_FPS)
            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
        vid_writer.write(im0)
    vid_writer.release()
    return {'direction': outputDirection}