#!python3
"""
Python 3 wrapper for identifying objects in images

@author: Philip Kahn
@date: 20180503
"""
from ctypes import *
import random
import os


# Global variables
net_main = None
meta_main = None
alt_names = None


def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1


def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


lib = CDLL("libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

copy_image_from_bytes = lib.copy_image_from_bytes
copy_image_from_bytes.argtypes = [IMAGE, c_char_p]


def network_width(net):
    return lib.network_width(net)


def network_height(net):
    return lib.network_height(net)


predict = lib.network_predict_ptr
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int), c_int]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict_ptr
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

load_net_custom = lib.load_network_custom
load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
load_net_custom.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

predict_image_letterbox = lib.network_predict_image_letterbox
predict_image_letterbox.argtypes = [c_void_p, IMAGE]
predict_image_letterbox.restype = POINTER(c_float)


def array_to_image(arr):
    import numpy as np
    # need to return old values to avoid python freeing memory
    arr = arr.transpose(2, 0, 1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
    data = arr.ctypes.data_as(POINTER(c_float))
    im = IMAGE(w, h, c, data)
    return im, arr


def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        if alt_names is None:
            name_tag = meta.names[i]
        else:
            name_tag = alt_names[i]
        res.append((name_tag, out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res


def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45, debug=False):
    """
    Performs the meat of the detection
    """
    im, _ = array_to_image(image)
    if debug:
        print("Loaded image")
    ret = detect_image(net, meta, im, thresh, hier_thresh, nms, debug)
    return ret


def detect_image(net, meta, im, thresh=.5, hier_thresh=.5, nms=.45, debug=False):
    num = c_int(0)
    if debug:
        print("Assigned num")
    pnum = pointer(num)
    if debug:
        print("Assigned pnum")
    predict_image(net, im)
    letter_box = 0
    # predict_image_letterbox(net, im)
    # letter_box = 1
    if debug:
        print("did prediction")
    # dets = get_network_boxes(net, custom_image_bgr.shape[1], custom_image_bgr.shape[0], thresh, hier_thresh, None, 0, pnum, letter_box) # OpenCV
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum, letter_box)
    if debug:
        print("Got dets")
    num = pnum[0]
    if debug:
        print("got zeroth index of pnum")
    if nms:
        do_nms_sort(dets, num, meta.classes, nms)
    if debug:
        print("did sort")
    res = []
    if debug:
        print("about to range")
    for j in range(num):
        if debug:
            print("Ranging on "+str(j)+" of "+str(num))
        if debug:
            print("Classes: "+str(meta), meta.classes, meta.names)
        for i in range(meta.classes):
            if debug:
                print("Class-ranging on "+str(i)+" of "+str(meta.classes)+"= "+str(dets[j].prob[i]))
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                if alt_names is None:
                    name_tag = meta.names[i]
                else:
                    name_tag = alt_names[i]
                if debug:
                    print("Got bbox", b)
                    print(name_tag)
                    print(dets[j].prob[i])
                    print((b.x, b.y, b.w, b.h))
                res.append((name_tag, dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    if debug:
        print("did range")
    res = sorted(res, key=lambda x: -x[1])
    if debug:
        print("did sort")
    free_detections(dets, num)
    if debug:
        print("freed detections")
    return res


def initialize(config_path, weight_path, meta_path):
    global meta_main, net_main, alt_names
    if not os.path.exists(config_path):
        raise ValueError("Invalid config path `" + os.path.abspath(config_path) + "`")
    if not os.path.exists(weight_path):
        raise ValueError("Invalid weight path `" + os.path.abspath(weight_path) + "`")
    if not os.path.exists(meta_path):
        raise ValueError("Invalid data file path `" + os.path.abspath(meta_path) + "`")
    if net_main is None:
        net_main = load_net_custom(config_path.encode("ascii"), weight_path.encode("ascii"), 0, 1)  # batch size = 1
    if meta_main is None:
        meta_main = load_meta(meta_path.encode("ascii"))
    if alt_names is None:
        # In Python 3, the metafile default access craps out on Windows (but not Linux)
        # Read the names file and create a list to feed to detect
        try:
            with open(meta_path) as metaFH:
                meta_contents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", meta_contents, re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            names_list = namesFH.read().strip().split("\n")
                            alt_names = [x.strip() for x in names_list]
                except TypeError:
                    pass
        except Exception:
            raise


def perform_detect(image_path="data/dog.jpg",
                   thresh=0.25,
                   config_path="./cfg/yolov3.cfg",
                   weight_path="yolov3.weights",
                   meta_path="./cfg/coco.data",
                   show_image=True,
                   make_image_only=False,
                   init_only=False):
    """
    Convenience function to handle the detection and returns of objects.

    Displaying bounding boxes requires libraries scikit-image and numpy

    Parameters
    ----------------
    image_path: str
        Path to the image to evaluate. Raises ValueError if not found

    thresh: float (default= 0.25)
        The detection threshold

    config_path: str
        Path to the configuration file. Raises ValueError if not found

    weight_path: str
        Path to the weights file. Raises ValueError if not found

    meta_path: str
        Path to the data file. Raises ValueError if not found

    show_image: bool (default= True)
        Compute (and show) bounding boxes. Changes return.

    make_image_only: bool (default= False)
        If showImage is True, this won't actually *show* the image, but will create the array and return it.

    init_only: bool (default= False)
        Only initialize globals. Don't actually run a prediction.

    Returns
    ----------------------


    When showImage is False, list of tuples like
        ('obj_label', confidence, (bounding_box_x_px, bounding_box_y_px, bounding_box_width_px, bounding_box_height_px))
        The X and Y coordinates are from the center of the bounding box. Subtract half the width or height to get the lower corner.

    Otherwise, a dict with
        {
            "detections": as above
            "image": a numpy array representing an image, compatible with scikit-image
            "caption": an image caption
        }
    """
    initialize(config_path, weight_path, meta_path)
    if init_only:
        return None
    if not os.path.exists(image_path):
        raise ValueError("Invalid image path `" + os.path.abspath(image_path) + "`")
    # Do the detection
    # detections = detect(netMain, metaMain, imagePath, thresh)	# if is used cv2.imread(image)
    detections = detect(net_main, meta_main, image_path.encode("ascii"), thresh)
    if show_image:
        try:
            from skimage import io, draw
            import numpy as np
            image = io.imread(image_path)
            print("*** "+str(len(detections))+" Results, color coded by confidence ***")
            imcaption = []
            for detection in detections:
                label = detection[0]
                confidence = detection[1]
                pstring = label+": "+str(np.rint(100 * confidence))+"%"
                imcaption.append(pstring)
                print(pstring)
                bounds = detection[2]
                shape = image.shape
                # x = shape[1]
                # xExtent = int(x * bounds[2] / 100)
                # y = shape[0]
                # y_extent = int(y * bounds[3] / 100)
                y_extent = int(bounds[3])
                x_entent = int(bounds[2])
                # Coordinates are around the center
                x_coord = int(bounds[0] - bounds[2]/2)
                y_coord = int(bounds[1] - bounds[3]/2)
                bounding_box = [
                    [x_coord, y_coord],
                    [x_coord, y_coord + y_extent],
                    [x_coord + x_entent, y_coord + y_extent],
                    [x_coord + x_entent, y_coord]
                ]
                # Wiggle it around to make a 3px border
                rr, cc = draw.polygon_perimeter([x[1] for x in bounding_box],
                                                [x[0] for x in bounding_box],
                                                shape=shape)
                rr2, cc2 = draw.polygon_perimeter([x[1] + 1 for x in bounding_box],
                                                  [x[0] for x in bounding_box],
                                                  shape=shape)
                rr3, cc3 = draw.polygon_perimeter([x[1] - 1 for x in bounding_box],
                                                  [x[0] for x in bounding_box],
                                                  shape=shape)
                rr4, cc4 = draw.polygon_perimeter([x[1] for x in bounding_box],
                                                  [x[0] + 1 for x in bounding_box],
                                                  shape=shape)
                rr5, cc5 = draw.polygon_perimeter([x[1] for x in bounding_box],
                                                  [x[0] - 1 for x in bounding_box],
                                                  shape=shape)
                box_color = (int(255 * (1 - (confidence ** 2))), int(255 * (confidence ** 2)), 0)
                draw.set_color(image, (rr, cc), box_color, alpha=0.8)
                draw.set_color(image, (rr2, cc2), box_color, alpha=0.8)
                draw.set_color(image, (rr3, cc3), box_color, alpha=0.8)
                draw.set_color(image, (rr4, cc4), box_color, alpha=0.8)
                draw.set_color(image, (rr5, cc5), box_color, alpha=0.8)
            if not make_image_only:
                io.imshow(image)
                io.show()
            detections = {
                "detections": detections,
                "image": image,
                "caption": "\n<br/>".join(imcaption)
            }
        except Exception as e:
            print("Unable to show image: "+str(e))
    return detections

