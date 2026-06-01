# Security Detection Guide

## Overview

The **Security Detection** module is the operational heart of your Cybrovate portal. It aggregates threat signals, alerts, and compliance events from across your environment into a unified detection workflow, enabling security teams to triage, investigate, and respond to threats efficiently.

---

## Table of Contents

- [What is Security Detection?](#what-is-security-detection)
- [Detection Hub Navigation](#detection-hub-navigation)
- [Overview](#overview-tab)
- [Ticket Insight](#ticket-insight)
- [Priority & Severity Levels](#priority--severity-levels)
- [Actions, Filters & Controls](#actions-filters--controls)
- [Detection Sources & Data Feeds](#detection-sources--data-feeds)
- [Investigation Workflow](#investigation-workflow)
- [Detection Metrics](#detection-metrics)
- [Common Scenarios](#common-scenarios)
- [Best Practices](#best-practices)

---

# What is Security Detection?

Security Detection in Cybrovate is the continuous process of identifying, correlating, and surfacing potential threats and compliance failures across your entire managed environment.

Cybrovate collects information from:

- EDR Agents
- SIEM Log Sources
- Vulnerability Scanners
- Compliance Engines
- Threat Intelligence Feeds
- Cloud Security Platforms

The platform transforms raw events into actionable tickets and alerts.

---

## Key Capabilities

### Unified Visibility

Consolidates threat signals from:

- Endpoints
- Servers
- Cloud Assets
- Network Devices
- Identity Systems

into a single operational view.

### Real-Time Alerting

Detections are generated as events occur.

Examples include:

- Suspicious process execution
- Failed login attacks
- Malware activity
- Vulnerability findings
- Policy violations

### Prioritized Triage

Detections are automatically assigned a severity level:

- Critical
- High
- Medium
- Low

based on risk context and business impact.

> Security Detection sits between data collection and incident response, helping analysts focus on actionable threats.

---

# Detection Hub Navigation

The Detection Hub is organized into the following sections:

| Tab | Purpose |
|------|----------|
| Overview | Security posture summary |
| Ticket Insight | Detection ticket management |
| Alerts | Real-time alert feed |
| Incidents | Escalated investigations |
| Threat Intelligence | IOC enrichment |
| Reports | Security reporting |

---

# Overview Tab

The Overview tab provides a high-level summary of security activity.

Displayed metrics include:

- Total Tickets
- Open Tickets
- Closed Tickets
- Severity Distribution
- Detection Trends
- Analyst Activity

Use this page at the beginning of each shift to assess overall security posture.

---

# Ticket Insight

Ticket Insight is the operational workspace for security analysts.

Every security detection becomes a structured ticket.

### Summary Metrics

| Metric | Description |
|----------|------------|
| Total Tickets | Total number of active tickets |
| Open | Awaiting analyst action |
| In Progress | Under active investigation |
| Closed | Investigation completed |

---

## Ticket Fields

| Field | Description | Operational Use |
|---------|-------------|-----------------|
| S. No. | Sequential row number | Quick reference |
| Ticket Number | Unique identifier | Cross-system tracking |
| Title | Detection description | Pattern recognition |
| Status | Open, In Progress, Closed | Workflow tracking |
| Assigned To | Responsible analyst | Ownership |
| Priority | Severity level | Response urgency |
| Created At | Detection timestamp | SLA tracking |
| Ticket Age | Time since creation | Queue management |
| Client ID | Tenant identifier | Multi-tenant operations |

---

## Ticket Lifecycle

### 1. Open

Detection is created and awaiting assignment.

### 2. Assigned

Analyst accepts ownership.

### 3. In Progress

Investigation and remediation begin.

### 4. Closed

Resolution documented and ticket completed.

> Avoid large backlogs of Open tickets. Monitor ticket age daily.

---

# Priority & Severity Levels

| Severity | Description | SLA |
|------------|------------|------|
| Critical | Active compromise or breach | ≤ 1 Hour |
| High | Significant security threat | ≤ 4 Hours |
| Medium | Suspicious activity | ≤ 24 Hours |
| Low | Informational or low-risk event | ≤ 7 Days |

---

## Critical

Examples:

- Ransomware
- Credential Dumping
- Domain Controller Compromise

Required Action:

- Immediate containment
- Incident escalation
- Management notification

---

## High

Examples:

- Malware Detection
- Privilege Escalation
- Data Exfiltration Indicators

Required Action:

- Immediate triage
- Asset isolation if required

---

## Medium

Examples:

- Failed MFA Attempts
- Unusual Login Activity
- Compliance Violations

Required Action:

- Investigation and remediation

---

## Low

Examples:

- Software Inventory Changes
- Informational IOC Matches

Required Action:

- Document and review

---

# Actions, Filters & Controls

## Actions Menu

Supports:

- Bulk Assignment
- Bulk Status Changes
- Priority Updates
- CSV Export
- Remediation Workflows

---

## Select Account

Filters detections by:

- Client
- Business Unit
- Tenant

Useful in multi-tenant environments.

---

## Filters

Filter by:

- Severity
- Status
- Assignee
- Date Range
- Asset Group
- Detection Rule

---

## Refresh

Forces immediate synchronization with backend services.

---

## Checkbox Selection

Allows bulk operations across multiple tickets.

---

# Detection Sources & Data Feeds

| Source | Detection Type | Reliability |
|----------|----------------|------------|
| EDR Agent | Endpoint activity | High |
| SIEM | Log correlation | Medium-High |
| Vulnerability Scanner | CVE findings | High |
| Compliance Engine | Policy violations | High |
| Threat Intelligence | IOC matches | Medium |
| Cloud CSPM | Cloud posture findings | Medium-High |

---

# Investigation Workflow

## Step 1 – Read Ticket Summary

Review:

- Detection Source
- Affected Asset
- Severity
- Detection Rule

---

## Step 2 – Assess Asset Criticality

Determine business impact of the affected system.

---

## Step 3 – Enrich with Threat Intelligence

Review:

- IOC Matches
- Threat Actor Information
- MITRE ATT&CK Mapping

---

## Step 4 – Review Evidence

Analyze:

- Process Trees
- Log Events
- Network Activity
- CVE Details

---

## Step 5 – Determine Classification

Choose:

- True Positive
- False Positive
- Informational

---

## Step 6 – Contain & Remediate

Actions may include:

- Endpoint Isolation
- Credential Reset
- IOC Blocking
- Malware Removal

---

## Step 7 – Document Resolution

Include:

- Findings
- Root Cause
- Remediation
- Lessons Learned

---

# Detection Metrics

## Mean Time to Detect (MTTD)

Average time from threat occurrence to detection.

Target:

```text
< 1 Hour
```

---

## Mean Time to Respond (MTTR)

Average time until analyst begins investigation.

Targets:

| Severity | Target |
|------------|--------|
| Critical | < 1 Hour |
| High | < 4 Hours |
| Medium | < 24 Hours |

---

## Mean Time to Close (MTTC)

Measures total resolution time.

---

## False Positive Rate (FPR)

Tracks percentage of detections closed as false positives.

Recommended:

```text
< 20%
```

---

## Detection Coverage

Measures MITRE ATT&CK coverage across detection rules.

Target:

```text
70%+
```

---

# Common Scenarios

## Scenario 1 – Sudden Ticket Spike

Actions:

1. Group by title.
2. Identify common rule.
3. Validate whether attack or false positive.
4. Tune rule if necessary.

---

## Scenario 2 – Critical Ticket Aging

Actions:

1. Assign immediately.
2. Escalate to SOC leadership.
3. Review SLA process.

---

## Scenario 3 – Repeated Alerts from One Asset

Possible causes:

- Persistent compromise
- False-positive loop

Perform deeper investigation.

---

## Scenario 4 – New Analyst Onboarding

Recommendations:

- Start with Medium severity tickets.
- Assign mentor.
- Review closure notes.

---

# Best Practices

- Review Open tickets daily.
- Monitor SLA compliance.
- Tune noisy detection rules.
- Maintain detailed closure notes.
- Track MTTD and MTTR weekly.
- Review false-positive rates monthly.
- Maintain MITRE ATT&CK coverage visibility.

---

# Related Documentation

- Endpoint Compliance Guide
- SIEM Configuration Guide
- Incident Response Playbooks
- Threat Intelligence Guide
- Detection Exclusion Guide
- Asset Inventory Guide