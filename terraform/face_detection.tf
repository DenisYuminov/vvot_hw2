# Переменные

variable "face_detection_fun_name" {
    type        = string
    description = "Название функции-обработчика, которая обнаруживает лица на оригинальной фотографии"
    default     = "vvot41-face-detection"
}

variable "photos_bucket_name" {
    type        = string
    description = "Название бакета с оригинальными фотографиями"
    default     = "vvot41-photos"
}

variable "tasks_queue_name" {
    type        = string
    description = "Название очереди сообщений с заданиями на создание фотографии лица"
    default     = "vvot41-tasks"
}

variable "upload_photo_trigger_name" {
    type        = string
    description = "Название триггера для запуска обработчика `face-detection`"
    default     = "vvot41-photo"
}

# Ресурсы

resource "yandex_function" "face_detection_fun" {
    name               = var.face_detection_fun_name
    entrypoint         = "index.handler"
    runtime            = "python312"
    user_hash          = data.archive_file.face_detection.output_sha256
    memory             = 256
    execution_timeout  = 30
    service_account_id = yandex_iam_service_account.sa.id
    environment = {
        PHOTOS_BUCKET     = yandex_storage_bucket.photos_bucket.bucket
        MESSAGE_QUEUE_URL = yandex_message_queue.tasks_queue.id
        ACCESS_KEY        = yandex_iam_service_account_static_access_key.sa_static_key.access_key
        SECRET_KEY        = yandex_iam_service_account_static_access_key.sa_static_key.secret_key
    }
    content {
        zip_filename = data.archive_file.face_detection.output_path
    }
    mounts {
        name = yandex_storage_bucket.photos_bucket.bucket
        mode = "ro"
        object_storage {
            bucket = yandex_storage_bucket.photos_bucket.bucket
        }
    }
}

resource "yandex_storage_bucket" "photos_bucket" {
    bucket        = var.photos_bucket_name
    force_destroy = true
}

resource "yandex_message_queue" "tasks_queue" {
    name                       = var.tasks_queue_name
    access_key                 = yandex_iam_service_account_static_access_key.sa_static_key.access_key
    secret_key                 = yandex_iam_service_account_static_access_key.sa_static_key.secret_key
    visibility_timeout_seconds = 1200
    receive_wait_time_seconds  = 20
}

resource "yandex_function_trigger" "upload_photo_trigger" {
    name        = var.upload_photo_trigger_name
    description = "Триггер в ответ на загрузку оригинальной фотографии в бакет `photos_bucket`"
    object_storage {
        bucket_id    = yandex_storage_bucket.photos_bucket.id
        suffix       = ".jpg"
        create       = true
        batch_cutoff = 3
    }
    function {
        id                 = yandex_function.face_detection_fun.id
        service_account_id = yandex_iam_service_account.sa.id
        retry_attempts     = 3
        retry_interval     = 20
    }
}

# ZIP-архив

data "archive_file" "face_detection" {
    type        = "zip"
    source_dir  = "../src/face_detection"
    output_path = "../build/face_detection.zip"
}
