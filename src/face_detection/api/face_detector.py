import cv2


def get_faces_coordinates(image_path):
    """Извлекает координаты лиц на изображении с учетом масштабирования."""
    image = cv2.imread(image_path)
    
    # Максимально допустимые размеры
    max_allowed_width, max_allowed_height = 1920, 1080

    # Получаем исходные размеры изображения
    original_image_height, original_image_width = image.shape[:2]

    # Масштабируем изображение, если оно превышает допустимые размеры
    if original_image_width > max_allowed_width or original_image_height > max_allowed_height:
        scaling_factor = min(max_allowed_width / original_image_width, max_allowed_height / original_image_height)
        image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        
        # Дополнительное масштабирование для улучшения распознавания
        additional_scaling_factor = 0.90
        scaled_width, scaled_height = int(image.shape[1] * additional_scaling_factor), int(image.shape[0] * additional_scaling_factor)
        image = cv2.resize(image, (scaled_width, scaled_height), interpolation=cv2.INTER_AREA)

    # Получаем размеры уже уменьшенного изображения
    resized_image_height, resized_image_width = image.shape[:2]

    # Переводим изображение в черно-белое для улучшения распознавания лиц
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Загрузка классификатора для лиц
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

    # Обнаружение лиц на изображении
    detected_faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    original_scale_faces = []

    # Преобразуем координаты лиц обратно в исходные размеры
    for (x, y, width, height) in detected_faces:
        x_original = int(x * (original_image_width / resized_image_width))
        y_original = int(y * (original_image_height / resized_image_height))
        width_original = int(width * (original_image_width / resized_image_width))
        height_original = int(height * (original_image_height / resized_image_height))
        
        # Добавляем координаты в список
        original_scale_faces.append([x_original, y_original, width_original, height_original])

    return original_scale_faces
