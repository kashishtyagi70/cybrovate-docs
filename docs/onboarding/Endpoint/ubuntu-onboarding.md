# Installing Agent on Ubuntu Machine

## Agent Installation Guide

Choose your preferred Ubuntu agent package.

---

# Installing Agent on Ubuntu Machine

Silent installation using the command-line interface.

## 1. Copy Package to Installation Directory

Download and place the installer package in the `/tmp` directory:

```text
/tmp/cyb-prod_datacenter_agent_ubuntu_v<version>.deb
```

> **Note:** All commands below must be executed from the same directory where the `.deb` package is downloaded.

---

## 2. Open Terminal with Administrator Privileges

Use an account with permission to install software and manage services.

---

## 3. Install the Agent

Run the installer package:

```bash
sudo SECRET=xxxx-xxxx-xxxx-xxxxx dpkg -i cyb-prod_datacenter_agent_ubuntu_v<version>.deb
```

### Expected Output

```text
Selecting previously unselected package cybrovate-datacenter-client-agent.
Preparing to unpack...
Unpacking cybrovate-datacenter-client-agent...
Setting up cybrovate-datacenter-client-agent...
```

---

## 4. Verify Agent Status

Check the status of the Cybrovate Agent service:

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

Remove the installed package:

```bash
sudo SECRET=xxxx-xxxx-xxxx-xxxxx dpkg -P cybrovate-datacenter-client-agent
```

---

## 6. Stop Cybrovate Agent Services

Before uninstalling, stop the service:

```bash
sudo systemctl stop cybrovateclientagent
```

Then remove the package:

```bash
sudo SECRET=xxxx-xxxx-xxxx-xxxxx dpkg -P cybrovate-datacenter-client-agent
```

---

## Verify Uninstallation

Verify that the package has been removed:

```bash
dpkg -l | grep cybrovate
```

No Cybrovate package entries should be displayed.

---

## Troubleshooting

### Installation Failed

Update package dependencies:

```bash
sudo apt update
sudo apt --fix-broken install
```

Then retry the installation.

### Service Not Running

Restart the service:

```bash
sudo systemctl restart cybrovateclientagent
```

Check the status again:

```bash
systemctl status cybrovateclientagent
```

### View Agent Logs

```bash
sudo journalctl -u cybrovateclientagent -f
```

---

## Download Agent

[⬇ Download Ubuntu Agent](/downloads/cyb-prod_datacenter_agent_ubuntu_v<version>.deb)