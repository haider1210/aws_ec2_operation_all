# Run AWS EC2 CLI Automation (Linux & Windows)

---

## 🐧 Linux / WSL Commands

### 1. Update System & Install Dependencies

```bash
sudo apt update
sudo apt install -y python3-full python3-venv awscli
```

### 2. Verify Installations

```bash
python3 --version
aws --version
```

### 3. Create Project Directory

```bash
mkdir ec2-cli-automation
cd ec2-cli-automation
```

### 4. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Python Dependencies

```bash
pip install sh
```

## 🪟 Windows (PowerShell) Commands

### 1. Install Python & AWS CLI

```powershell
winget install Python.Python.3
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

### 2. Verify Installations

```powershell
python --version
aws --version
```

### 3. Create Project Directory

```powershell
mkdir ec2-cli-automation
cd ec2-cli-automation
```

### 4. Create & Activate Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If activation fails:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 5. Install Python Dependencies

```powershell
pip install sh
```

---

## ✅ Supported Operations

```text
start
stop
reboot
terminate
```

---

## 📌 Output Example

```json
[
  {
    "InstanceId": "i-0123456789abcdef0",
    "Name": "web-server",
    "State": "running",
    "Private IP": "10.0.1.15",
    "Public IP": "13.232.45.10"
  }
]
```
