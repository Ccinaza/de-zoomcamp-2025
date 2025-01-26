variable "project" {
  description = "My Project "
  default     = "smiling-audio-448313-p0"
}

variable "location" {
  description = "My Project Location"
  default     = "EU"
}

variable "region" {
  description = "My Project region"
  default     = "europe-west1"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "smiling-audio-448313-p0-terra-bucket"
}

variable "gcs_storage_class" {
  description = "My Bucket Storage Class"
  default     = "STANDARD"
}