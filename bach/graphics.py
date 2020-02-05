import cv2


def draw_bounding_box(image, entity):
    """
    Draw a bounding box around an object.
    """
    top_left = entity.top_left()
    bottom_right = entity.bottom_right()
    cv2.rectangle(image,
                  (int(top_left.x), int(top_left.y)),
                  (int(bottom_right.x), int(bottom_right.y)),
                  entity.color, 2)
    label_point = (int(top_left.x), int(top_left.y) - 10)
    cv2.putText(image,
                "{} {}".format(entity.label, entity.marker()),
                label_point,
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, entity.color, 2)
    return image


def sharpen_image(image):
    """
    Return a sharpened version of an image.
    """
    blur = cv2.GaussianBlur(image, (0, 0), 3)
    sharp = cv2.addWeighted(image, 1.5, blur, -0.5, 0)
    return sharp


def resize(image, width, height):
    """
    Resize the image using user provided width and height.
    """
    resized_image = cv2.resize(image.copy(), (width, height), interpolation=cv2.INTER_NEAREST)
    return resized_image
