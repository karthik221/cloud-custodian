# AWS Bedrock & Bedrock AgentCore – Enterprise Security Controls Framework

As a Senior Agentic Architect, I would approach AWS Bedrock security as an enterprise security control framework covering the complete AI lifecycle, rather than simply enabling Bedrock Guardrails or applying IAM policies.

The objective should be to establish security controls across:

1. AI model access and consumption.
2. Agent provisioning and deployment.
3. Agent identity and authentication.
4. Authorization and access to enterprise resources.
5. Prompt injection and malicious content protection.
6. Tool execution and MCP server security.
7. Data protection and privacy.
8. Network isolation and connectivity.
9. Runtime security and workload isolation.
10. Monitoring, audit and incident response.
11. Governance, compliance and lifecycle management.

I would divide the framework into two layers:

- Layer 1 – Amazon Bedrock security: Controls governing foundation models, inference APIs, model access, data protection, guardrails and consumption.
- Layer 2 – Bedrock AgentCore security: Controls governing agent execution, agent identity, tool access, memory, browser interactions, code execution and runtime isolation.

One important architectural principle: An agent must not inherit unrestricted permissions simply because it is running inside an approved Bedrock environment. Every agent should have its own identity, permissions, resource boundaries and audit trail.

## 1. Amazon Bedrock – Security control catalogue

These controls apply to the model platform, inference APIs, foundation models, knowledge bases and shared AI services.

### A. Identity and access management



Critical

&#x20;Objective: Only authorized users, applications and agents can access approved models and AI resources.



| Control ID | Security control            | Implementation approach                                                                    |
| ---------- | --------------------------- | ------------------------------------------------------------------------------------------ |
| BED-IAM-01 | Restrict model invocation   | IAM policies restricting `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` |
| BED-IAM-02 | Model allowlisting          | Allow only approved foundation models and model versions                                   |
| BED-IAM-03 | Role-based access           | Separate roles for developers, platform admins, security teams and applications            |
| BED-IAM-04 | Least privilege             | Restrict model access by model ARN, resource and supported conditions                      |
| BED-IAM-05 | Cross-account access        | Require explicitly approved IAM roles and trust policies                                   |
| BED-IAM-06 | Administrative separation   | Separate model enablement, guardrail administration and inference permissions              |
| BED-IAM-07 | Restrict model provisioning | Restrict who can create, import, customize or delete model resources                       |
| BED-IAM-08 | Deny unapproved models      | Use AWS Organizations SCPs where applicable to prevent unauthorized model access           |

Recommended implementation:

Create separate IAM permission sets:

- `Bedrock-Developer`: invoke approved models in development.
- `Bedrock-Production-Invoker`: invoke only approved production models.
- `Bedrock-Platform-Admin`: manage model configurations and approved resources.
- `Bedrock-Security-Admin`: manage guardrails and security configurations.
- `Bedrock-Auditor`: read-only access to configuration, inventory and audit evidence.

Avoid granting developers unrestricted `bedrock:*` permissions.

### B. Foundation model governance

Critical

| Control ID | Security control               | Implementation approach                                          |
| ---------- | ------------------------------ | ---------------------------------------------------------------- |
| BED-MOD-01 | Approved model catalogue       | Maintain an enterprise-approved model list                       |
| BED-MOD-02 | Model risk classification      | Classify models by data sensitivity and business use             |
| BED-MOD-03 | Model lifecycle governance     | Approve model onboarding, upgrades and retirement                |
| BED-MOD-04 | Model access restriction       | Prevent unauthorized access to experimental or high-risk models  |
| BED-MOD-05 | Model customization governance | Restrict fine-tuning and imported models to approved teams       |
| BED-MOD-06 | Regional restrictions          | Enforce approved AWS Regions and cross-region inference policies |
| BED-MOD-07 | Model usage tracking           | Track model usage, token consumption and application ownership   |

A useful enterprise control is a model allowlist maintained centrally, rather than allowing every development team to choose any available foundation model.

### C. Bedrock Guardrails and AI safety

Critical

This is one of the most important security control categories.

| Control ID | Security control                | Implementation approach                                                             |
| ---------- | ------------------------------- | ----------------------------------------------------------------------------------- |
| BED-GRD-01 | Harmful content filtering       | Configure hate, violence, sexual content, insults and other harmful-content filters |
| BED-GRD-02 | Prompt injection detection      | Enable prompt attack detection                                                      |
| BED-GRD-03 | PII detection                   | Detect and redact sensitive personal information                                    |
| BED-GRD-04 | Denied topics                   | Define enterprise-prohibited topics                                                 |
| BED-GRD-05 | Sensitive information filtering | Configure sensitive data and custom regex filters                                   |
| BED-GRD-06 | Grounding validation            | Detect unsupported or ungrounded responses where applicable                         |
| BED-GRD-07 | Contextual relevance            | Detect irrelevant or off-topic responses where applicable                           |
| BED-GRD-08 | Guardrail enforcement           | Require approved guardrails on applicable production inference paths                |
| BED-GRD-09 | Guardrail versioning            | Deploy approved, versioned guardrail configurations                                 |
| BED-GRD-10 | Guardrail bypass prevention     | Prevent application teams from invoking models through unprotected paths            |

Important architectural consideration:

Do not assume that creating a Bedrock Guardrail automatically protects every model invocation.

You must enforce its application on the relevant inference paths, including supported Converse and InvokeModel operations, and test whether alternative APIs or direct model access can bypass the intended control.

I would establish three enterprise guardrail profiles:

| Profile   | Intended use                                                 | Protection                                                       |
| --------- | ------------------------------------------------------------ | ---------------------------------------------------------------- |
| Standard  | General enterprise assistants                                | Baseline content filters, PII and prompt attack detection        |
| Sensitive | HR, finance, legal and internal enterprise data              | Stronger PII, denied-topic and prompt attack controls            |
| High risk | Agents performing privileged or business-critical operations | Strong filtering, deterministic policy checks and human approval |

Guardrails are not a replacement for authorization. For example, a guardrail cannot determine whether a particular employee is authorized to approve a financial transaction.

### D. Data protection and encryption

Critical

| Control ID | Security control             | Implementation approach                                              |
| ---------- | ---------------------------- | -------------------------------------------------------------------- |
| BED-DAT-01 | Encryption at rest           | Use AWS KMS                                                          |
| BED-DAT-02 | Customer-managed keys        | CMK for supported resources requiring customer-controlled encryption |
| BED-DAT-03 | Encryption in transit        | Enforce TLS 1.2 or higher                                            |
| BED-DAT-04 | Sensitive prompt protection  | Prevent unnecessary transmission of confidential information         |
| BED-DAT-05 | PII masking                  | Mask sensitive data before inference where appropriate               |
| BED-DAT-06 | Invocation log protection    | Encrypt logs and restrict access                                     |
| BED-DAT-07 | Data retention               | Define retention and deletion policies                               |
| BED-DAT-08 | Cross-region data governance | Control where inference and supporting data are processed            |
| BED-DAT-09 | Knowledge base protection    | Restrict access to approved S3, vector stores and data sources       |
| BED-DAT-10 | Data classification          | Classify data before exposing it to AI applications                  |

One important distinction: CMK support varies by Bedrock resource. Do not assume that every inference request or foundation model itself can be configured with an individual CMK.

### E. Network security

Critical

| Control ID | Security control           | Implementation approach                                       |
| ---------- | -------------------------- | ------------------------------------------------------------- |
| BED-NET-01 | Private connectivity       | Use AWS PrivateLink/VPC interface endpoints where supported   |
| BED-NET-02 | VPC endpoint restrictions  | Restrict access through endpoint policies                     |
| BED-NET-03 | Public access restrictions | Restrict unapproved public network paths                      |
| BED-NET-04 | Egress control             | Restrict outbound connectivity to approved destinations       |
| BED-NET-05 | Region restrictions        | Enforce approved regional processing                          |
| BED-NET-06 | Network segmentation       | Separate development, test and production AI workloads        |
| BED-NET-07 | DNS security               | Use approved DNS resolution paths                             |
| BED-NET-08 | Network monitoring         | Enable VPC Flow Logs and relevant network security monitoring |

AWS provides specific data perimeter guidance for Bedrock, including VPC endpoint enforcement, SCPs, network segmentation and regional restrictions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

AWS Documentation+1



### F. Logging, audit and monitoring

| Control ID | Security control         | Implementation approach                                    |
| ---------- | ------------------------ | ---------------------------------------------------------- |
| BED-LOG-01 | API audit logging        | Enable AWS CloudTrail                                      |
| BED-LOG-02 | Model invocation logging | Enable invocation logging where justified                  |
| BED-LOG-03 | Guardrail monitoring     | Monitor blocked and filtered requests                      |
| BED-LOG-04 | Anomaly detection        | Detect unusual invocation volume and token consumption     |
| BED-LOG-05 | Administrative activity  | Monitor model, IAM and guardrail configuration changes     |
| BED-LOG-06 | Centralized logging      | Forward security events to a central logging/SIEM platform |
| BED-LOG-07 | Log access control       | Restrict access to prompts, responses and traces           |
| BED-LOG-08 | Cost anomaly detection   | Alert on unusual model usage and unexpected cost increases |

A critical security consideration: Bedrock invocation logs can contain complete prompts and model responses. They may therefore contain credentials, personal information and confidential enterprise data. Logging must have its own data classification, encryption, access control and retention policy. Invocation logging is disabled by default.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock+1



## 2. Amazon Bedrock AgentCore – Security control catalogue

This is where I would introduce a more stringent security framework.

AgentCore has multiple components, and each has a different security responsibility.

## AgentCore security architecture

Enterprise users / applications

Entra ID authentication

Kong AI Gateway

Central entry point · API policies · rate limits

AgentCore security capabilities

Identity

Authentication and credentials

Gateway

Controlled tool access

Policy

Action authorization

Runtime

Execution isolation

Memory

Conversation data isolation

Browser / Code Interpreter

Secure execution and browsing

Enterprise systems and data

AWS · Azure · Databricks · APIs · MCP servers · SaaS

Observability, audit and governance should span all layers.

### A. AgentCore Runtime security

Critical

The Runtime is the execution environment for your agents.

| Control ID | Security control             | Implementation                                                                   |
| ---------- | ---------------------------- | -------------------------------------------------------------------------------- |
| ACR-RT-01  | Private network mode         | Require VPC network mode where the workload's connectivity requirements allow it |
| ACR-RT-02  | Session isolation            | Ensure isolated agent execution sessions                                         |
| ACR-RT-03  | Dedicated execution identity | Assign dedicated IAM execution roles                                             |
| ACR-RT-04  | Least privilege              | Limit access to only required AWS resources                                      |
| ACR-RT-05  | Runtime authentication       | Require IAM or approved JWT-based authentication                                 |
| ACR-RT-06  | Runtime authorization        | Restrict who can invoke each agent                                               |
| ACR-RT-07  | Image security               | Scan container images for vulnerabilities                                        |
| ACR-RT-08  | Dependency security          | Scan Python packages, libraries and dependencies                                 |
| ACR-RT-09  | Runtime configuration        | Restrict unapproved runtime configuration changes                                |
| ACR-RT-10  | Secret protection            | Prevent credentials from being embedded in source code or images                 |
| ACR-RT-11  | Resource protection          | Apply execution limits, timeout policies and workload quotas                     |
| ACR-RT-12  | Runtime lifecycle            | Track deployed version, owner and approved release                               |

Important: AgentCore Runtime provides isolated sessions using microVM technology. However, session isolation does not automatically enforce business-level authorization or tenant-level data permissions inside your application. You must implement those controls too.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



### B. AgentCore Identity security

Critical

This should be one of your strongest control areas, particularly because your enterprise has selected Entra ID as its identity provider.

| Control ID | Security control           | Implementation                                                        |
| ---------- | -------------------------- | --------------------------------------------------------------------- |
| ACR-ID-01  | User authentication        | Authenticate users through Entra ID                                   |
| ACR-ID-02  | Agent identity             | Assign an identifiable identity to each agent                         |
| ACR-ID-03  | Tool authentication        | Authenticate agents when connecting to downstream tools               |
| ACR-ID-04  | OAuth integration          | Use OAuth 2.0/OIDC for supported integrations                         |
| ACR-ID-05  | Token exchange             | Use approved credential exchange and delegated authorization patterns |
| ACR-ID-06  | Token protection           | Securely store and manage OAuth credentials                           |
| ACR-ID-07  | Token lifecycle            | Define expiration, refresh and revocation                             |
| ACR-ID-08  | User context propagation   | Preserve the initiating user's identity and authorization context     |
| ACR-ID-09  | Credential isolation       | Prevent one agent from accessing another agent's credentials          |
| ACR-ID-10  | Cross-cloud authentication | Use federated authentication for AWS-to-Azure connectivity            |

Architecture recommendation for your environment:

```
User
  |
  v
Microsoft Entra ID
  |
  v
Kong AI Gateway
  |
  v
Bedrock AgentCore Runtime
  |
  v
AgentCore Identity
  |
  +---- AWS IAM Role
  |
  +---- Azure OAuth / Entra token
  |
  +---- Databricks OAuth / service principal
  |
  +---- External SaaS credentials
```

A crucial distinction:

- The AWS IAM execution role identifies the agent's AWS workload permissions.
- The user's Entra ID token establishes the user's identity.
- AgentCore Identity manages authentication and credential access for downstream integrations.
- The downstream application must still authorize the actual requested operation.

Do not use a single powerful Azure service principal for all agents. Prefer separate identities or tightly scoped credentials based on the application and resource boundaries.

### C. AgentCore Gateway security

Critical

Gateway is particularly important because agents can invoke APIs, Lambda functions and MCP tools.

| Control ID | Security control             | Implementation                                                |
| ---------- | ---------------------------- | ------------------------------------------------------------- |
| ACR-GW-01  | Gateway authentication       | Require authentication for inbound requests                   |
| ACR-GW-02  | Tool allowlisting            | Register only approved APIs, MCP servers and Lambda functions |
| ACR-GW-03  | Tool-level authorization     | Restrict which agents can invoke which tools                  |
| ACR-GW-04  | Schema validation            | Validate tool inputs and outputs                              |
| ACR-GW-05  | API security                 | Enforce approved API authentication                           |
| ACR-GW-06  | Rate limiting                | Limit calls by agent, user and application                    |
| ACR-GW-07  | Egress restrictions          | Restrict tools from accessing unapproved endpoints            |
| ACR-GW-08  | Credential isolation         | Avoid exposing downstream credentials to the model            |
| ACR-GW-09  | Tool registration governance | Require approval before onboarding new tools                  |
| ACR-GW-10  | Tool invocation auditing     | Record tool invocation, identity, target and outcome          |
| ACR-GW-11  | WAF protection               | Apply supported web ACL protections                           |
| ACR-GW-12  | Configuration encryption     | Use customer-managed KMS keys where required and supported    |

My recommendation: Build a centralized enterprise Tool Registry.

For example:

| Tool                      | Permitted agent        | Access                |
| ------------------------- | ---------------------- | --------------------- |
| AWS Cost Explorer         | Cloud Governance Agent | Read-only             |
| AWS Trusted Advisor       | Cloud Governance Agent | Read-only             |
| Azure Advisor API         | Cloud Governance Agent | Read-only             |
| Databricks SQL API        | Analytics Agent        | Restricted queries    |
| Azure DevOps API          | DevOps Agent           | Restricted operations |
| Production deployment API | Deployment Agent       | Approval required     |

This prevents agents from dynamically discovering and calling arbitrary APIs.

An additional consideration for your architecture: Kong and AgentCore Gateway have overlapping API gateway capabilities, but they serve different architectural roles.

I would use:

- Kong: Enterprise-wide API and AI traffic governance.
- AgentCore Gateway: Agent-to-tool integration and agent-specific tool governance.
- AgentCore Policy: Deterministic authorization of agent tool actions.

You should avoid duplicating authentication and rate-limiting policies unnecessarily, but make sure that every tool invocation has an enforceable authorization boundary.

### D. AgentCore Policy security

Critical

This is especially important for autonomous agents.

An agent may decide to invoke tools based on its reasoning. The model should never be the final authority for whether an operation is permitted.

| Control ID | Security control              | Example                                                      |
| ---------- | ----------------------------- | ------------------------------------------------------------ |
| ACR-POL-01 | Tool authorization            | Only approved agents can execute specific tools              |
| ACR-POL-02 | Read/write separation         | Read operations allowed; write operations restricted         |
| ACR-POL-03 | High-risk action restrictions | Restrict production deployment and deletion                  |
| ACR-POL-04 | Human approval                | Require approval before privileged actions                   |
| ACR-POL-05 | Context-based authorization   | Evaluate user, agent, environment and resource context       |
| ACR-POL-06 | Policy versioning             | Maintain approved policy versions                            |
| ACR-POL-07 | Default deny                  | Deny actions without an explicit allow decision              |
| ACR-POL-08 | Policy audit                  | Record authorization decisions                               |
| ACR-POL-09 | Separation of duties          | Prevent an agent from approving its own privileged operation |

Example policy:

```
Agent: Cloud-Governance-Agent

Allowed:
  - Read AWS Trusted Advisor
  - Read AWS Cost Explorer
  - Read Azure Advisor
  - Read resource configurations

Restricted:
  - Modify IAM policies
  - Delete cloud resources
  - Change production configurations

Approval required:
  - Create production resources
  - Modify production security groups
  - Execute remediation actions
```

I would make one architectural rule mandatory:

The agent can recommend an action, but a deterministic authorization layer must decide whether it can execute that action.

For high-risk actions, use a separate approval workflow outside the agent's own reasoning loop.

### E. AgentCore Memory security

Critical

Memory introduces a different category of risk because information from previous sessions may influence future agent behavior.

| Control ID | Security control            | Implementation                                                     |
| ---------- | --------------------------- | ------------------------------------------------------------------ |
| ACR-MEM-01 | Encryption at rest          | Use customer-managed KMS keys where supported                      |
| ACR-MEM-02 | User-level isolation        | Separate user memory                                               |
| ACR-MEM-03 | Agent-level isolation       | Separate agent-specific memory                                     |
| ACR-MEM-04 | Tenant isolation            | Prevent cross-tenant memory access                                 |
| ACR-MEM-05 | Data retention              | Define memory retention periods                                    |
| ACR-MEM-06 | Data deletion               | Support deletion and retention enforcement                         |
| ACR-MEM-07 | Sensitive data filtering    | Prevent credentials and sensitive information from entering memory |
| ACR-MEM-08 | Memory poisoning protection | Validate untrusted information before persistent storage           |
| ACR-MEM-09 | Memory access control       | Restrict which agents can read or update memory                    |
| ACR-MEM-10 | Audit                       | Log memory creation, retrieval and deletion events where available |

A practical scenario:

An HR agent should never retrieve another employee's conversation history simply because both employees use the same agent.

Memory must be scoped to the correct user, tenant and business context.

### F. AgentCore Browser security

If agents use browser automation, introduce additional security controls.

| Control ID | Security control             | Implementation                                         |
| ---------- | ---------------------------- | ------------------------------------------------------ |
| ACR-BR-01  | Browser network restrictions | Avoid unrestricted public network access               |
| ACR-BR-02  | Domain allowlisting          | Permit only approved enterprise domains                |
| ACR-BR-03  | Session isolation            | Separate browser sessions                              |
| ACR-BR-04  | Credential protection        | Prevent passwords and access tokens from being exposed |
| ACR-BR-05  | Session recording            | Enable recording for audit-sensitive use cases         |
| ACR-BR-06  | Download restrictions        | Restrict unapproved file downloads                     |
| ACR-BR-07  | Upload restrictions          | Prevent unauthorized uploads                           |
| ACR-BR-08  | Browser prompt injection     | Treat web content as untrusted input                   |

A major concern is indirect prompt injection: a web page can contain instructions designed to manipulate an agent into revealing confidential information or executing unauthorized actions.

### G. AgentCore Code Interpreter security

| Control ID | Security control              | Implementation                                          |
| ---------- | ----------------------------- | ------------------------------------------------------- |
| ACR-CI-01  | Private network configuration | Use private networking where applicable                 |
| ACR-CI-02  | Execution isolation           | Use isolated execution environments                     |
| ACR-CI-03  | Code validation               | Validate generated code before execution where feasible |
| ACR-CI-04  | Dependency restrictions       | Restrict unapproved packages                            |
| ACR-CI-05  | File access restrictions      | Restrict filesystem and mounted data access             |
| ACR-CI-06  | Egress restrictions           | Prevent unrestricted outbound connections               |
| ACR-CI-07  | Execution limits              | Enforce resource and execution limits                   |
| ACR-CI-08  | Secret protection             | Prevent access to credentials and environment secrets   |
| ACR-CI-09  | Audit                         | Record execution metadata and security events           |

Do not treat a sandbox as a substitute for authorization. A sandbox limits execution impact, but it does not automatically make every generated script safe.

## 3. Enterprise security controls that span both Bedrock and AgentCore

These are controls I would establish centrally rather than implementing independently for each agent.

| Control domain           | Enterprise control                     | AWS implementation                                      |
| ------------------------ | -------------------------------------- | ------------------------------------------------------- |
| Governance               | Central agent inventory                | AgentCore Registry / enterprise Agent Registry          |
| Provisioning             | Approved agent deployment templates    | Terraform modules                                       |
| Compliance               | Prevent noncompliant deployment        | AWS Organizations SCPs, IAM and policy-as-code          |
| Vulnerability management | Scan agent images and dependencies     | Amazon Inspector and ECR scanning                       |
| Threat detection         | Detect suspicious API and IAM activity | GuardDuty, CloudTrail                                   |
| Configuration compliance | Continuously assess resources          | AWS Config, Security Hub                                |
| Secrets                  | Central secrets management             | AWS Secrets Manager                                     |
| Encryption               | Central key governance                 | AWS KMS                                                 |
| Data protection          | Detect sensitive data exposure         | Amazon Macie                                            |
| Monitoring               | Agent traces and security events       | AgentCore Observability, CloudWatch                     |
| Enterprise monitoring    | Centralized monitoring                 | Dynatrace integration                                   |
| API governance           | Central API security                   | Kong                                                    |
| Identity governance      | Enterprise identity integration        | Microsoft Entra ID                                      |
| Incident response        | Automated security response            | EventBridge, Lambda and incident management integration |

AWS Security Hub now documents specific AgentCore CSPM controls, which are particularly useful as a starting point for automated compliance.

These include:

- AgentCore Runtime must use VPC network mode.
- AgentCore Gateway must require inbound authorization.
- AgentCore Memory must use customer-managed KMS encryption.
- AgentCore Gateway must use customer-managed KMS encryption.
- Custom browsers must not use public network mode.
- Custom browsers must have session recording enabled.
- Custom Code Interpreters should use private network configuration.

Check regional availability and applicability when implementing these controls.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

AWS Security Hub



## 4. How I would enforce these controls through Terraform

This is where you can make the framework operational.

I would not rely on application teams remembering to configure security controls manually. Security should be embedded into the standard Terraform modules used to provision Bedrock and AgentCore resources.

### Recommended provisioning architecture

Application team submits agent request

Use case · Owner · Environment · Data classification

Enterprise Agent Provisioning Pipeline

GitHub / Azure DevOps · Terraform

Preventive checks

OPA / Checkov / tfsec · IAM validation · Policy validation

Approval checks

Security approval · Data classification · Risk assessment

Terraform deployment

Bedrock · AgentCore Runtime · Identity · Gateway · Memory · Policy

Continuous compliance

AWS Config · Security Hub · CloudTrail · Dynatrace

### Suggested Terraform enforcement controls

| Security requirement      | Pipeline enforcement                              |
| ------------------------- | ------------------------------------------------- |
| Approved foundation model | Reject unapproved model IDs                       |
| Approved AWS Region       | Reject deployments outside approved Regions       |
| Mandatory tags            | Reject missing owner, application and environment |
| Private runtime           | Reject noncompliant network configuration         |
| Runtime IAM role          | Reject wildcard permissions                       |
| Approved guardrail        | Require an approved guardrail configuration       |
| Gateway authentication    | Reject unauthenticated production gateways        |
| Memory encryption         | Require approved KMS configuration                |
| Gateway encryption        | Require approved KMS configuration                |
| Browser security          | Reject public browser networking where prohibited |
| Code interpreter security | Require approved private networking               |
| Container image           | Reject images with critical vulnerabilities       |
| Agent ownership           | Require an identifiable business owner            |

For implementation, I would use:

- Terraform modules for reusable, approved configurations.
- OPA or HashiCorp Sentinel for policy enforcement.
- Checkov or equivalent IaC security scanning.
- AWS Config and Security Hub for post-deployment compliance.
- AWS Organizations SCPs for account-level guardrails.

An important distinction: Terraform checks are preventive, while AWS Config and Security Hub provide continuous detection. You need both.

## 5. Security control prioritization – What should be mandatory?

I would introduce three control tiers.

Tier 1 – Mandatory baseline

P0

Required for every production agent.

- Dedicated agent identity and least-privilege IAM role.
- Authentication and authorization for runtime invocation.
- Approved foundation models.
- Mandatory prompt attack and sensitive data protections based on use case.
- Secure secrets management.
- Encryption for supported sensitive resources.
- Approved network configuration.
- Centralized audit logging.
- Agent owner, environment and business classification.

  Tier 2 – Advanced protection

  P1

  Required for sensitive data and enterprise-connected agents.
- User-context propagation.
- Fine-grained tool-level authorization.
- Tenant and memory isolation.
- Browser and code interpreter restrictions.
- MCP server allowlisting.
- Prompt injection testing.
- Human approval for privileged operations.
- Egress filtering and network segmentation.
- Image and dependency scanning.

  Tier 3 – High-risk workloads

  P2

  Required for agents performing privileged or business-critical operations.
- Multi-party approval for critical actions.
- Just-in-time credentials.
- Transaction-level authorization.
- Independent policy decision engine.
- Enhanced trace and audit retention.
- Automated threat detection and incident response.
- Continuous adversarial testing.
- Independent security assessment before production release.

## 6. Security dashboard – How to measure compliance

I would create a centralized Bedrock Security Posture Dashboard.

Some recommended KPIs:

| Category         | Security metric                                                  |
| ---------------- | ---------------------------------------------------------------- |
| Identity         | % of agents with dedicated IAM roles                             |
| Identity         | % of agents using approved identity federation                   |
| Model governance | % of inference traffic using approved models                     |
| Guardrails       | % of production inference paths protected by approved guardrails |
| Runtime          | % of production runtimes using compliant network configuration   |
| Gateway          | % of gateways enforcing authentication                           |
| Tool security    | % of registered tools with approved authorization policies       |
| Memory           | % of sensitive memory resources encrypted with CMKs              |
| Data protection  | % of agents with defined data classification                     |
| Vulnerability    | Number of critical vulnerabilities in agent images               |
| Logging          | % of production agents with audit logging enabled                |
| Governance       | % of agents with owner and lifecycle metadata                    |
| Compliance       | Number of open high-risk security findings                       |

For your existing Dynatrace environment, I would integrate security-relevant AgentCore traces and metrics with Dynatrace, while retaining CloudTrail, Security Hub and AWS Config as authoritative AWS security evidence sources.

## 7. Ten thoughtful questions to ask the AWS, Security and Platform teams

These questions will help identify gaps in the current security architecture.

1\. Identity: Are we assigning a unique workload identity to every agent, or are multiple agents sharing the same IAM execution role?

2\. Authorization: How do we ensure that an agent can only execute tools and actions explicitly approved for that agent?

3\. Prompt injection: Are we implementing prompt injection protection at both the model inference and agent tool-execution layers?

4\. Gateway: Can an agent invoke AgentCore Runtime or downstream APIs directly and bypass Kong or AgentCore Gateway security policies?

5\. Secrets: How are we preventing agents from exposing credentials, OAuth tokens and service principal secrets in prompts, logs or responses?

6\. Cross-cloud access: How are agents hosted in AWS authenticating to Azure resources and Databricks without relying on shared, long-lived credentials?

7\. Memory: How are we preventing cross-user and cross-tenant data leakage through persistent agent memory?

8\. Tool governance: Do we have a centrally managed registry of approved MCP servers, APIs and tools, including their owners and permissions?

9\. Provisioning: Are all mandatory security controls enforced through Terraform, or are we relying on individual application teams to configure them?

10\. Continuous compliance: How do we continuously validate that an agent remains compliant after deployment, especially when its IAM permissions, tools or configuration change?

## 8. My recommended enterprise security architecture

Considering your existing architecture choices (Entra ID, Kong, Dynatrace, AWS, Azure and Databricks), I would recommend the following ownership model:

| Security responsibility                   | Recommended owner/platform          |
| ----------------------------------------- | ----------------------------------- |
| User authentication                       | Microsoft Entra ID                  |
| Enterprise API governance                 | Kong                                |
| Agent execution isolation                 | Bedrock AgentCore Runtime           |
| Agent identity and downstream credentials | AgentCore Identity                  |
| AWS workload permissions                  | IAM                                 |
| Agent tool integration                    | AgentCore Gateway                   |
| Agent action authorization                | AgentCore Policy                    |
| AI content protection                     | Bedrock Guardrails                  |
| Encryption and key governance             | AWS KMS                             |
| Secrets                                   | AWS Secrets Manager                 |
| Network isolation                         | VPC, PrivateLink, security groups   |
| Infrastructure policy enforcement         | Terraform + OPA                     |
| Security posture                          | AWS Security Hub + Config           |
| Audit                                     | CloudTrail                          |
| Runtime monitoring                        | AgentCore Observability + Dynatrace |
| Agent inventory                           | Enterprise Agent Registry           |

My strongest recommendation: Establish an Enterprise Agent Security Baseline with approximately 25–35 mandatory controls initially, then expand it based on agent risk classification.

Do not make the framework exclusively Bedrock-specific. The same security control model should eventually work across AWS Bedrock AgentCore and Azure AI Foundry. For example, agent identity, tool authorization, memory isolation, prompt injection protection, and lifecycle governance should be platform-independent control objectives.

### AWS reference documentation

1. [AWS Security Hub – AgentCore security controls](https://docs.aws.amazon.com/securityhub/latest/userguide/bedrockagentcore-controls.html?utm_source=chatgpt.com)
2. [AWS Prescriptive Guidance – Generative AI security architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture-generative-ai/bedrock-integration.html?utm_source=chatgpt.com)
3. [AgentCore security and access controls](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness-security.html?utm_source=chatgpt.com)
4. [Data perimeter for Amazon Bedrock](https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/data-perimeter-for-amazon-bedrock/data-perimeter-for-amazon-bedrock.pdf?utm_source=chatgpt.com)
5. [Implementing least privilege access for Bedrock](https://aws.amazon.com/blogs/security/implementing-least-privilege-access-for-amazon-bedrock/?utm_source=chatgpt.com)

A particularly useful next deliverable would be a Bedrock and AgentCore Security Control Matrix in Excel, with control IDs, descriptions, risk ratings, AWS service mappings, Terraform enforcement methods, validation procedures, evidence requirements and ownership. This could become the foundation for your enterprise security architecture review and security sign-off process.




===========================




===================================



# AWS Bedrock & AgentCore – Enterprise Security Control Framework

I recommend organizing the security controls around NIST Cybersecurity Framework (CSF 2.0), NIST AI Risk Management Framework (AI RMF), and AWS Well-Architected Security Pillar.

This gives you a standards-aligned framework rather than a list of individual AWS service configurations.

The framework below is designed for enterprise security architecture reviews and can be applied to both Amazon Bedrock and Bedrock AgentCore.

## 1. Security categories and control matrix

Priority: P0 = mandatory baseline · P1 = enhanced protection · P2 = risk-dependent

| Security category                            | NIST alignment | Key security controls                                                                                                     | AWS implementation                                    |
| -------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| 1. Identity & Access Management              | PR.AA          | Least privilege, RBAC, MFA for administrators, workload identity, agent-specific IAM roles, cross-account access controls | IAM, IAM Identity Center, AgentCore Identity, STS     |
| 2. Data Protection & Privacy                 | PR.DS          | Encryption at rest/transit, CMK, PII masking, data classification, retention, memory isolation                            | KMS, Secrets Manager, S3 encryption, AgentCore Memory |
| 3. Network Security                          | PR.IR          | Private connectivity, VPC isolation, endpoint policies, egress restrictions, approved Regions                             | VPC, PrivateLink, Security Groups, SCPs               |
| 4. AI Model Governance                       | GV.PO / GOVERN | Approved model catalogue, model risk classification, model version governance, usage restrictions                         | Bedrock model access, IAM, Organizations              |
| 5. AI Safety & Guardrails                    | PR.PS / MANAGE | Prompt injection protection, harmful content filtering, PII filtering, denied topics, grounding validation                | Bedrock Guardrails                                    |
| 6. Agent Runtime Security                    | PR.IR / PR.PS  | Runtime isolation, secure execution, session isolation, container image scanning, dependency security                     | AgentCore Runtime, ECR, Inspector                     |
| 7. Tool & API Security                       | PR.AA / PR.PS  | MCP allowlisting, API authentication, tool-level authorization, input validation, rate limiting                           | AgentCore Gateway, AgentCore Policy, Kong             |
| 8. Secrets & Credential Management           | PR.AA / PR.DS  | No hardcoded credentials, credential rotation, token lifecycle, secure cross-cloud authentication                         | Secrets Manager, AgentCore Identity, IAM, Entra ID    |
| 9. Logging & Monitoring                      | DE.CM / DE.AE  | API audit logs, inference monitoring, agent traces, anomalous activity detection, security alerting                       | CloudTrail, CloudWatch, Security Hub, Dynatrace       |
| 10. Vulnerability & Configuration Management | ID.RA / PR.PS  | IaC scanning, vulnerability scanning, secure configuration baselines, patch management                                    | Inspector, AWS Config, Security Hub, Terraform        |
| 11. Incident Response & Recovery             | RS.MA / RC.RP  | Agent shutdown, credential revocation, compromised agent isolation, incident investigation and recovery                   | EventBridge, Lambda, CloudTrail, Security Hub         |
| 12. Governance & Compliance                  | GV.OV / GV.RM  | Agent inventory, ownership, risk classification, lifecycle management, periodic compliance assessment                     | Agent Registry, AWS Config, Security Hub              |

## 2. Recommended control mapping by NIST framework

For a formal enterprise security policy, I would map the controls to the six NIST CSF 2.0 functions:

| NIST function | What it addresses                                     | Example Bedrock controls                                                     |
| ------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------- |
| GOVERN (GV)   | Security policies, ownership, risk and accountability | Approved models, agent registry, risk classification, lifecycle governance   |
| IDENTIFY (ID) | Asset discovery and risk assessment                   | Bedrock inventory, agent inventory, data classification, threat modeling     |
| PROTECT (PR)  | Prevent unauthorized access and security incidents    | IAM, encryption, Guardrails, private networking, tool authorization          |
| DETECT (DE)   | Identify suspicious activity                          | CloudTrail, CloudWatch, agent traces, anomaly detection                      |
| RESPOND (RS)  | Contain and investigate incidents                     | Agent suspension, credential revocation, incident response automation        |
| RECOVER (RC)  | Restore secure operations                             | Agent redeployment, configuration recovery, key rotation, backup restoration |

For AI-specific risks, complement this with the NIST AI RMF:

- GOVERN: Establish AI governance and accountability.
- MAP: Identify agent use cases, risks, data and dependencies.
- MEASURE: Evaluate model behavior, security and performance.
- MANAGE: Mitigate risks and continuously monitor agents.

## 3. AWS security standards to use as implementation baselines

I would use these standards in your security architecture documentation:

| Standard                                        | Purpose                                 |
| ----------------------------------------------- | --------------------------------------- |
| AWS Well-Architected Security Pillar            | Overall AWS security architecture       |
| AWS Foundational Security Best Practices (FSBP) | AWS resource configuration compliance   |
| CIS AWS Foundations Benchmark                   | AWS account and infrastructure security |
| NIST SP 800-53 Rev. 5                           | Detailed security control requirements  |
| NIST AI RMF 1.0                                 | AI risk management                      |
| OWASP Top 10 for LLM Applications               | LLM-specific security risks             |
| OWASP Top 10 for Agentic Applications           | Agent-specific threats                  |

Particularly relevant AWS development: AWS Security Hub CSPM introduced an AI Security Best Practices standard (v1.0.0) with 31 automated controls in June 2026. It covers Bedrock, AgentCore and SageMaker. This is worth using as a technical compliance baseline rather than building every AWS configuration check from scratch.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://aws.amazon.com.cdn.amazon.com\&sz=32)

AWS+1



## 4. My recommendation: Minimum mandatory security baseline

For your enterprise, I would start with these 15 controls:

| #  | Mandatory security control                                            | Enforcement                             |
| -- | --------------------------------------------------------------------- | --------------------------------------- |
| 1  | Only approved foundation models                                       | IAM / Model allowlist                   |
| 2  | Dedicated identity for each agent                                     | IAM / AgentCore Identity                |
| 3  | Least-privilege permissions                                           | IAM policies                            |
| 4  | Entra ID integration for user authentication                          | AgentCore Identity / OAuth              |
| 5  | Approved Bedrock Guardrails                                           | Terraform / Guardrails                  |
| 6  | Encryption using approved KMS keys                                    | AWS KMS                                 |
| 7  | Private networking for production agents where supported and required | VPC / PrivateLink                       |
| 8  | Mandatory gateway authentication                                      | AgentCore Gateway                       |
| 9  | Approved tool and MCP server allowlist                                | AgentCore Gateway                       |
| 10 | Deterministic authorization for privileged agent actions              | AgentCore Policy                        |
| 11 | Secure secrets and credential management                              | Secrets Manager / AgentCore Identity    |
| 12 | Memory and tenant isolation                                           | AgentCore Memory / Application controls |
| 13 | Centralized audit and runtime monitoring                              | CloudTrail / CloudWatch / Dynatrace     |
| 14 | Vulnerability and IaC scanning                                        | Inspector / Checkov / Terraform         |
| 15 | Continuous compliance monitoring                                      | Security Hub / AWS Config               |

AWS specifically documents AgentCore controls for VPC runtime configuration, gateway authorization, KMS encryption, browser network isolation and session recording.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

AWS Security Hub+1



## 5. Suggested ownership model

| Team                    | Responsibility                                        |
| ----------------------- | ----------------------------------------------------- |
| Cloud Platform          | IAM, networking, encryption, Terraform modules        |
| AI Platform             | Model governance, Guardrails, AgentCore configuration |
| Cybersecurity           | Security policies, risk assessment, threat detection  |
| Application teams       | Agent logic, data access and tool authorization       |
| Enterprise Architecture | Standards, reference architecture and exceptions      |
| GRC / Compliance        | NIST mapping, evidence and compliance assessment      |

Final architectural recommendation: Use NIST CSF 2.0 as the overarching security control taxonomy, NIST AI RMF for AI-specific risk governance, and AWS Security Hub AI Security Best Practices as the technical implementation baseline.

This gives you a defensible framework for security reviews, Terraform enforcement, compliance reporting and eventually standardizing the same controls across AWS Bedrock AgentCore and Azure AI Foundry.

Useful references:

- [AWS Security Hub – AgentCore controls](https://docs.aws.amazon.com/securityhub/latest/userguide/bedrockagentcore-controls.html?utm_source=chatgpt.com)
- [AWS Security Reference Architecture for Generative AI](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture-generative-ai/bedrock-integration.html?utm_source=chatgpt.com)
- [AWS Agentic AI security guidance](https://builder.aws.com/content/3GvGFpW4zMzdjtOYwfUGpSDJnT4/secure-your-ai-agents-on-aws-part-1-inputs-identity-and-human-oversight?utm_source=chatgpt.com)
- [AWS AI Security Best Practices standard](https://aws.amazon.com.cdn.amazon.com/about-aws/whats-new/2026/06/aws-security-hub-cspm-ai-security/?utm_source=chatgpt.com)
