import cv2


def draw_bounding_box(img, label, color, x, y, w, h):
    """
    Draw a bounding box around an object.
    """
    cv2.rectangle(img, (int(x - (w / 2)), int(y - (h / 2))), (int(x + (w / 2)), int(y + (h / 2))), color, 2)
    cv2.putText(img, label, (int(x - 10), int(y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return img
