def cut_face(image, face_coordinates):
    left, upper, w, h = face_coordinates
    right = left + w
    lower = upper + h

    return image.crop((left, upper, right, lower))