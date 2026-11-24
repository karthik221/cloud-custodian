Yes, but I’d separate **Port’s role in the process** from **the system that owns and deploys AWS permissions**. Port can provide the developer experience and trigger work. For organization-wide provisioning permissions, I’d keep the permission definitions versioned and deploy them through your AWS infrastructure pipeline.

| Choice | Pros | Cons | Fit |
|---|---|---|---|
| **Port’s IAM permission workflow guide** | Fastest way to offer permission requests and revocation in Port; tracks requests in the catalog; supports time-bound grants. | It addresses requesting permissions for AWS resources, which is different from maintaining the cross-account provisioning role for every golden path. Port’s guide uses GitHub Actions and an IAM user with broad IAM operations on `Resource: "*"`, which would need redesign for a production multi-account setup. [Port’s guide](https://docs.port.io/guides/all/iam-permissions-guide/) | Good if developers need temporary access requests. **Not my choice as the policy source of truth for this problem.** |
| **Port actions/workflows with a custom backend** | Keeps the developer experience in Port; you can validate inputs, open a pull request, trigger a workflow, show status, and record the result. Port supports self-service actions backed by your existing workflow systems. [Port self-service actions](https://docs.port.io/workflows/actions-and-automations/create-self-service-experiences/) | You own the backend, security checks, retries, audit trail, and policy lifecycle. Directly changing IAM from a Port action can make policy changes harder to review and reproduce. | Useful as the **front door** to a governed pipeline. |
| **Policy-as-code repository + CI + AWS StackSets** | Makes each golden path’s permissions reviewable, testable, versioned, and traceable. StackSets can target an OU and its child OUs, with automatic deployment to accounts added to the target OU. [AWS StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-associate-stackset-with-org.html) | Requires building and operating the permission manifest format, policy generation, validations, and deployment pipeline. | **Best fit for consistent cross-account role permissions across nested OUs and environments.** |
| **AWS-native controls such as SCPs and permission boundaries** | Useful guardrails: constrain what Port’s role or other principals can do, even when an identity policy grants access. | They don’t grant the actions a golden path needs; you still need identity policies on the role. [AWS Organizations security guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/organizations-security.html) | Use alongside the policy pipeline, not instead of it. |

## Recommendation

Use a **hybrid**:

- Port owns the catalog, golden-path interface, and workflow initiation.
- Each golden path declares its required AWS permissions in a versioned manifest.
- A CI pipeline validates the change and produces a reviewable policy update.
- CloudFormation StackSets deploy the approved role policies to the target OUs and accounts.
- SCPs and permission boundaries enforce organization guardrails.
- Port shows the rollout status and links back to the change record.

That way, onboarding a new service requires a permission change alongside the golden-path change. Port can initiate or track that change, while your AWS deployment pipeline remains the controlled mechanism for applying it. I would reserve Port’s IAM permission workflow pattern for **developer access requests**; it is not, by itself, the OU-wide policy distribution mechanism you need.

==============

Since the Port provisioning role already exists in each target account, the change is **attaching additional permissions to that role as golden paths are onboarded**.

That’s a valid automation pattern, but I’d make **your IAM policy-as-code pipeline the source of truth** and use Port as the trigger and status surface. Port workflows can invoke a backend such as GitHub Actions, but Port’s IAM guide demonstrates creating and revoking temporary roles; it doesn’t document updating a standing cross-account provisioning role across target accounts. [Port IAM permission guide](https://docs.port.io/guides/all/iam-permissions-guide/)

A good flow is:

1. A golden path adds its required permissions in a versioned manifest.
2. CI reviews and validates the policy change.
3. The deployment pipeline attaches the approved policy to the existing Port role in the target accounts, using StackSets or your existing IaC deployment system.
4. Port shows the request and rollout status.

So Port **can handle the workflow around the change**, and a custom Port action could trigger the deployment. I would avoid making Port itself the authoritative place where teams define or directly edit AWS permissions; keep that in reviewed, version-controlled IaC. StackSets support OU targeting, including child OUs when a parent OU is targeted. [AWS StackSets and Organizations](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-associate-stackset-with-org.html)



======================

**Confirmed—with an important distinction:** Port’s IAM permission guide does not provide a built-in, OU-wide mechanism for applying new policies to an existing cross-account provisioning role.

As written, the guide creates a **new IAM role and policy** through GitHub Actions using configured AWS credentials. The workflow calls `create-policy`, `create-role`, and `attach-role-policy`; its trust policy names an AWS account principal so users from that account can assume the temporary role. That’s a different pattern from updating a standing Port provisioning role across target accounts. [Port’s IAM permission workflow guide](https://docs.port.io/guides/all/iam-permissions-guide/)

The guide does use a single configured `AWS_ACCOUNT_ID`, and the sample workflow doesn’t show assuming roles into multiple target accounts or deploying through OUs. So it doesn’t cover your multi-account rollout **out of the box**.

You could customize its GitHub Actions backend to assume a deployment role in each target account and apply policies there. For consistent OU-wide rollout, I’d have Port trigger or track a policy-as-code pipeline and let AWS StackSets distribute the approved changes.

==============




# Evaluating Port's built-in IAM permission management vs. Policy as Code

From a Cloud Governance Engineering perspective, I would approach this as an architecture and governance capability evaluation, rather than simply comparing two ways of creating IAM policies.

The key question is:

Should Port become an additional control plane for managing cloud IAM permissions, or should it complement the existing Policy as Code and CI/CD governance model?

My recommendation would be to experiment with Port, but initially position it as a controlled IAM management and self-service layer—not an immediate replacement for the existing Policy as Code pipeline.

There are several dimensions to evaluate:

1. Security and least-privilege enforcement.
2. Governance, approvals, and separation of duties.
3. Policy lifecycle management and change traceability.
4. Integration with existing IaC and CI/CD workflows.
5. Drift detection and reconciliation.
6. Operational scalability and auditability.
7. Lock-in, portability, and long-term ownership.

Let's break this down in a way you can use in an architecture review, technical discussion, or proof-of-concept proposal.

## 1. Understand the two approaches

First, establish that Port's built-in IAM permission management and Policy as Code solve related but not necessarily identical problems.

### Option A: Port as an IAM management layer

IAM permission management | Port

[docs.port.io](<https://docs.port.io/guides/all/iam-permissions-guide/?utm_source=chatgpt.com>)

Port provides a centralized developer portal and workflow layer. Its IAM permission management capability can be evaluated as a way to manage identity policies associated with cloud IAM roles.

The architectural idea is to let users interact with permissions through a centralized interface and workflow instead of requiring every permission change to go through a manually maintained code pipeline.

Potential capabilities to evaluate include:

- Centralized visibility into IAM role permissions.
- Managing or updating IAM identity policies.
- Standardized permission requests.
- Workflow-driven permission changes.
- Integrating IAM operations into developer self-service.
- Governance through predefined workflows and approval mechanisms.

An important distinction: verify exactly which cloud providers, IAM resource types, policy operations, and workflow controls Port supports in your environment. Do not assume that every AWS IAM capability is covered simply because identity policy management is supported.

### Option B: Traditional Policy as Code

Your CI-CD Pipeline Is Your Real Infrastructure Control Plane - DEV Community

[dev.to](<https://dev.to/ntctech/your-ci-cd-pipeline-is-your-real-infrastructure-control-plane-2c0m?utm_source=chatgpt.com>)

In the traditional model:

- IAM policies are defined in Terraform, CloudFormation, CDK, or another IaC framework.
- Policy definitions are stored in Git.
- Changes go through pull requests.
- Automated checks validate policy compliance.
- Security and governance policies are enforced through tools such as OPA, Checkov, or custom validation.
- Approved changes are deployed through CI/CD.
- Cloud resources are continuously reconciled against declared configuration.

The central principle is that Git and the deployment pipeline are the authoritative sources of desired IAM configuration.

This distinction becomes particularly important when considering whether Port writes directly to cloud IAM or generates changes that are subsequently deployed through an existing pipeline.

## 2. Important architectural finding: Port does not necessarily replace Policy as Code

There is an important detail in Port's own implementation guide that should influence your evaluation.

Port's documented AWS IAM permission management implementation uses:

- Port blueprints to represent AWS resources and allowed IAM permissions.
- Port workflows to initiate permission requests and revocations.
- GitHub Actions as the execution backend.
- AWS IAM credentials to execute the actual IAM operations.
- Port entities to track provisioned permissions, requesters, and expiration.
- Timer-triggered workflows to revoke expired permissions.

In other words, Port can act as the developer-facing control plane while GitHub Actions remains the execution plane.

This is a significant architectural distinction. The documented approach is not simply Port independently replacing Terraform or your CI/CD deployment mechanism. It uses Port to orchestrate the IAM lifecycle through an external execution backend.

Port

+2

### Simplified architecture

Developer / Application Team

Requests temporary access to an AWS resource

Port Developer Portal

IAM request form · Blueprints · Workflow · Approval · Request tracking

Workflow dispatch

GitHub Actions / Execution Backend

Validate request · Generate IAM policy · Execute provisioning or revocation

AWS IAM

Create role · Create policy · Attach policy · Detach policy · Delete role

Port Context Lake / Audit Visibility

Provisioned permissions · Requester · Resource · Expiration · Workflow status

This architecture has an interesting benefit: you can introduce a more convenient developer experience without immediately abandoning your existing engineering automation.

However, it also introduces new questions around execution credentials, policy validation, deployment ownership, and reconciliation.

## 3. Pros and cons: Port vs. traditional Policy as Code

Here is how I would frame the comparison in an architecture review.

| Evaluation area | Port IAM management | Traditional Policy as Code |
| --- | --- | --- |
| Developer experience | Strong self-service experience | Requires Git/PR knowledge |
| Access requests | Workflow-driven | Usually ticket or PR-driven |
| Approval process | Can be integrated into workflows | PR approvals and pipeline gates |
| IAM policy definition | Catalog-driven permission selection and workflow logic | Version-controlled policy definitions |
| Deployment | Can orchestrate external execution | Native CI/CD deployment |
| Auditability | Requester and workflow tracking | Git history, pipeline logs, cloud audit logs |
| Temporary access | Supports expiry-driven revocation in documented guide | Requires custom automation or dedicated tooling |
| Policy validation | Must be implemented in workflow/backend | Mature policy testing and static validation ecosystem |
| Governance | Centralized request interface | Centralized through code review and policy enforcement |
| Drift management | Requires additional reconciliation design | Can use IaC plan and drift detection |
| Portability | Port-specific workflows and data model | Generally more portable |
| Change management | Workflow configuration and backend code | Git-based change management |

### Advantages of Port

1. Improved developer self-service

Developers can request permissions from a portal rather than understanding IAM policy syntax, locating the correct repository, creating a PR, and waiting for the deployment process.

This reduces operational friction for frequently requested, well-defined access.

2. Better visibility of who has requested access

Port's provisioned-permissions catalog provides a centralized view of access requests, requesters, resources, and generated policies.

This is useful for operational governance and access reviews.

Port

+1

3. Temporary access and automated revocation

This is probably one of the strongest use cases.

For example:

- Developer requests access to an S3 bucket.
- Developer selects an approved permission.
- The workflow provisions access.
- An expiration timestamp is recorded.
- A timer event triggers revocation.
- The role and associated policy are removed.

This can reduce standing permissions and support just-in-time access patterns.

Port

4. Reduced dependency on cloud engineering teams

Standardized permission requests can be delegated to application teams while cloud governance retains control over which permissions are available and who can execute workflows.

5. Faster delivery

For low-risk, frequently repeated access requests, a self-service workflow could reduce turnaround time compared with a conventional PR-based process.

### Disadvantages and potential risks

1. IAM execution credentials become a critical security boundary

Port's documented guide uses an AWS IAM management identity with permissions including:

- `iam:CreateRole`
- `iam:UpdateRole`
- `iam:DeleteRole`
- `iam:CreatePolicy`
- `iam:DeletePolicy`
- `iam:AttachRolePolicy`
- `iam:DetachRolePolicy`

The example policy uses `Resource: "*"`. This is a significant security consideration.

I would not deploy that example permission scope unchanged into a production environment.

Instead, investigate:

- Resource-level restrictions wherever supported.
- Separate execution identities by environment or account.
- Short-lived credentials through IAM roles and federation.
- Permission boundaries.
- Explicit trust policies.
- Restrictions on which principals can assume generated roles.

This should be one of the primary security gates in your experiment.

Port

+1

2. Potential bypass of existing governance controls

If Port workflows can create or modify IAM policies independently of the existing IaC pipeline, you could introduce a second mechanism for managing IAM.

This creates risks such as:

- Terraform-managed resources being modified outside Terraform.
- Configuration drift.
- Conflicting ownership of IAM roles.
- Unreviewed permission escalation.
- Difficulty determining which system is authoritative.

3. Limited policy validation unless explicitly engineered

A workflow that accepts a permission from a predefined list is not automatically a comprehensive IAM policy governance mechanism.

You still need to validate:

- Whether the action is approved.
- Whether the resource ARN is correct.
- Whether wildcard access is permitted.
- Whether conditions are required.
- Whether the permission violates organizational policies.
- Whether the resulting policy introduces privilege escalation.

4. Vendor dependency

Your permission catalog, workflows, and request model may become dependent on Port-specific blueprints, APIs, and execution integrations.

You should evaluate how easily the same access model can be exported, reproduced, or migrated.

5. Lifecycle and reconciliation complexity

What happens when someone manually modifies an IAM role in AWS?

What happens if the GitHub workflow succeeds but the Port workflow fails to update the catalog?

What happens if revocation fails?

These are important operational scenarios that need explicit handling.

## 4. Architectural design considerations for Cloud Governance

This is where I would spend most of the discussion time.

I would recommend covering the following eight design considerations.

### 4.1 Source of truth and ownership

This is probably the most important architectural decision.

You need to establish which system owns the desired IAM configuration.

There are three possible models:

Model 1 — Port as the primary provisioning interface

Higher governance impact- Port initiates IAM changes.
- Its workflows execute changes through the backend.
- Git is not necessarily the authoritative source for each provisioned permission.
- Requires additional reconciliation with IaC.

Model 2 — Port as the request interface, IaC as the source of truth

Recommended starting point- Developer submits a request through Port.
- Port triggers a GitHub Actions workflow.
- The backend generates a policy change.
- Changes are committed to Git and reviewed or validated.
- The existing deployment pipeline provisions the IAM changes.
- Port records the resulting status.

Model 3 — Hybrid management

Potential long-term model- Port handles temporary, time-bound access.
- Terraform handles permanent IAM roles and baseline policies.
- Security guardrails apply to both.
- Centralized inventory and reconciliation detect conflicts.

My preference is Model 2 initially, with Model 3 as a potential future state.

Why?

Because it allows the organization to benefit from Port's self-service functionality without creating competing sources of truth.

### 4.2 IAM privilege boundaries

You should establish what Port is allowed to provision.

For example, define permission categories:

| Category | Example | Suggested treatment |
| --- | --- | --- |
| Low risk | S3 read-only | Self-service eligible |
| Medium risk | S3 write access | Approval required |
| High risk | IAM policy administration | Security approval |
| Critical | Administrator access | Excluded from self-service |

I would establish the following controls:

- Explicit allowlist of IAM actions.
- Resource ARN restrictions.
- No unrestricted `Resource: "*"`, unless specifically justified.
- Permission boundaries on generated roles.
- Explicit trust relationships.
- Restrictions on `iam:PassRole`.
- No permission to modify governance or security administration roles.
- Account and environment restrictions.

AWS specifically recommends least privilege, temporary credentials, permission boundaries, and IAM Access Analyzer validation.

AWS Identity and Access Management

+1

### 4.3 Authentication and execution identity

One question to raise:

How does Port authenticate to AWS, and what identity actually executes the IAM changes?

The Port example uses an IAM management user with access credentials stored in GitHub secrets.

For a production architecture, I would investigate replacing long-lived IAM user credentials with:

- GitHub Actions OIDC federation.
- A dedicated AWS execution role.
- STS temporary credentials.
- Account-specific role assumption.
- Separate roles for development, staging, and production.

This reduces the risk associated with long-lived access keys.

Also consider whether the execution identity can only provision approved, constrained roles rather than create arbitrary IAM identities and policies.

### 4.4 Separation of duties and approval workflows

Port's workflow permissions can restrict who executes a workflow based on roles, users, teams, and dynamic policies.

Port

+1

However, workflow execution permission is not equivalent to an independent approval control.

You should define:

| Activity | Responsible party |
| --- | --- |
| Submit access request | Developer |
| Validate requested permission | Automated policy validation |
| Approve elevated access | Resource owner / Security |
| Execute IAM change | Restricted automation identity |
| Monitor access | Cloud Governance |
| Review exceptions | Security / IAM team |

An important discussion point:

Can a developer request and approve their own permission?

My recommendation is to prevent self-approval for elevated permissions and production access.

Also ensure the person who can modify the workflow definition cannot silently weaken the security controls governing the workflow.

### 4.5 Policy validation and preventive guardrails

Port should not be considered the policy validation engine simply because it provides a workflow interface.

You should consider retaining dedicated policy validation tools.

For example:

Proposed validation sequence

1. Request validation
   Is the requester authorized to request access to this resource?
2. Permission validation
   Is the requested IAM action on the approved allowlist?
3. Resource validation
   Does the ARN belong to the expected AWS account and environment?
4. Policy validation
   Does the generated IAM JSON comply with security standards? Use IAM Access Analyzer and/or existing policy-as-code tooling.
5. Approval validation
   Have the appropriate resource owner and security approvers approved the request?
6. Execution validation
   Does the execution identity have only the permissions necessary to perform the operation?
7. Post-deployment validation
   Does the actual AWS policy match the approved policy?

I would also retain automated checks for:

- Wildcard actions.
- Wildcard resources.
- Privilege escalation.
- Sensitive IAM actions.
- Cross-account trust.
- Public or unintended resource access.
- Missing policy conditions.
- Excessive policy size or statement complexity.

### 4.6 IAM drift detection and reconciliation

This is an area that deserves a dedicated architecture discussion.

Imagine the following:

1. Port provisions an IAM role.
2. Terraform also manages an IAM role with overlapping responsibilities.
3. An administrator manually changes the AWS IAM policy.
4. Port still displays the original provisioned permission.
5. Terraform subsequently attempts to reconcile its declared state.

Which system wins?

You need a defined reconciliation strategy.

My recommendation:

- Maintain a record of every provisioned role and policy ARN.
- Tag generated resources with ownership and request identifiers.
- Compare actual AWS IAM configuration against the approved configuration.
- Use CloudTrail to capture IAM API changes.
- Run periodic reconciliation jobs.
- Alert when unauthorized modifications occur.
- Define whether unexpected drift results in automatic remediation or manual review.

Do not rely exclusively on Port's catalog to establish actual cloud permissions. The AWS account must remain the authoritative source for what permissions are actually active.

### 4.7 Lifecycle management

Port's documented workflow supports time-based expiration and revocation. This is useful, but the architecture must handle failure scenarios.

Consider:

| Scenario | Required behavior |
| --- | --- |
| Permission expires | Automatically revoke |
| Revocation workflow fails | Alert and retry |
| Port becomes unavailable | Existing access should still expire independently |
| GitHub Actions unavailable | Avoid indefinite access |
| Developer leaves company | Trigger access revocation |
| Resource is deleted | Remove associated temporary permissions |
| Request is duplicated | Prevent duplicate provisioning |
| Workflow partially succeeds | Reconcile actual IAM state |

One particularly important question:

What happens if Port or GitHub Actions is unavailable when an access permission reaches its expiration time?

The expiration mechanism should not depend exclusively on a successful Port timer event.

Consider an independent scheduled reconciliation process in AWS or your automation platform.

### 4.8 Audit, compliance, and evidence

You should distinguish between three types of audit evidence:

1. Port audit evidence: Who initiated the workflow and what happened within Port?
2. CI/CD audit evidence: What code or automation executed?
3. AWS audit evidence: What IAM API changes actually occurred?

Port documents an audit log for organizational changes and workflow activity, but its documented default retention is 90 days for audit entries. That may not meet your organization's compliance retention requirements.

Port

+1

I would integrate the relevant evidence into your centralized logging/SIEM platform and retain it according to organizational policy.

## 5. Proposed target architecture

For an enterprise cloud governance environment, this is the architecture I would recommend exploring.

## Governed IAM self-service architecture

Developer / Application Team

Access request with business justification, resource, permission and duration

Port

Developer interface · Catalog · Workflow · RBAC · Approvals

Governance and policy validation layer

IAM allowlist

Approved actions

OPA / policy checks

Security guardrails

IAM Access Analyzer

Policy validation

Approval engine

Risk-based approvals

Execution layer

GitHub Actions / Terraform / AWS SDK · OIDC · STS

AWS Accounts

IAM roles · Identity policies · Permission boundaries · Trust policies

Continuous governance and observability

AWS CloudTrail · IAM inventory · Drift detection · SIEM · Access reviews · Expiration monitoring

The important architectural principle is that Port provides the self-service and orchestration experience, while the existing security and policy enforcement capabilities remain independently enforceable.

## 6. How I would structure the Proof of Concept (PoC)

I would avoid experimenting with production IAM roles initially.

Instead, build a PoC around one AWS account, a limited number of resources, and a small number of permissions.

### Suggested PoC scope

Recommended experiment| Component | PoC implementation |
| --- | --- |
| Cloud provider | AWS |
| Environment | Non-production |
| Resources | S3 bucket and EC2 instance |
| Permissions | S3 read-only and S3 write |
| Identity | Dedicated automation execution role |
| Request interface | Port workflow |
| Backend | GitHub Actions |
| Validation | IAM Access Analyzer + policy checks |
| Approval | Application owner |
| Expiration | 1-hour or 4-hour access |
| Audit | Port + GitHub + CloudTrail |

### Test scenarios

I would make the PoC demonstrate these scenarios:

| Test | Expected result |
| --- | --- |
| Request approved S3 read permission | Successfully provisioned |
| Request unapproved IAM action | Rejected |
| Request access to another account | Rejected |
| Request wildcard permissions | Rejected |
| Request elevated access | Approval required |
| Permission reaches expiry | Automatically revoked |
| Manual IAM policy modification | Drift detected |
| Execution workflow fails | Alert generated |
| Developer leaves organization | Access revoked |
| Duplicate request | No duplicate permission created |

### Success criteria

Don't measure success only by whether Port can provision an IAM role.

Measure whether it can do so securely, consistently, and with adequate operational visibility.

I would define the following acceptance criteria:

- 100% of provisioning requests have an identifiable requester.
- 100% of provisioned permissions pass policy validation.
- No unauthorized IAM actions can be provisioned.
- No long-lived AWS credentials are required.
- All elevated permissions require appropriate approval.
- Expired permissions are revoked within an agreed SLA.
- Failed provisioning and revocation operations generate alerts.
- Unauthorized IAM drift is detected.
- The existing IaC governance process is not bypassed unintentionally.

## 7. Questions to ask during the architecture review

These are the questions I would bring to the discussion when someone proposes experimenting with Port's IAM capabilities.

### A. Security architecture

1. What exact AWS IAM permissions does Port's execution identity require?
2. Can we use OIDC and assume-role rather than long-lived IAM credentials?
3. Can we restrict IAM provisioning to approved resources and actions?
4. Can we enforce permissions boundaries on every generated role?
5. How do we prevent privilege escalation through trust policies or `iam:PassRole`?
6. Can we independently validate generated IAM policies before execution?

### B. Governance and ownership

7. Is Port intended to become the source of truth for IAM, or just the request interface?
8. How will Port coexist with Terraform-managed IAM roles?
9. Who owns the approved permission catalog?
10. Who can modify the workflow and its security controls?
11. How do we enforce separation of duties?
12. How do we handle emergency access and exceptions?

### C. Operational architecture

13. How does Port handle failed provisioning or revocation?
14. What happens if the workflow backend is unavailable?
15. How do we detect manual changes made directly in AWS?
16. How do we reconcile Port's inventory with actual AWS IAM configuration?
17. Can we support multiple AWS accounts and environments?
18. Can we integrate provisioning and revocation evidence with our SIEM?

### D. Strategic considerations

19. Does this reduce operational overhead compared with our current pipeline?
20. What capabilities does Port provide that we cannot already achieve with our existing automation?
21. Does Port introduce an additional operational dependency?
22. Can we migrate the permission management logic outside Port if needed?
23. Is this intended for temporary developer access, permanent IAM role management, or both?

These questions help move the conversation away from simply evaluating a new feature toward evaluating its impact on the enterprise cloud security architecture.

## 8. Port vs. Policy as Code: Where should each be used?

I would not recommend treating them as mutually exclusive.

A better strategy is to identify which use cases benefit from self-service and which require stricter infrastructure change management.

| Use case | Recommended approach |
| --- | --- |
| Temporary developer access | Port workflow |
| Time-bound S3 access | Port workflow |
| Temporary production troubleshooting | Port + security approval |
| Permanent application IAM roles | Terraform / IaC |
| Standard workload IAM policies | Policy as Code |
| AWS account baseline policies | IaC + centralized governance |
| Organization-wide SCPs | IaC + security review |
| IAM permission boundary changes | Policy as Code |
| Emergency privileged access | Dedicated privileged access process |
| Access inventory and visibility | Port + AWS inventory |

The underlying philosophy:

- Port: Who needs access, why do they need it, and for how long?
- Policy as Code: Is the requested access compliant with organizational security standards?
- CI/CD: How is the approved change safely deployed?
- AWS IAM: What permissions are actually enforced?
- Cloud Governance: How do we continuously validate and monitor all of the above?

## 9. A practical recommendation: Three-phase adoption strategy

1. Phase 1 — Experiment and validate
   Start here- Deploy Port's documented IAM workflow in a sandbox.
   - Test provisioning and revocation.
   - Evaluate execution identity and permissions.
   - Validate approval controls.
   - Test failure and expiration scenarios.
   Outcome: Determine whether Port provides meaningful value for temporary access management.
2. Phase 2 — Integrate with existing governance
   - Introduce Policy as Code validation.
   - Integrate OIDC authentication.
   - Establish account-level execution boundaries.
   - Implement drift detection.
   - Integrate CloudTrail and SIEM.
   - Define clear ownership between Port and Terraform.
   Outcome: Establish a governed, hybrid architecture.
3. Phase 3 — Controlled production adoption
   - Expand to selected AWS accounts.
   - Introduce additional permission categories.
   - Implement automated access reviews.
   - Monitor provisioning and revocation SLAs.
   - Measure operational efficiency and security outcomes.
   Outcome: Establish whether Port should become a standard self-service interface for eligible IAM access requests.

## 10\. Suggested architecture review decision matrix

You can use this to structure the actual evaluation meeting.

Score each dimension from 1 to 5, where 1 is poor and 5 is excellent.

Port IAM evaluation scorecard

Enter scores based on PoC evidence, not assumptions or vendor demonstrations.

Security and least privilege

Weight: 25%

1

2

3

4

5

Governance and approvals

Weight: 15%

1

2

3

4

5

Policy validation

Weight: 15%

1

2

3

4

5

Auditability and compliance

Weight: 10%

1

2

3

4

5

Integration with existing IaC

Weight: 15%

1

2

3

4

5

Operational reliability

Weight: 10%

1

2

3

4

5

Developer experience

Weight: 5%

1

2

3

4

5

Portability and maintainability

Weight: 5%

1

2

3

4

5

Weighted score

# 0 / 100

0 of 8 criteria scored

 Copy evaluation

Important: I would make security, least privilege, and policy validation mandatory gates. A high overall score should never compensate for a critical security weakness.

## 11\. My proposed position as a Cloud Governance Engineer

If I were presenting this to the Cloud Architecture or Security Engineering team, my position would be:

I support experimenting with Port's IAM permission management capability, provided we treat it as a governed self-service access provisioning mechanism and not as an automatic replacement for our existing Policy as Code framework.

There are three reasons:

1. Developer experience: Port can simplify access requests and reduce the operational burden on cloud engineering teams.
2. Access lifecycle: Its workflow model provides an opportunity to standardize temporary access, approvals, and automated revocation.
3. Governance: We can potentially centralize access request visibility while retaining independent security validation and IaC controls.

However, I would establish three non-negotiable architectural requirements:

- No uncontrolled IAM provisioning or unrestricted execution credentials.
- No bypass of existing security policy validation and infrastructure ownership controls.
- No dependency on Port alone for access expiration, drift detection, or audit evidence.

The strongest adoption model is therefore a hybrid approach:

Port for self-service + Policy as Code for security guardrails + CI/CD for controlled execution + AWS for actual enforcement and audit evidence.

## 12\. Reference documentation for the discussion

These are the resources I would bring to the architecture review:

1. [Port – IAM Permission Management](<https://docs.port.io/guides/all/iam-permissions-guide/?utm_source=chatgpt.com>) — The actual AWS IAM provisioning and revocation implementation.
2. [Port – IAM Workflow Configuration](<https://www.docs.port.io/guides/all/iam-permissions-guide/?utm_source=chatgpt.com>) — How Port workflows dispatch GitHub Actions.
3. [Port – Governance Across Pillars](<https://docs.port.io/governance/governance-across-pillars/overview/?utm_source=chatgpt.com>) — Port RBAC and workflow governance.
4. [Port – Audit Log](<https://docs.port.io/platform-administration/audit-log/?utm_source=chatgpt.com>) — Audit capabilities and retention.
5. [AWS – IAM Security Best Practices](<https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html?utm_source=chatgpt.com>) — Least privilege, temporary credentials, permission boundaries, and policy validation.
6. [AWS Well-Architected – Use Temporary Credentials](<https://docs.aws.amazon.com/wellarchitected/latest/framework/sec02-bp02.html?utm_source=chatgpt.com>) — Recommended identity and credential architecture.

### A final point worth emphasizing in your meeting

I would ask the team one fundamental question:

> Are we trying to solve the problem of developers requesting cloud permissions, or are we trying to solve the problem of managing and governing IAM policies across our cloud environment?

These are two different problems.

Port's documented capability provides a promising solution for the first problem. The second requires a broader architecture involving policy enforcement, IaC ownership, identity governance, drift detection, and continuous compliance.

My recommendation: Start with temporary, resource-scoped developer access as the PoC. Keep permanent IAM role and baseline policy management within the existing Policy as Code pipeline until the experiment demonstrates that Port can meet the same governance and operational requirements.

That gives you a defensible technical position: you're not rejecting the new capability, but you're ensuring the experiment doesn't introduce a second, uncontrolled IAM management plane.
