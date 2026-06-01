# Scan Host

Scan Host performs comprehensive security scans on individual hosts (servers, workstations) in your environment.

Scans detect:

- Threats
- Vulnerabilities
- Suspicious files
- System misconfigurations
- Compliance issues

Learn how to initiate scans, interpret results across five analysis tabs, and take remediation actions based on scan findings.

---

# Scan Host Metrics

The Scan Host dashboard displays four key metrics at the top.

These KPIs provide an at-a-glance overview of your host scanning program and current threat landscape across managed systems.

| Metric | Value |
|----------|---------|
| Total Hosts | 247 |
| Active Scans | 3 |
| Threats Detected | 18 |
| Last Scan Time | 2 Minutes Ago |

---

## Total Hosts

The total number of devices registered in your scanning program.

This includes:

- Servers
- Workstations
- Laptops
- Managed endpoints

Higher counts indicate broader security coverage.

### Use Cases

- Track security coverage growth
- Monitor onboarding of new assets
- Measure endpoint visibility

---

## Active Scans

The number of hosts currently being scanned.

A value of **3** indicates three hosts are actively running scans.

### Important Notes

- Active scans consume CPU and disk resources.
- Extended periods showing **0 Active Scans** may indicate scheduling issues.
- Verify scan schedules and job status if no scans are running.

---

## Threats Detected

The total number of threats and suspicious findings discovered across all hosts.

Examples include:

- Malware
- Suspicious files
- Risky configurations
- Unauthorized software

### Investigation Guidance

Each threat should be reviewed to determine whether it should be:

- Quarantined
- Removed
- Monitored
- Whitelisted

---

## Last Scan Time

Displays the most recent successful scan completion time.

Example:

> 2 minutes ago

This helps determine the freshness of scan data.

### Best Practice

Maintain a regular scan schedule:

- Daily scans for critical systems
- Weekly scans for standard endpoints

Older scan data may miss recent compromises.

---

# Scan Scheduling

Configure automated schedules to ensure consistent host coverage.

### Recommended Schedule

| Host Type | Scan Frequency |
|------------|----------------|
| Critical Servers | Daily Full Scan |
| Workstations | Weekly Full Scan |
| All Hosts | Daily Quick Scan |

### Scheduling Recommendations

- Run scans during low-usage periods.
- Prefer nights and weekends.
- Balance scan coverage against performance impact.

---

# Scan Actions: Quick vs Deep

Two scan modes are available:

1. Quick Scan
2. Deep Scan

Choose based on urgency and performance requirements.

---

## Quick Scan Mode

### Characteristics

| Feature | Details |
|----------|---------|
| Duration | 5–15 Minutes |
| Coverage | Critical files, processes, system areas |
| CPU Impact | Low |
| Frequency | Daily |

### Use Cases

- Daily monitoring
- Routine threat detection
- Baseline security checks

### Advantages

- Fast execution
- Minimal user disruption
- Suitable during business hours

---

## Deep Scan Mode

### Characteristics

| Feature | Details |
|----------|---------|
| Duration | 1–4 Hours |
| Coverage | Full filesystem, memory, registry, archives |
| CPU Impact | High |
| Frequency | Weekly or Monthly |

### Use Cases

- Incident response
- Compliance audits
- New host baselines
- Compromise investigations

### Advantages

- Comprehensive analysis
- Improved malware discovery
- Full system visibility

---

## When to Choose Which Scan

Use **Quick Scans** when:

- Performing daily monitoring
- Checking host health
- Running scheduled scans

Use **Deep Scans** when:

1. Threats were found during a Quick Scan.
2. A host is suspected compromised.
3. Compliance audits require evidence.
4. Security incidents occurred.
5. Quarterly baseline validation is required.

---

# Scan Results Tabs

Scan results are organized into five tabs.

Each tab focuses on a different category of findings.

---

# 1. Overview Tab

## Purpose

Provides a high-level summary of scan results across all hosts.

### Overview Table Columns

| Column | Description |
|----------|-------------|
| Host Name | Device hostname |
| IP Address | Host network address |
| Scan Status | Scan progress state |
| Risk Level | Overall host risk |
| Last Scan | Latest scan timestamp |
| Threats | Number of findings |

---

## Scan Status Values

- Completed
- Scanning
- Pending
- Failed

### Usage

- Verify scan completion
- Identify failed jobs
- Monitor scan progress

---

## Risk Levels

| Risk Level | Meaning |
|------------|----------|
| Low | Healthy system |
| Medium | Requires review |
| High | Immediate remediation needed |
| Critical | Urgent investigation required |

---

## Use Overview To

- Monitor overall host health
- Prioritize remediation
- Verify scan completion
- Identify high-risk systems

---

# 2. System Drift Tab

## Purpose

Displays configuration drift and unauthorized system modifications.

Examples include:

- Registry modifications
- Driver replacements
- System file changes
- Configuration changes

---

## Information Displayed

### Change Type

Examples:

- File Modified
- Registry Key Changed
- Driver Replaced
- System File Altered

### Timestamp

Shows when the change occurred.

### Severity

Indicates risk level associated with the change.

---

## Use System Drift To

- Detect unauthorized modifications
- Identify persistence mechanisms
- Discover suspicious driver installations
- Track baseline deviations

---

# 3. Suspicious Files Tab

## Purpose

Displays files flagged as suspicious or malicious.

This is the primary malware investigation tab.

---

## Information Displayed

### File Name

Location of the detected file.

Example:

```text
C:\Temp\malware.exe
```

### Threat Name

Example:

- Trojan.Win32.Generic
- PUA.Adware.Cutter

### Detection Method

- Signature-Based
- Heuristic Analysis
- Sandboxing

### Risk Level

- Critical
- High
- Medium
- Low

### Available Actions

- Quarantine
- Remove
- Monitor
- Whitelist

---

## Use Suspicious Files To

- Identify malware infections
- Investigate trojans and backdoors
- Detect potentially unwanted applications (PUAs)
- Quarantine threats before execution

---

# 4. Exclusions Tab

## Purpose

Displays files, folders, processes, or extensions excluded from scanning.

Exclusions reduce scan overhead but also reduce visibility.

---

## Information Displayed

### Exclusion Type

Examples:

- File
- Folder
- Extension
- Process
- Hash

### Pattern

Example:

```text
C:\Program Files\*
*.log
```

### Reason

Examples:

- Performance optimization
- False positive prevention
- Trusted software

### Added By

Displays the user who created the exclusion.

---

## Use Exclusions To

- Reduce false positives
- Improve scan performance
- Audit exclusion policies
- Validate approval processes

### Security Warning

Never exclude:

- Critical system files
- Windows system directories
- Security applications

---

# 5. Reports Tab

## Purpose

Provides exportable reports for security reviews and compliance audits.

---

## Available Report Types

### Executive Summary

High-level overview for leadership.

### Detailed Scan Report

Complete technical findings.

### Threat Report

Focused malware analysis.

### Compliance Report

Audit-ready documentation.

---

## Statistics Included

- Files scanned
- Threats detected
- Threats removed
- Scan duration
- Performance metrics

---

## Export Formats

- PDF
- HTML
- CSV

---

## Use Reports To

- Support compliance audits
- Track threat trends
- Share findings with stakeholders
- Document incidents

---

# Overview Table: Host Status Details

The Overview tab serves as the primary interface for monitoring host health.

---

## Overview Table Columns

| Column | What It Shows | Investigation Use |
|----------|-------------|------------------|
| Host Name | Device hostname | Drill into scan results |
| IP Address | Device IP | Correlate network activity |
| Scan Status | Scan state | Verify completion |
| Risk Level | Overall security posture | Prioritize remediation |
| Last Scan | Scan timestamp | Validate freshness |
| Threats | Threat count | Identify affected systems |

---

# Host Review Workflow

## 1. Sort by Risk Level

Review Critical and High-risk hosts first.

---

## 2. Check Scan Status

Ensure all scans completed successfully.

Investigate:

- Failed scans
- Stuck scans
- Long-running scans

---

## 3. Review Threat Counts

Identify systems with the highest number of threats.

Investigate findings within the Suspicious Files tab.

---

## 4. Verify Last Scan Time

Confirm all systems were scanned recently.

Recommended:

> No host should exceed 24 hours without a scan.

---

# Daily Overview Review Checklist

Each morning:

- Check for Critical and High-risk hosts.
- Review failed scans.
- Verify threat trends.
- Confirm scan freshness.
- Investigate newly discovered threats.

This review should take approximately 10 minutes.

---

# Effective Scan Host Operations

Establish a consistent scanning program.

### Recommended Strategy

- Daily Quick Scans on all hosts.
- Weekly Deep Scans on critical servers.
- Monthly Deep Scans on workstations.
- Daily Overview reviews.

### Operational Goals

- Detect threats early.
- Maintain scan coverage.
- Reduce remediation time.
- Improve compliance posture.

---

# Continuous Host Scanning Reduces Compromise Risk

Scan Host serves as a frontline defense against:

- Malware
- Misconfigurations
- Unauthorized changes
- Compliance violations

The five tabs provide different perspectives on host security:

| Tab | Primary Purpose |
|-------|----------------|
| Overview | Host triage and monitoring |
| System Drift | Unauthorized changes |
| Suspicious Files | Malware investigation |
| Exclusions | False-positive management |
| Reports | Compliance and auditing |

Use each tab according to its intended purpose to maximize visibility and reduce compromise risk.

For assistance with host scanning, threat remediation, or scan configuration, contact the Cybrovate Help & Support team.