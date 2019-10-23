import cv2


def draw_bounding_box(image, entity):
    """
    Draw a bounding box around an object.
    """
    top_left = entity.top_left()
    bottom_right = entity.bottom_right()
    cv2.rectangle(image, (top_left.x, top_left.y), (bottom_right.x, bottom_right.y), entity.color, 2)
    label_point = (top_left.x, top_left.y - 10)
    cv2.putText(image, entity.label, label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, entity.color, 2)
    return image


def sharpen_image(image):
    """
    Return a sharpened version of an image.
    """
    blur = cv2.GaussianBlur(image, (0, 0), 3)
    sharp = cv2.addWeighted(image, 1.5, blur, -0.5, 0)
    return sharp
