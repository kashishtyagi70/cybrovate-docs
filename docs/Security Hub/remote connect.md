# Remote Connect

## Overview Guide

The **Remote Connect** module allows administrators and security teams to securely access managed machines directly from the Cybrovate portal. It provides real-time terminal connectivity to servers, endpoints, and virtual machines without requiring external remote access tools.

---

## Purpose of Remote Connect

Remote Connect enables authorized users to:

- Access managed systems remotely through a secure terminal.
- Troubleshoot servers and endpoints in real time.
- Perform administrative and maintenance tasks.
- Investigate security incidents and conduct forensic analysis.
- Manage systems without requiring third-party remote access software.

---

## Machine List Panel

The **Machine List** displays all registered systems available for remote access. Each machine represents a managed endpoint, workstation, server, or virtual machine monitored by the platform.

| Component | Description | Operational Use |
|------------|------------|------------|
| Machine Name | Unique hostname or device identifier. | Select the system you want to connect to. |
| Search | Search function to quickly locate machines. | Used in large environments with many endpoints. |
| Scroll Panel | Displays the complete machine inventory. | Browse available systems. |

### How to Use

1. Locate the target machine from the machine list.
2. Use the search bar to find a specific system.
3. Select the desired machine.
4. Click **Connect Terminal** to start a remote session.

---

## Remote Terminal Window

The **Remote Terminal Window** provides a secure command-line interface to the selected machine. Administrators can execute commands, perform diagnostics, and manage system configurations remotely.

| Component | Description | Operational Use |
|------------|------------|------------|
| Terminal Console | Command-line interface. | Run system commands remotely. |
| Session Status | Displays connection status. | Confirms whether the session is active. |
| Connect Terminal Button | Initiates remote session. | Starts secure remote access. |

> **Security Note:** All remote sessions should be logged and monitored for audit and compliance purposes.

---

## Last Refreshed Time

The **Last Refreshed Time** displays the most recent synchronization timestamp for machine availability and connection status.

This ensures administrators are working with the latest system state and current endpoint information.

---

## Common Use Cases

### 1. Remote Troubleshooting

Diagnose and resolve issues on servers and endpoints without physical access.

### 2. Incident Response

Access affected systems during security investigations and forensic analysis.

### 3. System Maintenance

Perform administrative tasks, configuration changes, and software updates.

### 4. Patch Validation

Verify security patches and remediation activities across managed systems.

---

## Best Practices

### Access Control

- Restrict remote access to authorized administrators only.
- Apply role-based access control (RBAC).
- Regularly review user permissions.

### Session Security

- Enable session logging for audit compliance.
- Monitor remote sessions for suspicious activity.
- Use secure authentication methods.

### Operational Security

- Disconnect sessions after completing maintenance tasks.
- Avoid sharing privileged credentials.
- Follow organizational security policies.

---

## Security Recommendations

> Remote access provides powerful administrative control over managed systems. Ensure all access is authorized, monitored, and logged to maintain compliance and reduce security risk.

---

## Related Features

- Endpoint Management
- Asset Inventory
- Incident Response
- Threat Investigation
- Audit Logging
- Role-Based Access Control (RBAC)