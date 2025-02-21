# Переменные

variable "cloud_id" {
    type        = string
    description = "Идентификатор облака в Yandex Cloud"
}

variable "folder_id" {
    type        = string
    description = "Идентификатор каталога в Yandex Cloud"
}

variable "tg_bot_key" {
    type        = string
    description = "Токен Telegram бота"
}

variable "sa_name" {
    type        = string
    description = "Название сервисного аккаунта"
    default     = "sa-vvot41-face-recognizer-admin"
}

variable "sa_key_file_path" {
    type        = string
    description = "Путь к авторизованному ключу сервисного аккаунта"
    default     = "../key.json"
}

variable "yandex_zone" {
    type        = string
    description = "Зона доступности Yandex Cloud"
    default     = "ru-central1-a"
}

# Обязательные провайдеры

terraform {
    required_providers {
        yandex = {
            source = "yandex-cloud/yandex"
        }
        telegram = {
            source  = "yi-jiayu/telegram"
            version = "0.3.1"
        }
    }
    required_version = ">= 0.13"
}

provider "yandex" {
    cloud_id                 = var.cloud_id
    folder_id                = var.folder_id
    zone                     = var.yandex_zone
    service_account_key_file = pathexpand(var.sa_key_file_path)
}

provider "telegram" {
    bot_token = var.tg_bot_key
}

# Сервисный аккаунт с ролью "администратор"

resource "yandex_iam_service_account" "sa" {
    folder_id = var.folder_id 
    name      = var.sa_name
}

resource "yandex_resourcemanager_folder_iam_member" "sa_admin" {
    folder_id = var.folder_id
    role      = "admin"
    member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

resource "yandex_iam_service_account_static_access_key" "sa_static_key" {
    service_account_id = yandex_iam_service_account.sa.id
    description        = "Статический ключ доступа к Object Storage"
}
