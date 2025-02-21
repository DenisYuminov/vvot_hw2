variable "database_name" {
    type    = string
    default = "vvot41-db"
}

resource "yandex_ydb_database_serverless" "database" {
    name                = var.database_name
    deletion_protection = false

    serverless_database {
        enable_throttling_rcu_limit = false
        provisioned_rcu_limit       = 10
        throttling_rcu_limit        = 0
        storage_size_limit          = 5
    }
}

resource "yandex_ydb_table" "database_table" {
    path              = "photos"
    connection_string = yandex_ydb_database_serverless.database.ydb_full_endpoint
    
    primary_key = ["face_id"]
    
    column {
        name     = "photo_id"
        type     = "String"
        not_null = true
    }
    column {
        name     = "face_id"
        type     = "String"
        not_null = true
    }
    column {
        name     = "face_name"
        type     = "String"
        not_null = false
    }
    column {
        name     = "is_processing"
        type     = "Bool"
        not_null = true
    }
}