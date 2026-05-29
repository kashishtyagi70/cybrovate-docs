# Installing Agent on RHEL Machine

## Agent Installation Guide

Choose your preferred RHEL agent package.

---

# Installing Agent on RHEL Machine

Silent installation using the command-line interface.

## 1. Copy Package to Installation Directory

Download and place the installer package in the `/tmp` directory:

```text
/tmp/cyb-prod_datacenter_agent_rhel_v<version>.rpm
```

> **Note:** All commands below must be executed from the same directory where the `.rpm` package is downloaded.

---

## 2. Open Terminal with Administrator Privileges

Use an account with permission to install software and manage services.

---

## 3. Install the Agent

Run the installer package:

```bash
sudo SECRET=xxxx-xxxx-xxxx-xxxxx rpm -ivh cyb-prod_datacenter_agent_rhel_v<version>.rpm
```

### Expected Output

```text
Preparing...
Updating / installing...
cyb-prod_datacenter_agent_rhel-<version>
```

---

## 4. Start the Service

Start the Cybrovate Agent service:

```bash
sudo systemctl start cybrovateclientagent
```

### Verify Service Status

Check whether the service is running:

```bash
systemctl status cybrovateclientagent
```

### Expected Output

```text
● cybrovateclientagent.service - Cybrovate Client Agent
   Loaded: loaded
   Active: active (running)
```

---

## 5. Uninstall the Agent

### Stop the Service

Before uninstalling, stop the Cybrovate Agent service:

```bash
sudo systemctl stop cybrovateclientagent
```

### Remove the Package

```bash
sudo SECRET=xxxx-xxxx-xxxx-xxxxx rpm -e cyb-prod_datacenter_agent
```

---

## Verify Uninstallation

Verify that the package has been removed:

```bash
rpm -qa | grep cyb
```

No Cybrovate package entries should be displayed.

---

## Troubleshooting

### Installation Failed

Verify package integrity:

```bash
rpm -K cyb-prod_datacenter_agent_rhel_v<version>.rpm
```

Check for dependency issues:

```bash
sudo yum check
```

or on newer RHEL versions:

```bash
sudo dnf check
```

---

### Service Not Running

Restart the service:

```bash
sudo systemctl restart cybrovateclientagent
```

Verify status:

```bash
systemctl status cybrovateclientagent
```

---

### View Agent Logs

```bash
sudo journalctl -u cybrovateclientagent -f
```

---

## Download Agent

[⬇ Download RHEL Agent](/downloads/cyb-prod_datacenter_agent_rhel_v<version>.rpm)