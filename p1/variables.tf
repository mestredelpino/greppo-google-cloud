variable "project_name" {
   description = "Your GCP Project Name"
   type        = string
}

variable "gcp_region" {
   description = "The GCP region you want to deploy your resources to"
   type        = string
   default     = "europe-west4"
}

# variable "vpc_name" {
#    description = "The name of the VPC that will be created"
#    type        = string
# }

# variable "vpc_subnets" {
#    description = "The subnets contained in the main VPC"
#    type        = list
# }

variable "bucket_name" {
   description = "The name of the bucket to create"
   type        = string
}

variable "bucket_location" {
   description = "The location of the bucket"
   type        = string
   default     = "EU"
}

variable "bucket_objects" {
   description = "The files to upload to the newly created bucket"
   type        = list
}

variable "repository_name" {
   description = "The name of the repository where container images will be stored"
   type        = string
   default     = "example-repo"
}
