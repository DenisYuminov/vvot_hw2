# Переменные

variable "api_gw_name" {
    type        = string
    description = "Название Yandex API Gateway"
    default     = "vvot41-apigw"
}

variable "api_gw_fun_name" {
    type        = string
    description = "Название функции-обработчика, которая выступает прокси для Yandex API Gateway"
    default     = "vvot41-apigw-fun"
}

# Ресурсы

resource "yandex_function" "api_gw_fun" {
    name               = var.api_gw_fun_name
    entrypoint         = "index.handler"
    runtime            = "python312"
    user_hash          = data.archive_file.api_gw_zip.output_sha256
    memory             = 128
    execution_timeout  = 30
    service_account_id = yandex_iam_service_account.sa.id
    environment = {
        PHOTOS_BUCKET = yandex_storage_bucket.photos_bucket.bucket
        FACES_BUCKET  = yandex_storage_bucket.faces_bucket.bucket
    }
    content {
        zip_filename = data.archive_file.api_gw_zip.output_path
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
        mode = "ro"
        object_storage {
            bucket = yandex_storage_bucket.faces_bucket.bucket
        }
    }
}

resource "yandex_api_gateway" "api_gw" {
    name = var.api_gw_name
    spec = <<-EOT
        openapi: "3.0.0"
        info:
          version: 1.0.0
          title: Face Recognizer API
        paths:
          /:
            get:
              summary: Get images with faces by key
              parameters:
                - name: face
                  in: query
                  description: Key of the object with face image 
                  required: true
                  schema:
                    type: string
              x-yc-apigateway-integration:
                type: cloud_functions
                tag: $latest
                function_id: ${yandex_function.api_gw_fun.id}    
                service_account_id: ${yandex_iam_service_account.sa.id} 
          /original_photo:
            get:
              summary: Get original photo
              parameters:
                - name: original_photo
                  in: query
                  required: true
                  schema:
                    type: string
              x-yc-apigateway-integration:
                type: cloud_functions
                tag: $latest
                function_id: ${yandex_function.api_gw_fun.id}    
                service_account_id: ${yandex_iam_service_account.sa.id}      
    EOT
}

data "archive_file" "api_gw_zip" {
    type        = "zip"
    source_dir  = "../src/api_gateway"
    output_path = "../build/api_gateway.zip"
}
