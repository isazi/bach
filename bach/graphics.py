import cv2


def draw_bounding_box(img, label, color, x, y, w, h):
    """
    Draw a bounding box around an object.
    """
    cv2.rectangle(img, (x - (w / 2), y - (h / 2)), (x + (w / 2), y + (h / 2)), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return img
