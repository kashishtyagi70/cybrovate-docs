# Azure Onboarding

This guide explains how to complete the Azure onboarding bootstrap process for Cybrovate.

---

# Overview

The onboarding bootstrap script creates temporary Microsoft Entra and Azure resources required for secure onboarding.

The script performs:

- Application creation
- Service Principal creation
- Subscription Owner assignment
- Entra ID administrative role assignments

---

# Customer Actions

## Step 1 — Extract Package

Extract:

```text
azure-onboarding-client-bootstrap
```

to a local working folder.

Example:

```text
C:\Temp\azure-onboarding-client-bootstrap
```

---

## Step 2 — Open PowerShell

Open:

```text
Windows PowerShell
```

or:

```text
PowerShell 7
```

Run as:

```text
Administrator
```

---

## Step 3 — Navigate to Scripts Folder

Run:

```powershell
Set-Location C:\Temp\azure-onboarding-client-bootstrap\scripts
```

---

## Step 4 — Prepare Wrapper File

Run:

```powershell
Copy-Item .\Run-Interactive.ps1.example .\Run-Interactive.ps1
```

This creates a working onboarding script configuration file.

---

## Step 5 — Edit Script Values

Open:

```text
Run-Interactive.ps1
```

Update the following values:

| Parameter | Required |
|---|---|
| TenantId | ✅ |
| SubscriptionId | ✅ |
| BootstrapDisplayName | Optional |
| OutputFile | Optional |

---

## Step 6 — Run Bootstrap Script

Run the onboarding PowerShell script using the updated parameters.

Example:

```powershell
.\Run-Interactive.ps1
```

---

## Step 7 — Interactive Sign-In

A Microsoft authentication popup window appears.

Complete the sign-in process using the appropriate Azure account.

---

## Step 8 — Resources Created

The script automatically creates:

- Microsoft Entra Application
- Service Principal
- Subscription Owner Assignment
- Application Administrator Role
- Security Administrator Role

These resources are required temporarily during onboarding.

---

## Step 9 — Review Output File

Verify the output file was created successfully.

Example:

```text
client-bootstrap-output.json
```

Confirm the file exists in the configured output path.

---

## Step 10 — Secure Handoff to Cybrovate

Securely send:

```text
client-bootstrap-output.json
```

to Cybrovate for onboarding completion.

---

# Verification Checklist

| Check | Status |
|---|---|
| Package Extracted | ✅ |
| PowerShell Opened as Administrator | ✅ |
| Script Updated | ✅ |
| Bootstrap Script Executed | ✅ |
| Authentication Completed | ✅ |
| Output JSON Generated | ✅ |

---

# Troubleshooting

## PowerShell Execution Policy Error

Run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope Process
```

---

## Authentication Popup Not Appearing

Ensure:
- Browser popups are allowed
- Microsoft authentication endpoints are accessible

---

## Output File Missing

Verify:
- Script completed successfully
- OutputFile path is valid

---

# Next Step

Continue with endpoint onboarding after Azure onboarding is completed.