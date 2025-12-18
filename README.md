# AWS EC2 CLI Automation using Python

## 📌 Overview

This project provides a **Python-based automation tool** to manage **AWS EC2 instances** using the **AWS CLI** (not boto3). It is designed for engineers who want **CLI-driven automation**, logging, and state monitoring without SDK dependencies.

You can perform the following operations:

* Start EC2 instances
* Stop EC2 instances
* Reboot EC2 instances
* Terminate EC2 instances
* Monitor instance state until it reaches the desired status
* Fetch instance details (Name, State, Private IP, Public IP)

---

## 🧠 Architecture & Flow

The script internally calls AWS CLI commands using the `sh` Python module and parses JSON responses.

---

##  Features

* ✅ No boto3 dependency (CLI-only)
* ✅ Supports single, multiple, or all EC2 instances
* ✅ Polling-based state monitoring
* ✅ Structured logging (file + console)
* ✅ JSON output for easy integration

---

## 🔧 Prerequisites

### 1️⃣ System Requirements

* Linux / macOS / WSL
* Python 3.7+

### 2️⃣ Install AWS CLI

```bash
sudo apt install awscli -y
aws --version
```

### 3️⃣ Install Python Dependencies

```bash
pip install sh
```

### 4️⃣ AWS IAM Permissions

The IAM user must have at least:

```json
{
  "Effect": "Allow",
  "Action": [
    "ec2:DescribeInstances",
    "ec2:StartInstances",
    "ec2:StopInstances",
    "ec2:RebootInstances",
    "ec2:TerminateInstances"
  ],
  "Resource": "*"
}
```

---

## 🧪 Usage

### ▶️ Basic Command Structure

#### Command for performing on all instances 
```bash
python script.py \
  --key_id <AWS_ACCESS_KEY_ID> \
  --access_key <AWS_SECRET_ACCESS_KEY> \
  --region <region> \
  --operation <start or stop or reboot or terminate> \
  --all
```

```bash
python ec2_operations.py \
  --key_id <AWS_ACCESS_KEY_ID> \
  --access_key <AWS_SECRET_ACCESS_KEY> \
  --region <region> \
  --operation <start or stop or reboot or terminate > \
  --instance_id i-0123456789abcdef
```

---

## ⚙️ Command-Line Arguments

| Argument        | Required | Description                       |
| --------------- | -------- | --------------------------------- |
| `--key_id`      | ✅        | AWS Access Key ID                 |
| `--access_key`  | ✅        | AWS Secret Access Key             |
| `--region`      | ✅        | AWS Region                        |
| `--operation`   | ✅        | start / stop / reboot / terminate |
| `--instance_id` | ❌        | One or more EC2 instance IDs      |
| `--all`         | ❌        | Apply operation to all instances  |

---

## 🔄 Operations Explained

### ▶️ Start Instance

```bash
--operation start
```

Target state: `running`

### ⏹ Stop Instance

```bash
--operation stop
```

Target state: `stopped`

### 🔁 Reboot Instance

```bash
--operation reboot
```

Target state: `running`

### ❌ Terminate Instance

```bash
--operation terminate
```

Target state: `terminated`

---

## ⏳ Monitoring Logic

The script:

1. Calls `describe-instances`
2. Reads instance state
3. Polls every **10 seconds**
4. Retries **10 times**
5. Exits when desired state is reached

This prevents false success reporting.

---

## 📝 Logging

Log file example:

```
ec2_operations_14_32_10.log
```

Log format:

```
2025-12-18 14:32:15 - INFO - line 120 - All instances reached state: running
```

Logs are written to:

* Console (stdout)
* Timestamped log file

---

## 📤 Output Format

Final output is printed in JSON:

```json
[
  {
    "InstanceId": "i-0123456789abcdef",
    "Name": "web-server",
    "State": "running",
    "Private IP": "172.31.10.12",
    "Public IP": "3.110.45.22"
  }
]
```

---

## ⚠️ Common Errors & Fixes

### ❌ UnauthorizedOperation

**Cause:** Missing IAM permission

**Fix:** Attach EC2 permissions to IAM user

---

### ❌ No instance IDs provided

**Cause:** Forgot `--instance_id` or `--all`

**Fix:** Provide at least one

---

## 🧩 Design Decisions

* AWS CLI instead of boto3 → easier debugging
* Explicit state polling → reliable automation
* No global state → predictable behavior

---

## 📈 Enhancements (Future)

* Parallel instance monitoring
* Retry with exponential backoff
* CloudWatch logging
* Dry-run mode
* YAML config support

---

## 👤 Author

**Md Haider Ali**
Python Developer | Cloud Automation

---

## ✅ Conclusion

This script is ideal for **cloud engineers**, **DevOps**, and **SREs** who want a **lightweight, transparent EC2 automation tool** without SDK overhead.

Feel free to extend it for Auto Scaling, Load Balancers, or multi-account autom
