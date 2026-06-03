# AWS Onboarding

This guide explains how to onboard an AWS account with Cybrovate.

---

# Overview

During onboarding, an IAM Role is created in the customer AWS account.

This role is used temporarily to provision required onboarding resources securely.

---

# Customer Actions

## Step 1 — Login to AWS Console

Open the AWS Console.

Navigate to:

```text
IAM → Roles → Create Role
```
![Medium screenshot](/media/images/aws/aws-step-1.png){.media-md}

---

## Step 2 — Choose Custom Trust Policy

Select:

```text
Custom Trust Policy
```
![Medium screenshot](/media/images/aws/aws-step-2.png){.media-md}
---

## Step 3 — Paste Trust Policy JSON

Paste the following JSON configuration:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "CLIENT_ID"
        }
      }
    }
  ]
}
```
![Medium screenshot](/media/images/aws/aws-step-3.png){.media-md}
---

## Step 4 — Paste Permission Policy JSON

Paste the required permission policy JSON provided by Cybrovate.

```text
Paste the onboarding permission policy here.
```
![Medium screenshot](/media/images/aws/aws-step-4.png){.media-md}
---

## Step 5 — Enter Role Name

Use the following role name:

```text
Cybrovate-BootstrapProvisioningRole
```

Review all configurations before continuing.

![Medium screenshot](/media/images/aws/aws-step-5.png){.media-md}
---

## Step 6 — Copy Role ARN

After role creation, copy the generated Role ARN.

Example:

```text
arn:aws:iam::123456788012:role/Cybrovate-BootstrapProvisioningRole
```
![Medium screenshot](/media/images/aws/aws-step-6.png){.media-md}
---

## Step 7 — Click Create Role

Click:

```text
Create Role
```

The role will now be available for onboarding integration.
![Medium screenshot](/media/images/aws/aws-step-7.png){.media-md}
---

# Important Notes

- This role is used only during onboarding.
- Do not modify the trust relationship unless instructed.
- Ensure the External ID matches the provided client ID.

---

# Verification

Verify the following:

| Check | Status |
|---|---|
| IAM Role Created | ✅ |
| Trust Policy Added | ✅ |
| Permission Policy Added | ✅ |
| Role ARN Copied | ✅ |

---

# Troubleshooting

## Invalid Principal Error

Ensure the AWS account ID is correct.

---

## External ID Mismatch

Verify the provided `CLIENT_ID`.

---

# Next Step

Continue with endpoint onboarding after AWS onboarding is completed.