# Installing Agent on macOS

## Agent Installation Guide

Choose your preferred macOS agent package.

---

# Installing Cybrovate Agent on macOS

Silent installation using the command-line interface.

## 1. Copy Package to Installation Directory

Download and place the installer package in the current directory:

```text
cyb-prod_datacenter_agent_mac_v<version>.pkg
```

> **Note:** All commands below must be executed from the same directory where the `.pkg` file is downloaded.

---

## 2. Configure Secret

Create the secret file required by the agent.

```bash
sudo sh -c 'echo "xxxx-xxxx-xxxx-xxxxx" > /private/var/tmp/cybrovate_secret && chmod 600 /private/var/tmp/cybrovate_secret'
```

---

## 3. Install the Agent

Run the installer package:

```bash
sudo installer -pkg cyb-prod_datacenter_agent_mac_v<version>.pkg -target /
```

### Expected Output

```text
installer: Package name is Cybrovate Client Agent
installer: Installing at base path /
installer: The install was successful.
```

---

## 4. Start CYB Agent Services

Start or restart the Cybrovate service:

```bash
sudo launchctl kickstart -k system/com.cybrovate.clientagent
```

---

## 5. Verify Agent Status

Check whether the Cybrovate agent process is running:

```bash
ps aux | grep -i cybrovate
```

### Example Output

```text
root      1234   0.0  0.1  CybrovateClientAgent
```

---

## 6. Uninstall the Agent

### Stop CYB Agent Services

```bash
sudo launchctl bootout system/com.cybrovate.clientagent
```

### Navigate to Installation Directory

```bash
cd /Applications/CybrovateClientAgent
```

### Grant Execute Permission

```bash
chmod +x CybrovateUninstaller
```

### Run the Uninstaller

```bash
./CybrovateUninstaller
```

---

## Verify Uninstallation

Confirm that the agent process is no longer running:

```bash
ps aux | grep -i cybrovate
```

No active Cybrovate agent processes should be displayed.

---

## Troubleshooting

### Installation Failed

- Verify that the package file is not corrupted.
- Ensure the secret file has been created successfully.
- Confirm you are running commands with `sudo` privileges.

### Agent Service Not Running

Restart the service:

```bash
sudo launchctl kickstart -k system/com.cybrovate.clientagent
```

Then verify the status:

```bash
ps aux | grep -i cybrovate
```

### Permission Errors

Ensure the secret file permissions are set correctly:

```bash
ls -l /private/var/tmp/cybrovate_secret
```

Expected permissions:

```text
-rw-------  root  wheel
```

---

## Download Agent

[⬇ Download macOS Agent](/downloads/cyb-prod_datacenter_agent_mac_v<version>.pkg)