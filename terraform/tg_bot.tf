# Переменные

variable "tg_bot_fun_name" {
    type        = string
    description = "Название функции-обработчика, которая обрабатывает сообщения, отправляемые Telegram боту"
    default     = "vvot41-tg-bot"
}

# Ресурсы

resource "yandex_function" "tg_bot_fun" {
    name               = var.tg_bot_fun_name
    entrypoint         = "index.handler"
    runtime            = "python312"
    user_hash          = data.archive_file.tg_bot.output_sha256
    memory             = 128
    execution_timeout  = 30
    service_account_id = yandex_iam_service_account.sa.id
    environment = {
        TG_BOT_KEY    = var.tg_bot_key
        PHOTOS_BUCKET = yandex_storage_bucket.photos_bucket.bucket
        FACES_BUCKET  = yandex_storage_bucket.faces_bucket.bucket
        API_GW_URL    = "https://${yandex_api_gateway.api_gw.domain}"
        YDB_ENDPOINT  = yandex_ydb_database_serverless.database.ydb_api_endpoint
        YDB_PATH      = yandex_ydb_database_serverless.database.database_path
    }
    content {
        zip_filename = data.archive_file.tg_bot.output_path
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

resource "yandex_function_iam_binding" "tg_bot_fun_iam_binding" {
    function_id = yandex_function.tg_bot_fun.id
    role        = "functions.functionInvoker"
    members     = [ "system:allUsers" ]
}

resource "telegram_bot_webhook" "tg_bot_webhook" {
    url = "https://functions.yandexcloud.net/${yandex_function.tg_bot_fun.id}"
}

# ZIP-архив

data "archive_file" "tg_bot" {
    type        = "zip"
    source_dir  = "../src/tg_bot"
    output_path = "../build/tg_bot.zip"
}
