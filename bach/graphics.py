import cv2


def draw_bounding_box(image, entity, color):
    """
    Draw a bounding box around an object.
    """
    cv2.rectangle(image, entity.top_left(), entity.bottom_right(), color, 2)
    label_point = (int(entity.position.x - (entity.width / 2)), int(entity.position.y - (entity.height / 2)) - 10)
    cv2.putText(image, entity.label, label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image


def sharpen_image(image):
    """
    Return a sharpened version of an image.
    """
    blur = cv2.GaussianBlur(image, (0, 0), 3)
    sharp = cv2.addWeighted(image, 1.5, blur, -0.5, 0)
    return sharp
