variable "function_name"   { type = string }
variable "filename"        { type = string }  # path to the ZIP file
variable "handler"         { type = string }  # e.g., "bedrock_lambda.handler"
variable "runtime"         { 
    type = string
    default = "python3.11"
    
}

# where images will be written
variable "bucket_name"     { type = string }
variable "bucket_arn"      { type = string }
variable "image_prefix"    { 
    type = string  
    default = "generated/" 
}

# Bedrock + env config
variable "model_id"        { type = string }  # e.g., "amazon.titan-image-generator-v2:0"
variable "aws_region"      { type = string }
variable "url_expiry_secs" { 
    type = number  
    default = 900 
}

# Lambda sizing
variable "timeout"         { 
    type = number
    default = 60
}
variable "memory_size"     { 

    type = number
    default = 1024
}

variable "tags"            { 
    type = map(string)  
    default = {} 
}
