import cv2


def draw_bounding_box(img, label, color, x, y, w, h):
    """
    Draw a bounding box around an object.
    """
    top_left = (int(x - (w / 2)), int(y - (h / 2)))
    bottom_right = (int(x + (w / 2)), int(y + (h / 2)))
    cv2.rectangle(img, top_left, bottom_right, color, 2)
    label_point = (int(x - (w / 2)), int(y - (h / 2)) - 10)
    cv2.putText(img, label, label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return img
