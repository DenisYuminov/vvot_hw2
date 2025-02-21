# Переменные

variable "face_cut_fun_name" {
    type        = string
    description = "Название функции-обработчика, которая создает фотографию лица"
    default     = "vvot41-face-cut"
}

variable "faces_bucket_name" {
    type        = string
    description = "Название бакета с изображениями лиц"
    default     = "vvot41-faces"
}

variable "face_cut_trigger_name" {
    type        = string
    description = "Название триггера для запуска обработчика `face-cut`"
    default     = "vvot41-task"
}

# Ресурсы

resource "yandex_function" "face_cut_fun" {
    name               = var.face_cut_fun_name
    entrypoint         = "index.handler"
    runtime            = "python312"
    user_hash          = data.archive_file.face_cut.output_sha256
    memory             = 128
    execution_timeout  = 30
    service_account_id = yandex_iam_service_account.sa.id
    environment = {
        PHOTOS_BUCKET = yandex_storage_bucket.photos_bucket.bucket
        FACES_BUCKET  = yandex_storage_bucket.faces_bucket.bucket
        ACCESS_KEY    = yandex_iam_service_account_static_access_key.sa_static_key.access_key
        SECRET_KEY    = yandex_iam_service_account_static_access_key.sa_static_key.secret_key
        YDB_ENDPOINT  = yandex_ydb_database_serverless.database.ydb_api_endpoint
        YDB_PATH      = yandex_ydb_database_serverless.database.database_path
    }
    content {
        zip_filename = data.archive_file.face_cut.output_path
    }
    mounts {
        name = yandex_storage_bucket.photos_bucket.bucket
        mode = "ro"
        object_storage {
            bucket = yandex_storage_bucket.photos_bucket.bucket
        }
    }
    mounts {
        name = yandex_storage_bucket.faces_bucket.bucket
        mode = "rw"
        object_storage {
            bucket = yandex_storage_bucket.faces_bucket.bucket
        }
    }
}

resource "yandex_storage_bucket" "faces_bucket" {
    bucket        = var.faces_bucket_name
    force_destroy = true
}

resource "yandex_function_trigger" "face_cut_trigger" {
    name = var.face_cut_trigger_name
    message_queue {
        queue_id           = yandex_message_queue.tasks_queue.arn
        service_account_id = yandex_iam_service_account.sa.id
        batch_cutoff       = "4"
        batch_size         = "4"
    }
    function {
        id                 = yandex_function.face_cut_fun.id
        service_account_id = yandex_iam_service_account.sa.id
    }
}

# ZIP-архив

data "archive_file" "face_cut" {
    type        = "zip"
    source_dir  = "../src/face_cut"
    output_path = "../build/face_cut.zip"
}