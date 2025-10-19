# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"  # Set AWS region to US East 1 (N. Virginia)
}

# Local variables block for configuration values
locals {
    aws_key = "SWEN_AWS_KEY"   # SSH key pair name for EC2 instance access
}

data "aws_subnets" "in_vpc" {
  filter {
    name   = "vpc-id"
    values = ["vpc-09c21db1f2350ca56"]
  }
}

# security group setup
resource "aws_security_group" "wp_sg" {
  name   = "wp-sg"
  vpc_id = "vpc-09c21db1f2350ca56"

  ingress { 
      from_port = 80 
      to_port = 80 
      protocol = "tcp" 
      cidr_blocks = ["0.0.0.0/0"] 
  }
  ingress { 
      from_port = 22 
      to_port = 22 
      protocol = "tcp" 
      cidr_blocks = ["0.0.0.0/0"] 
  }
  egress  { 
      from_port = 0  
      to_port = 0  
      protocol = "-1"  
      cidr_blocks = ["0.0.0.0/0"] 
  }
}

# EC2 instance resource definition
resource "aws_instance" "my_server" {
   ami           = data.aws_ami.amazonlinux.id  # Use the AMI ID from the data source
   instance_type = var.instance_type            # Use the instance type from variables
   key_name      = "${local.aws_key}"          # Specify the SSH key pair name
   subnet_id                   = data.aws_subnets.in_vpc.ids[0]
   associate_public_ip_address = true 
   vpc_security_group_ids = [aws_security_group.wp_sg.id]

   user_data = file("wp_install.sh")
  
   # Add tags to the EC2 instance for identification
   tags = {
     Name = "my ec2"
   }                  
}

terraform {
  required_version = ">= 1.11.0"
  backend "s3" {
    bucket = "github-devops-bucket9468"
    key = "prod/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    use_lockfile = true
  }
}