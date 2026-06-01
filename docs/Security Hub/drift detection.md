# Drift Detection

Drift Detections identifies unauthorized, undocumented, or unexpected configuration changes across your infrastructure. When systems diverge from their baseline configuration (installation of unauthorized software, network policy changes, hardware modifications, user account additions), Drift Detections captures these changes.

Learn how to review drift events, understand change impact, and acknowledge approved modifications.

---

# Understanding Drift Detection

Configuration drift occurs when systems deviate from their documented, approved state.

This can happen through:

- Intentional changes (upgrades, patches)
- Accidental modifications (misconfigured settings)
- Malicious activity (unauthorized software installation, privilege escalation)

Drift Detections monitors these changes and flags them for review and approval.

## Expected Changes (Normal Drift)

- Security patches applied by maintenance teams
- Software upgrades rolled out via deployment automation
- Hardware replacements (RAM or disk upgrades)
- Policy updates applied by system administrators
- Approved application installations

## Suspicious Changes (Security Risk)

- Unknown software suddenly installed
- Unauthorized user accounts created
- Firewall rules disabled or modified unexpectedly
- Registry or system files modified outside change windows
- Privilege escalations not requested through proper channels

> **Drift Detection Goal**
>
> Distinguish between authorized changes (which should be acknowledged) and unauthorized changes (which require investigation and potential rollback).
>
> Regular drift reviews maintain infrastructure consistency and prevent configuration creep that can degrade security and stability.

---

# Drift Metrics Overview

The Drift Detections dashboard displays three key metrics at the top. These KPIs provide a quick snapshot of drift status and pending actions.

| Metric | Value |
|----------|---------|
| Total Changes | 10 |
| Last 7 Days Changes | 0 |
| Pending Acknowledgment | 7 |

---

## Total Changes

The cumulative count of all configuration changes detected since drift monitoring began.

Includes:

- Acknowledged changes
- Pending changes

High totals may indicate:

- Active infrastructure
- Frequent updates
- High-change environments

---

## Last 7 Days Changes

Changes detected during the previous seven days.

A count of **0** indicates no recent configuration changes.

A spike may indicate:

- Deployment activity
- Patch windows
- Unauthorized modifications

Always compare activity against maintenance schedules.

---

## Pending Acknowledgment

Changes awaiting review and approval.

Each pending change requires one of the following actions:

- Approve and acknowledge
- Investigate
- Roll back if unauthorized

High pending counts may indicate:

- Review backlog
- Large infrastructure changes
- Security concerns

### Managing Pending Changes

Recommended review process:

- Review pending changes daily.
- Expected pending count during deployment periods: **5–15**
- Escalate when pending changes exceed **20**
- Investigate before acknowledging

---

# Drift Categories

Detected drift is categorized by change type.

Understanding categories helps prioritize review and approval.

---

## Application Changes

New software installations, upgrades, or removals.

### Examples

- New software installation
- Application upgrade

### Considerations

- Require IT or development team approval.
- Higher risk if installed by unauthorized users.

---

## Network Changes

Firewall policy modifications and network configuration updates.

### Examples

- Firewall policy tightened
- Restricted ports enabled

### Considerations

- Can impact connectivity.
- Coordinate with network teams.
- Unauthorized changes may indicate compromise.

---

## Hardware Changes

Physical upgrades or resource modifications.

### Examples

- RAM upgrade
- Storage upgrade
- CPU modification

### Considerations

- Usually maintenance related.
- Verify against asset inventory records.

---

## System Updates

Operating system and security updates.

### Examples

- Security patch installation
- Driver update
- OS upgrade

### Considerations

- Typically expected.
- Verify alignment with patch schedules.

---

## User Management

User account creation, deletion, or permission changes.

### Examples

- User account creation
- User deletion
- Permission updates

### Considerations

- High security sensitivity.
- Verify requests through approved channels.

---

## Privilege Changes

Administrative access or privilege elevation.

### Examples

- Administrator assignment
- Privilege escalation

### Considerations

- Critical security category.
- Requires explicit approval and documentation.

---

## High-Risk Categories

Treat these as priority investigations:

- User Management
- Privilege Changes

Before acknowledging:

1. Verify HR records.
2. Review security approvals.
3. Check change requests.

If no request exists, escalate immediately.

---

# Drift Changes Table

The Drift Detections table lists all detected configuration changes.

Each row represents a single drift event.

Use the table to:

- Investigate changes
- Assess impact
- Approve modifications
- Escalate suspicious activity

## Table Columns Explained

| Column Name | What It Shows | Investigation Use |
|------------|--------------|-------------------|
| S. No. | Sequential event number | Reference changes during discussions |
| Resource Name | System where change occurred | Identify affected resource |
| Change ID | Unique drift identifier | Correlate with logs and tickets |
| Category | Type of change | Prioritize investigations |
| What Changed | Description of modification | Understand impact |
| Old States | Previous configuration | Review baseline state |
| New States | Current configuration | Verify expected outcome |
| Date | Timestamp of event | Compare against maintenance windows |
| Ack | Approval action | Approve authorized changes |

---

# Drift Review Workflow

## 1. Review Resource and Category

Identify:

- Which system changed
- What category the change belongs to

This provides initial context.

## 2. Understand the Change

Review:

- What Changed
- Old State
- New State

Determine impact and risk.

## 3. Verify Against Change Records

Cross-reference:

- Change requests
- Maintenance schedules
- Deployment records

If no matching record exists, investigate further.

## 4. Acknowledge or Escalate

### Authorized Change

- Acknowledge the event.
- Remove it from the pending queue.

### Suspicious Change

- Escalate for investigation.
- Do not acknowledge until verified.

---

# Acknowledgment Workflow

Only acknowledge changes after confirming they correspond to approved requests or maintenance activities.

Acknowledgment means:

> This change is authorized and requires no further investigation.

Bulk acknowledgment is acceptable after scheduled maintenance windows.

### Example

> Drift #05 acknowledged — Python upgrade completed during approved maintenance window.

---

# Investigating Suspicious Drift

Changes without approvals or maintenance records require investigation.

## Red Flags (Investigate Immediately)

- User account created without HR approval
- Unapproved privilege escalation
- Unknown application installation
- Firewall rules disabled unexpectedly
- Changes outside business hours
- Unplanned network modifications

## Yellow Flags (Verify Before Acknowledging)

- Maintenance activity missing documentation
- Minor patch updates
- Hardware upgrades not yet logged
- Automated patching activity
- Network policy updates similar to existing policies

---

# Investigation Process

## 1. Contact Resource Owner

Ask:

> Did you approve this change?

Provide:

- Resource name
- Change ID
- Timestamp

## 2. Check Change Management Systems

Review:

- Jira
- ServiceNow
- Internal ticketing systems

Search using:

- Change ID
- Date
- Resource name

## 3. Review System Logs

For high-risk events review:

- Windows Event Logs
- Audit logs
- Access control records

Verify authorization.

## 4. Decide Next Action

| Situation | Action |
|------------|---------|
| Authorized | Acknowledge |
| Low-risk but unclear | Continue investigation |
| Unauthorized | Escalate and consider rollback |

---

# Escalation Path

If a change is unauthorized:

**Do not acknowledge it.**

Immediately:

1. Notify Security Operations.
2. Engage Incident Response.
3. Preserve logs and evidence.
4. Determine whether compromise occurred.

This becomes a security incident rather than a routine approval task.

---

# Drift Management Best Practices

## Daily Drift Review

Schedule 15–30 minutes daily to review pending drift events.

Benefits:

- Faster approvals
- Reduced backlog
- Better visibility

## Coordinate with Change Windows

Maintain a visible change calendar.

After maintenance windows:

- Review changes
- Batch acknowledge approved events
- Document approvals

## Establish Approval Workflows

| Category | Approver |
|-----------|-----------|
| Application Changes | DevOps / IT Team |
| User Management | Security Team |
| Privilege Changes | Security + Management |
| Network Changes | Network Team |

## Investigate Anomalies

Watch for patterns such as:

- Multiple users created overnight
- Repeated privilege escalations
- Clusters of unauthorized software

Patterns often indicate compromise or process failures.

## Document Decisions

Maintain audit records explaining approvals.

Example:

> Drift #05 acknowledged as part of approved maintenance window.

## Correlate with Security Events

Review drift alongside:

- Failed logins
- Privilege escalation alerts
- Malware detections
- Endpoint security alerts

Suspicious drift combined with security alerts may indicate compromise.

---

# Baseline Establishment

At project launch:

1. Establish baseline configurations.
2. Document approved software.
3. Define standard system settings.
4. Record expected operating states.

Baselines provide the foundation for effective drift analysis.

---

# Next Steps for Configuration Governance

Establish a daily workflow:

1. Review the Drift Dashboard every morning.
2. Investigate high-risk changes immediately.
3. Acknowledge approved maintenance changes.
4. Configure alerts for:
   - User Management
   - Privilege Changes
   - Critical Applications

Long-term goals:

- Infrastructure as Code (IaC)
- Automated deployments
- Strict change control
- Reduced unauthorized drift

> Every change should be tracked, approved, and documented before reaching production.

---

# Configuration Governance Reduces Risk

Drift Detections provides visibility into what is actually happening across your infrastructure.

Regular reviews help identify:

- Approved operational changes
- Unintended modifications
- Security incidents
- Process failures

Treat drift management as a core security function rather than an administrative task.

For assistance with drift events, configuration governance, or escalation procedures, contact the Cybrovate Help & Support team.