variable "ddb_table_name" {
  type        = string
  description = "DynamoDB table name"
  default     = "lyriclens-db"
}

variable "hash_key" {
  type        = string
  default     = "id"
}

variable "attributes" {
  description = "Attribute definitions for keys (and any GSIs)"
  type        = list(
                  object({ 
                    name = string, 
                    type = string     # "S" = string | "N" = number | "B" = binary
                  }))
  default     = [{ name = "id", type = "S" }]
}