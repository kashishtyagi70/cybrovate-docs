# Kubernetes Dashboard – Overview Guide

## Purpose of Kubernetes Dashboard

The Kubernetes Dashboard provides centralized visibility into containerized workloads, runtime security posture, image vulnerability exposure, and namespace activity across your Kubernetes clusters.

It helps DevOps, Security, and Platform Engineering teams monitor cluster health, identify risks, and prioritize remediation actions.

---

# Cluster Metrics Overview

## 42 Pods

Total number of running container workloads across the Kubernetes cluster.

A sudden increase or decrease in pod count may indicate scaling events or operational issues.

---

## 9 Images Assessed

Number of container images scanned for vulnerabilities.

This indicates coverage of container security scanning across deployed workloads.

---

## 1,105 Vulnerabilities

Total number of detected vulnerabilities across container images.

This includes known CVEs identified during image scanning.

---

## 6,432 Runtime Detections

Total number of runtime security events detected within containers.

These may include:

- Suspicious processes
- Unauthorized access attempts
- Abnormal network activity

> **Operational Insight:**  
> High runtime detections combined with critical vulnerabilities may indicate active exploitation attempts or insecure workloads requiring immediate remediation.

---

# Image Assessment by Severity

This chart displays vulnerability severity distribution across scanned container images.

| Severity | Description | Recommended Action |
|-----------|-------------|-------------------|
| Critical | High-risk vulnerabilities that may allow remote code execution or system compromise. | Patch immediately or redeploy a secure image. |
| High | Significant vulnerabilities with potential security impact. | Schedule remediation within defined SLA. |
| Medium | Moderate security issues with limited exploitability. | Include in regular patch cycles. |
| Low | Minor security issues. | Monitor and address during maintenance windows. |

---

# Runtime Detections by Severity

This chart shows real-time security event distribution based on severity levels.

It helps security teams prioritize investigation and incident response actions.

> **Security Note:**  
> A spike in critical runtime detections may indicate malware activity, container breakout attempts, or unauthorized privilege escalation.

---

# Top 15 Pods Used by Count

This visualization highlights the most frequently used or resource-intensive pods in the cluster.

These workloads typically handle production traffic or critical services.

| Pod Type | Example | Operational Use |
|-----------|----------|----------------|
| Application Pod | api-gateway-prod | Handles client API requests. |
| Database Pod | mongodb-primary | Stores application data. |
| Cache Pod | redis-cache | Improves application performance. |
| Ingress Controller | nginx-ingress | Routes external traffic into the cluster. |

---

# Top 15 Namespaces by Count

This chart displays the distribution of workloads across Kubernetes namespaces.

Namespaces logically separate environments such as production, staging, and development.

| Namespace | Purpose | Security Consideration |
|------------|---------|------------------------|
| production | Hosts live application workloads. | Requires strict security monitoring. |
| staging | Testing environment before production deployment. | Monitor for configuration drift. |
| development | Developer testing environment. | Apply least privilege access controls. |
| monitoring | Observability and logging tools. | Ensure log integrity and availability. |

---

# Last Refreshed Time Indicator

Displays the most recent data synchronization timestamp for Kubernetes telemetry.

This ensures administrators and security teams are working with up-to-date cluster information.

---

# Common Use Cases

- Monitor Kubernetes cluster health and workload distribution.
- Identify vulnerable container images before deployment.
- Detect runtime security incidents in containers.
- Analyze resource usage across namespaces and pods.

---

# Best Practices

## Image Scanning

Regularly scan container images for vulnerabilities.

### Recommendations

- Integrate image scanning into CI/CD pipelines.
- Scan images before deployment.
- Continuously monitor for newly disclosed vulnerabilities.

---

## Runtime Monitoring

Monitor runtime detections for abnormal behavior.

### Recommendations

- Investigate unusual process activity.
- Monitor network communications.
- Enable real-time alerting for critical detections.

---

## Access Control

Restrict access using Role-Based Access Control (RBAC).

### Recommendations

- Apply least-privilege principles.
- Regularly review user permissions.
- Limit administrative access.

---

## Namespace Separation

Maintain separate namespaces for production and testing environments.

### Recommendations

- Isolate workloads by environment.
- Apply namespace-specific security policies.
- Restrict cross-namespace communication where appropriate.

---

## Automated Patching

Apply automated patching and redeployment workflows.

### Recommendations

- Automate vulnerability remediation.
- Use trusted base images.
- Continuously validate deployment integrity.

---

# Support

For assistance with Kubernetes monitoring or cluster security configuration, contact the Cybrovate Help & Support team.