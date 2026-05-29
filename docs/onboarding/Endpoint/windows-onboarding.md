# Installing Agent on Windows Machine

## Agent Installation Guide

Choose your preferred installation method:

- Installation via CLI (Silent Installation)
- Installation via GUI (Interactive Installation)

---

## Downloads

| Platform | Download |
|-----------|----------|
| Windows | [Download Agent](/downloads/cyb_datacenter_agent_win_v2.2.4.exe) |


# Installation via CLI

Silent installation using the command-line interface.

## 1. Copy Installer to `C:\Temp`

Download and place the installer executable in the following directory:

```text
C:\Temp
```

## 2. Open Command Prompt as Administrator

Right-click **Command Prompt** and select **Run as administrator** to ensure proper permissions.

## 3. Navigate to Installation Directory

Run the following command:

```cmd
cd C:\Temp
```

## 4. Run Installation Command

Execute the installer with the required parameters:

```cmd
.\cyb_datacenter_agent_win_v<version>.exe /INSTALL /SECRET=xxxx-xxxx-xxxx-xxxxx /REGION=INDIA /VERYSILENT /NORESTART
```

### Parameter Description

| Parameter | Description |
|------------|------------|
| `/INSTALL` | Starts the installation process |
| `/SECRET` | Registration secret provided by Cybrovate |
| `/REGION` | Deployment region |
| `/VERYSILENT` | Performs a silent installation without user interaction |
| `/NORESTART` | Prevents automatic system restart |

## 5. Verify Service Status

1. Open **Run** (`Win + R`).
2. Type:

```text
services.msc
```

3. Press **Enter**.
4. Verify that the following service is present and running:

```text
CybrovateClientAgent
```

## 6. Uninstallation Command

To uninstall the agent silently, run:

```cmd
.\cyb_datacenter_agent_win_v<version>.exe /UNINSTALL /SECRET=xxxx-xxxx-xxxx-xxxxx /REGION=INDIA /VERYSILENT /NORESTART
```

---

# Installation via GUI

Interactive setup using the graphical installer wizard.

## 1. Download Installer

Download the Windows installer (`.exe`) from the official distribution portal.

## 2. Launch Installer

Double-click the installer executable to start the installation process.

## 3. Follow the Setup Wizard

1. Click **Next**.
2. Accept the license agreement.
3. Click **Install** to begin the installation.

## 4. Monitor Installation Progress

Wait for the installation wizard to complete all setup tasks and file copying operations.

## 5. Verify Service Status

1. Open **Run** (`Win + R`).
2. Type:

```text
services.msc
```

3. Press **Enter**.
4. Verify that the following service is present and running:

```text
CybrovateClientAgent
```

---

## Installation Progress Example

The installer will display a progress screen similar to the following:

> **Cybrovate Client Agent version 2.2.4 installation progress**

Wait until the installation reaches **100%** and the completion message is displayed.

---

## Troubleshooting

### Installation Failed

- Ensure Command Prompt is running as Administrator.
- Verify that the installation package is not corrupted.
- Confirm that antivirus or endpoint protection is not blocking the installer.

### Service Not Running

- Open `services.msc`.
- Locate **CybrovateClientAgent**.
- Right-click and select **Start**.
- If the service fails to start, review installation logs and contact Cybrovate Support.

### Reinstallation

If the installation becomes corrupted:

1. Run the uninstall command.
2. Reboot the machine if required.
3. Install the latest version using either the CLI or GUI method.
````
