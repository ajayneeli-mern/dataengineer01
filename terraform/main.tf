terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

# Create a folder on Windows
resource "local_file" "folder_marker" {
  content  = "This folder was created by Terraform"
  filename = "${path.cwd}/my_terraform_folder/.terraform_marker2"
}

resource "null_resource" "run_extract_script" {
  provisioner "local-exec" {
    command = "python3 /opt/airflow/project_root/extract.py"
  }
}
