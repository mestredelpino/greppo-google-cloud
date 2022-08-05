provider "google" {
  project     = var.project_name
  region      = var.gcp_region
}

# # ----------------------------------- NETWORK ----------------------------------- #

# resource "google_compute_network" "vpc_network" {
#   project                 = var.project_name
#   name                    = var.vpc_name
#   auto_create_subnetworks = false
# }

# resource "google_compute_subnetwork" "vpc_subnets" {
#   for_each =  { for index, subnet in var.vpc_subnets: subnet.name => subnet }
#   name          = each.value.name
#   ip_cidr_range = each.value.ip_cidr_range
#   region        = var.gcp_region
#   network       = google_compute_network.vpc_network.id
#   secondary_ip_range {
#     ip_cidr_range = each.value.secondary_ip_range_1
#     range_name    = "${each.value.name}-secondary-range-1"
#   }
#   secondary_ip_range {
#     ip_cidr_range = each.value.secondary_ip_range_2
#     range_name    = "${each.value.name}-secondary-range-2"
#   }
# }

# ----------------------------------- STORAGE ----------------------------------- #

resource "google_storage_bucket" "greppo-data" {
  name          = var.bucket_name
  location      = var.bucket_location
  force_destroy = true
  storage_class = "STANDARD"
}

data "http" "data" {
  for_each =  { for index, object in var.bucket_objects: object.name => object if can(object.url)}
  url = each.value.url
}

data "local_file" "data" {
  for_each =  { for index, object in var.bucket_objects: object.name => object if can(object.local_file)}
  filename = each.value.local_file
}

resource "google_storage_bucket_object" "bucket_objects" {
  for_each =  { for index, object in var.bucket_objects: object.name => object }
  name   = each.value.name
  content = can(each.value.url) ? data.http.data[each.value.name].body : base64decode(data.local_file.data[each.value.name].content_base64)
  bucket = var.bucket_name
}

resource "google_artifact_registry_repository" "my-repo" {
  location      = var.gcp_region
  repository_id = var.repository_name
  description   = "Docker repository for the application's container images"
  format        = "DOCKER"
}


# ----------------------------------- FUNCTIONS ----------------------------------- #



resource "google_cloudfunctions_function" {
  name                         = "bucket_geojson_to_bq"
  description                  = "This function converts a geojson file contained in a Cloud Storage Bucket into a Bigquery table"
  runtime                      = "python39"
  available_memory_mb          = 512
  trigger_http                 = true   
  https_trigger_security_level = "SECURE_ALWAYS"
  timeout                      = 60      
  entry_point                  = "bucket_geojson_to_bq"
}


