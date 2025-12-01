### Manual Terraform Setup

#### Prereqs:

1. Terraform:

   - Required version: >= 1.11.0
   - Download: https://developer.hashicorp.com/terraform/downloads

2. AWS CLI:
   - Download: https://aws.amazon.com/cli/
   - Configure AWS CLI with this command (have your AWS Access Key ID & AWS Secret Access Key ready):
   ```
   aws configure
   ```

#### Setup and tear down:

Call these to setup your instance:

```
terraform init
terraform plan  -var="bucket_name=<unique-bucket-name>"  -var="aws_region=us-east-1"
terraform apply -var="bucket_name=<unique-bucket-name>"  -var="aws_region=us-east-1"
```

- Once `terraform apply` is called, the website url will be outputted (see output.tf for what else is outputted).
- If the bucket already exists (same name) in another account, pass in another name for the `bucket_name` field.

Call this to destroy your instance:

```
terraform destroy
```

### Running Locally

1. **Set up a Python virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies (if any):**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**

   ```bash
   python3 server.py
   ```

4. **Open the frontend:**
   - Open `index.html` in your web browser.

## Using our service

1. **Input a public spotify playlist URL in the given input field**

2. **Click on the Analyze button to start the process**
