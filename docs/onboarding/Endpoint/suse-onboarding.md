# Installing Agent on SUSE

## Agent Installation Guide

Choose your preferred SUSE agent package.

---

# Installing Agent on SUSE

Silent installation using the command-line interface.

## 1. Copy Package to Installation Directory

Download and place the installer package in the current directory:

```text
cyb_datacenter_agent_suse_v<version>.rpm
```

> **Note:** All commands below must be executed from the same directory where the `.rpm` package is downloaded.

---

## 2. Open Terminal with Administrator Privileges

Use an account with permission to install software and manage services.

Verify sudo access:

```bash
sudo whoami
```

Expected output:

```text
root
```

---

## 3. Run Installation Command

Install the Cybrovate Agent package:

```bash
sudo SECRET=xxxx-xxxx-xxxx-xxxxx zypper install --allow-unsigned-rpm ./cyb_datacenter_agent_suse_v<version>.rpm
```

### Expected Output

```text
Loading repository data...
Reading installed packages...
Installing: cybrovate-client-agent
```

---

## 4. Verify Service Status

Check whether the Cybrovate Agent service is running:

```bash
systemctl status cybrovateremoteclientagent
```

### Expected Output

```text
● cybrovateremoteclientagent.service - Cybrovate Remote Client Agent
   Loaded: loaded
   Active: active (running)
```

---

## 5. Restart Services

Restart the Cybrovate Agent service:

```bash
sudo systemctl restart cybrovateremoteclientagent
```

Verify the service status again:

```bash
systemctl status cybrovateremoteclientagent
```

---

## 6. Uninstall the Agent

Remove the Cybrovate Agent package:

```bash
sudo zypper remove cybrovate-client-agent
```

### Expected Output

```text
Removing: cybrovate-client-agent
```

---

## Verify Uninstallation

Verify that the package has been removed:

```bash
rpm -qa | grep cybrovate
```

No Cybrovate package entries should be displayed.

---

## Troubleshooting

### Installation Failed

Refresh repositories and retry:

```bash
sudo zypper refresh
```

Then reinstall the package:

```bash
sudo SECRET=xxxx-xxxx-xxxx-xxxxx zypper install --allow-unsigned-rpm ./cyb_datacenter_agent_suse_v<version>.rpm
```

---

### Service Not Running

Start the service manually:

```bash
sudo systemctl start cybrovateremoteclientagent
```

Check status:

```bash
systemctl status cybrovateremoteclientagent
```

---

### View Agent Logs

```bash
sudo journalctl -u cybrovateremoteclientagent -f
```

---

## Download Agent

[⬇ Download SUSE Agent](/downloads/cyb_datacenter_agent_suse_v<version>.rpm)