# Enterprise AI Agent Security & Governance Framework

AWS Bedrock AgentCore | Azure AI Foundry | Microsoft Copilot Studio | Bespoke Agent Runtimes



Enterprise architecture / production readiness

Multi-cloud security


One particularly important architectural decision is that not using AWS AgentCore Identity does not mean identity management is absent. It means you must explicitly design the integration between Entra ID, AWS IAM, AgentCore runtime, downstream resources and tool identities.

I would also establish one important distinction:

- Authentication: Who or what is calling the agent?
- Authorization: What is that caller or agent allowed to do?
- Delegation: Is the agent acting as itself or exercising permissions on behalf of a human?
- Execution identity: Which identity does the actual runtime use when calling AWS, Azure, APIs, databases or tools?

These four concepts must not be treated as interchangeable.

## 1. Target architecture and security boundaries

[AWS AgentCore vs Azure AI Foundry for MCP | Explore Agentic](https://images.openai.com/static-rsc-4/tZ2d4RaNsH0N4bOvogNfC5k5dI_y_j3aozRnvx3lFgn4N6zrMAHi5WBF8nGi2FGawdoy0L3BAmmTCdGFSFdaRjBXqhx3eqD0E9aeL0d-FettpO_kiK2xoQCXndnOs95UzIqJcqEwFeahkDa2KMG9cIGk9Ig_S-OMZ8LdOjLs6_A?purpose=inline)

[exploreagentic.ai](https://exploreagentic.ai/insights/aws-agentcore-vs-azure-ai-foundry/?utm_source=chatgpt.com)

I would propose the following logical architecture:

```
                Users / Applications
                         |
                         v
                  Microsoft Entra ID
                User Auth / Agent SPN
                Agent ID / Token Claims
                         |
                         v
               Enterprise Agent Entry
             API Gateway / Agent Endpoint
                         |
                         v
             Agent Authentication & Policy
                         |
             +-----------+-----------+
             |                       |
             v                       v
       AWS AgentCore           Azure AI Foundry
             |                       |
             +-----------+-----------+
                         |
                 Agent Execution Layer
                         |
           +-------------+-------------+
           |             |             |
           v             v             v
       Kong AI        MCP Servers    Enterprise APIs
       Gateway        / A2A Tools    / Databases
           |
           v
     Approved LLM Providers
     Bedrock / Azure / Other
                         |
                         v
                 Data & Actions

       Dynatrace: End-to-end observability
       Agent Registry: Governance and inventory
       Security Platform: SIEM / SOC / Incident Response
       Policy Engine: Authorization / Guardrails
```

This is a logical architecture, not a prescribed deployment topology. For example, Kong may be reached through a private network connection, and the agent's tool calls may follow a separate path from its LLM calls.

Critical architectural principle: Kong should be the mandatory enforcement point for LLM traffic, but it should not be assumed to secure every agent interaction. Tool execution, data access, MCP, A2A, agent ingress and cloud resource access require independent authorization and network controls.

Also, Dynatrace is an observability platform, not an authorization engine or a substitute for an audit/SIEM platform.

# 2. Workshop area 1 – Agent onboarding and governance

The first objective is to prevent uncontrolled agent creation and establish an accountable lifecycle from request to retirement.

### 2.1 Comprehensive workshop questions

| ID     | Questions to ask                                           | Recommended solution / expected outcome                                                                                  |
| ------ | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| ONB-01 | Who can request an agent?                                  | Define authorized requesters: application owners, product owners, developers and platform teams.                         |
| ONB-02 | Who sponsors and accepts business accountability?          | Require a named business sponsor and technical owner.                                                                    |
| ONB-03 | Who approves an agent for production?                      | Establish application owner, security, data owner and platform approval based on risk.                                   |
| ONB-04 | What agent types require different onboarding paths?       | Categorize bespoke, managed platform, SaaS, low-code and autonomous agents.                                              |
| ONB-05 | Do all agents require the same security assessment?        | Introduce risk-based onboarding with standard, elevated and restricted pathways.                                         |
| ONB-06 | What determines fast-track versus enhanced review?         | Evaluate data sensitivity, autonomy, external connectivity, write permissions, regulated data and business impact.       |
| ONB-07 | What information must be captured before provisioning?     | Capture use case, owner, sponsor, environment, runtime, model, data sources, tools, permissions and budget.              |
| ONB-08 | What happens after approval?                               | Automatically provision identity, registry entry, approved runtime, Kong policies, observability and secrets references. |
| ONB-09 | How are development, test and production agents separated? | Separate environments, identities, credentials, policies and deployment pipelines.                                       |
| ONB-10 | What happens to rejected or abandoned requests?            | Maintain rejection reasons, expiration, cleanup and audit history.                                                       |
| ONB-11 | How are proof-of-concept agents promoted to production?    | Require production-readiness assessment, security testing, owner confirmation and approval.                              |
| ONB-12 | Can developers create agents outside the approved process? | Detect shadow agents through cloud inventory, Entra applications, Kong traffic and platform inventories.                 |
| ONB-13 | Are agents allowed to create other agents?                 | Require explicit delegation, parent-child ownership, quotas and approval for agent spawning.                             |
| ONB-14 | How are third-party or SaaS agents onboarded?              | Require vendor security assessment, data processing review, identity integration and contractual controls.               |
| ONB-15 | What happens when an agent is no longer required?          | Implement formal decommissioning, credential revocation, endpoint removal and data retention.                            |

### 2.2 Recommended onboarding workflow

[Expediting Cloud Services Integration for Maximizing Growth & Fostering Innovation](https://images.openai.com/static-rsc-4/L1BOk2rNgMh6WyfRv1in0tGsitVRpPaUozL7Nq5AI14J-NVCkaekjXa5ER_aHHd3TVS3aidYEtpXrGvLOf7mn1lOowMCwiiIbXBk0ZvMUbvtXgUHaNKjmlyx06qUnUnS7LA3OpNFeztALj1oFo7ttTFLHxbjiYEfqquYMZgKcRg?purpose=inline)

[letsbloom.io](https://www.letsbloom.io/blog/accelerating-cloud-service-onboarding-for-optimal-growth-and-innovation/?utm_source=chatgpt.com)

| Stage          | Automated activity                                       |
| -------------- | -------------------------------------------------------- |
| Request        | Register agent request and business purpose              |
| Classification | Determine risk, data classification and autonomy         |
| Assessment     | Evaluate identity, security, privacy and architecture    |
| Approval       | Route to appropriate business and technical approvers    |
| Provisioning   | Create identities, runtime configuration and policies    |
| Registration   | Create agent registry record and unique ID               |
| Deployment     | Deploy through approved IaC and CI/CD                    |
| Validation     | Verify controls, connectivity and observability          |
| Production     | Enable approved traffic and operational monitoring       |
| Retirement     | Revoke access, remove resources and retain audit records |

### 2.3 Risk-based onboarding model

I would avoid treating every agent equally.

| Risk tier | Example                                                                    | Required approval                                                                    |
| --------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Low       | Read-only internal knowledge assistant                                     | Standard platform approval                                                           |
| Medium    | Agent accessing internal APIs and business data                            | Application owner and security review                                                |
| High      | Agent updating cloud resources or financial/business records               | Security, data owner and business approval; human approval for consequential actions |
| Critical  | Autonomous agent with privileged access or external execution capabilities | Enhanced architecture, security, privacy and risk approval; restricted deployment    |

Important workshop decision: Does the organization approve the agent once, or approve the combination of agent + identity + tools + data + model + runtime?

My recommendation is to approve the complete execution profile, not just the agent application.

# 3. Workshop area 2 – Identity and access management

Highest-priority security domain

This is arguably the most important workshop discussion because you are using Entra ID across two cloud platforms but not using AWS AgentCore Identity.

I would explicitly separate identity into five layers.

## 3.1 Five identity layers

| Layer            | Identity                                                    | Responsibility                                                |
| ---------------- | ----------------------------------------------------------- | ------------------------------------------------------------- |
| Human identity   | Entra user                                                  | Authenticates the person using the agent                      |
| Agent identity   | Entra Agent ID or service principal                         | Represents the agent as a logical entity                      |
| Runtime identity | AWS IAM role / Azure managed identity                       | Allows the agent to access its hosting environment            |
| Tool identity    | Entra SPN, managed identity, OAuth identity or AWS IAM role | Allows access to MCP servers, APIs, databases and other tools |
| Model identity   | Kong-controlled provider credentials                        | Authenticates to approved LLM providers                       |

These identities should not automatically share permissions.

For example, an agent running in AWS should not receive broad Azure subscription access simply because it has a valid Entra service principal.

## 3.2 Comprehensive identity workshop questions

| ID    | Questions to ask                                                                | Recommended solution                                                                                                                     |
| ----- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| ID-01 | When does an agent act as itself versus on behalf of a user?                    | Define autonomous and delegated execution modes separately.                                                                              |
| ID-02 | Are we using Entra Agent ID, application registration/SPN, or managed identity? | Define supported identity patterns for each runtime.                                                                                     |
| ID-03 | Does every production agent have a unique identity?                             | Require unique agent identity for production agents. Avoid shared identities.                                                            |
| ID-04 | How is the agent authenticated when invoking AgentCore?                         | Configure AgentCore inbound JWT authentication using Entra-issued tokens, or a tightly controlled SigV4 invocation model.                |
| ID-05 | How is the agent authenticated when invoking Azure AI Foundry?                  | Use supported Entra authentication and runtime-specific authorization.                                                                   |
| ID-06 | How do we distinguish a human token from an agent token?                        | Validate issuer, audience, client ID, subject, scopes, roles and token type.                                                             |
| ID-07 | How is user identity propagated through multiple agents?                        | Define a trusted delegation mechanism and maintain the initiating user context.                                                          |
| ID-08 | Can an agent obtain another agent's permissions?                                | Prevent implicit privilege inheritance. Use explicit delegation and scoped token exchange.                                               |
| ID-09 | How are AWS permissions granted to an agent running in AWS?                     | Assign a dedicated IAM execution role with resource-scoped policies.                                                                     |
| ID-10 | How does an AWS agent access Azure resources?                                   | Use Entra workload identity federation where supported, or a controlled OAuth client-credential flow with certificate-based credentials. |
| ID-11 | How does an Azure agent access AWS resources?                                   | Use AWS IAM OIDC federation with tightly restricted trust policies where appropriate.                                                    |
| ID-12 | How are model, data, API, tool, MCP and A2A permissions granted?                | Define separate authorization policies for each resource category.                                                                       |
| ID-13 | Who approves access to sensitive data?                                          | Data owner approval and data classification-based access policies.                                                                       |
| ID-14 | How is least privilege established?                                             | Start with deny-by-default and grant only explicitly approved permissions.                                                               |
| ID-15 | How are permissions periodically reviewed?                                      | Conduct automated access reviews and periodic owner certification.                                                                       |
| ID-16 | What happens when an agent sponsor leaves?                                      | Transfer ownership, revalidate sponsorship and suspend if no accountable owner exists.                                                   |
| ID-17 | What happens when an agent changes runtime or platform?                         | Reassess identity, permissions, network boundaries and approval.                                                                         |
| ID-18 | Can an agent use human credentials or access tokens directly?                   | Prohibit credential collection through prompts, files or agent memory.                                                                   |
| ID-19 | How are credentials rotated and revoked?                                        | Use managed secrets, automated rotation and centralized revocation procedures.                                                           |
| ID-20 | Who can immediately suspend an agent?                                           | Provide emergency suspension to the platform security team and designated incident responders.                                           |

## 3.3 Critical discussion: Entra Agent ID versus SPN

This needs a deliberate architecture decision.

| Consideration           | Traditional Entra SPN                                   | Entra Agent ID                                                 |
| ----------------------- | ------------------------------------------------------- | -------------------------------------------------------------- |
| Primary representation  | Application/service principal                           | Agent-specific identity construct                              |
| Workload authentication | Client credentials, certificates, federated credentials | Agent identity capabilities and supported authentication flows |
| Lifecycle               | Application registration lifecycle                      | Agent identity lifecycle                                       |
| Delegation              | OAuth and supported token flows                         | Agent-specific identity and delegation capabilities            |
| Best fit                | Conventional service-to-service authentication          | Agent-aware identity management and governance                 |

My recommendation:

- Use Entra Agent ID where its lifecycle and platform integration capabilities are supported.
- Use dedicated SPNs for platforms and integrations that require conventional OAuth workload authentication.
- Do not create one common SPN for all agents.
- Make the identity-to-agent-registry relationship mandatory.

An agent's identity should be traceable to its registry record, business owner and deployment.

## 3.4 Critical discussion: How to secure AgentCore without AgentCore Identity

This deserves its own workshop session.

AWS AgentCore supports inbound JWT authentication through an external OIDC identity provider. Microsoft Entra ID can therefore be used as the identity provider without requiring AgentCore Identity to manage the inbound authentication model.

The recommended approach:

[AWS AgentCore Access Control with Azure Entra ID: A Unified OAuth 2.0 Guide for MCP Servers and Deployed Agents | by Arpan Das | May, 2026 | Medium](https://images.openai.com/static-rsc-4/m0SyOKb_Uelin3R5kS4sS9Mo8bBIp8kCO7CiOq1Kn_lak3C3gbyCKrjtwZmRl1UK2GnMj2FKsBHanYQXlH1MYcNaBxwf9AwQcO_TWHf-4Vt-vBQsWoPwM5QYn9ftbjgWJfK_0GmnN6fInLEGv1xdzK8V5iTlspZQsqL6UUdVcP8?purpose=inline)

[medium.com](https://medium.com/%40dasarpan67/aws-agentcore-access-control-with-azure-entra-id-a-unified-oauth-2-0-623997c7601a?utm_source=chatgpt.com)

1. The user or calling application authenticates through Entra ID.
2. Entra issues an access token for the intended AgentCore audience.
3. The calling application sends the bearer token to the AgentCore runtime.
4. AgentCore validates the JWT issuer, signature, audience, permitted client and configured claims/scopes.
5. The agent executes using its dedicated AWS IAM execution role.
6. AWS IAM controls access to AWS services and resources.
7. For Azure resources, the agent obtains a separately authorized Entra access token using an approved workload identity mechanism.

AWS documentation supports external OIDC providers for JWT inbound authentication.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



Important distinction: AgentCore's JWT inbound authorizer authenticates incoming requests. It does not automatically provide all the outbound delegated credential management capabilities of AgentCore Identity.

If you are not using AgentCore Identity, you must design alternatives for:

- User-delegated OAuth flows.
- Workload-to-workload authentication.
- Third-party API credential management.
- Token acquisition and caching.
- Credential rotation.
- Identity propagation to MCP servers.
- Revocation and audit trails.

### Specific questions to challenge the architecture team

1. Are we passing the original Entra access token into the agent, or exchanging it for a downstream token?
2. Is the token audience intended for the agent, Kong or downstream API?
3. Are we using the same SPN for agent authentication and tool authentication?
4. How do we prevent a compromised agent from reusing its execution credentials?
5. Can an agent access another agent's runtime or memory?
6. How do we implement user-level authorization when an agent uses a service principal?
7. How do we revoke an agent's access immediately without waiting for token expiry?
8. Are AWS IAM roles scoped to individual agents or shared across an entire application team?

Recommended decision: Every agent should have a dedicated execution identity, with explicit separation between inbound identity, runtime identity and downstream tool identity. Use short-lived credentials and resource-level permissions wherever possible.

# 4. Workshop area 3 – Runtime security

The objective is to establish common controls regardless of where the agent runs.

## 4.1 Platform-independent security baseline

| Security domain        | AWS AgentCore                                       | Azure AI Foundry                                        | Copilot Studio / Bespoke                                      |
| ---------------------- | --------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------- |
| Inbound authentication | JWT / IAM SigV4                                     | Entra authentication                                    | Entra authentication / application-specific                   |
| Workload identity      | AWS IAM role                                        | Managed identity / agent identity where supported       | Entra workload identity                                       |
| Authorization          | IAM, resource policies and application policies     | Azure RBAC and application authorization                | Environment, connector and application policies               |
| LLM access             | Kong                                                | Kong                                                    | Kong where integration architecture supports enforced routing |
| Tool access            | IAM, OAuth, API authorization                       | Entra RBAC, OAuth and API authorization                 | Connector and API authorization                               |
| MCP access             | Gateway and MCP-level authorization                 | MCP integration and authorization                       | Controlled connector/MCP integration                          |
| Secrets                | AWS Secrets Manager                                 | Azure Key Vault                                         | Approved enterprise secret store                              |
| Network                | VPC, security groups, endpoints and egress controls | VNet integration, private endpoints and egress controls | Platform-specific network capabilities                        |
| Observability          | Dynatrace / CloudWatch                              | Dynatrace / Azure Monitor                               | Dynatrace integration where supported                         |
| Runtime lifecycle      | IaC and deployment pipeline                         | IaC and deployment pipeline                             | Environment governance and managed deployment                 |

The exact capabilities and enforcement mechanisms vary by product version and deployment model. Do not assume that a common control has an identical implementation across platforms.

## 4.2 Runtime workshop questions and solutions

| ID    | Questions to ask                                               | Recommended solution                                                                                |
| ----- | -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| RT-01 | Which controls are mandatory across every runtime?             | Establish a common enterprise security baseline.                                                    |
| RT-02 | Where is inbound authentication enforced?                      | At the agent entry point and runtime, not just at the frontend.                                     |
| RT-03 | Where is authorization enforced?                               | At runtime, API, tool and data-resource boundaries.                                                 |
| RT-04 | Can an agent bypass Kong and call an LLM directly?             | Enforce network egress restrictions and provider allowlisting.                                      |
| RT-05 | How are model endpoints approved?                              | Maintain an approved model/provider catalog.                                                        |
| RT-06 | How are tools approved and registered?                         | Maintain an approved tool catalog with owner, permissions and security assessment.                  |
| RT-07 | How are MCP servers authenticated?                             | Use authenticated transport, scoped authorization and individual server identities.                 |
| RT-08 | How is A2A communication secured?                              | Authenticate both agents, authorize each operation and validate delegation context.                 |
| RT-09 | How are secrets accessed?                                      | Runtime retrieves secrets through its own workload identity; never expose secrets to model context. |
| RT-10 | How is network access controlled?                              | Default-deny outbound access, private connectivity and domain/IP allowlisting.                      |
| RT-11 | How do we stop infinite agent loops?                           | Configure maximum steps, tool-call limits, token budgets, timeouts and recursion limits.            |
| RT-12 | How do we handle model outages?                                | Controlled retries, circuit breakers, fallback models and graceful degradation.                     |
| RT-13 | How do we handle tool failures?                                | Timeout, retry with backoff, idempotency and failure isolation.                                     |
| RT-14 | Can agents execute arbitrary code?                             | Sandboxed execution, restricted filesystem, no privileged host access and controlled egress.        |
| RT-15 | Can agents install additional tools or packages dynamically?   | Prohibit uncontrolled runtime modification; use approved deployment pipelines.                      |
| RT-16 | Can agents spawn subagents?                                    | Enforce parent-child identity, permissions, cost and execution limits.                              |
| RT-17 | Who owns runtime rollback?                                     | Assign platform and application owners with defined recovery procedures.                            |
| RT-18 | Who owns the emergency kill switch?                            | Security operations and designated platform operators.                                              |
| RT-19 | How are runtime configurations drift-checked?                  | IaC reconciliation, policy-as-code and continuous compliance scans.                                 |
| RT-20 | Are production and non-production agent environments isolated? | Separate identities, secrets, network paths and data permissions.                                   |

## 4.3 Critical design area: Mandatory Kong routing

Since Kong must sit before every LLM call, this should be an explicit architectural requirement.

[Enterprise AI Gateway for AI Applications  | Kong Inc.](https://images.openai.com/static-rsc-4/6P-o7t-Wl0ctG2P9JzKisnkAs_59hweroO-VfrYLYBNd0GuvX639CT4mY4iuh3xjrCzUuF3po5k8fgOzXSNggVhk0CnFQHoxU8fKPAejudxq0UtduhdhLn8TybO_lQLlqjeEsfbr8dz_b13-wHFIBb2T5UEWXfG7fgjo-wNOd6o?purpose=inline)

[konghq.com](https://konghq.com/products/kong-ai-gateway?utm_source=chatgpt.com)

I would establish the following controls:

| Control             | Expected implementation                                                        |
| ------------------- | ------------------------------------------------------------------------------ |
| Model allowlisting  | Only approved LLM providers and models can be accessed.                        |
| Authentication      | Authenticate agent workload and/or approved caller at the gateway.             |
| Authorization       | Restrict which agent can invoke which model.                                   |
| Rate limiting       | Apply per-agent, per-user and per-application quotas.                          |
| Token budgets       | Set request, context and output-token limits.                                  |
| Cost control        | Enforce budget thresholds and spending alerts.                                 |
| Prompt inspection   | Detect prohibited content and suspicious prompt patterns.                      |
| PII protection      | Redact sensitive information before provider transmission where appropriate.   |
| Response inspection | Apply content and data leakage checks.                                         |
| Provider failover   | Control model failover based on approved provider policies.                    |
| Audit               | Log agent identity, model, request metadata, token usage and policy decisions. |

Kong documents AI-specific controls including prompt and response guards, sanitization, AI rate limiting, model cost management, OAuth-based tool-call authorization and provider failover.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developer.konghq.com\&sz=32)

Kong Docs



### Questions I would challenge the Kong team with

1. Is Kong mandatory for all LLM traffic, including agents running in AWS and Azure?
2. Can an agent invoke Amazon Bedrock or Azure OpenAI directly?
3. How are direct provider endpoints blocked at the network level?
4. Can Kong distinguish Agent A from Agent B?
5. Can we apply model access policies by agent identity?
6. Can we apply different token quotas for different agents?
7. Can we block an agent from accessing a particular model?
8. Does Kong inspect both incoming prompts and outgoing responses?
9. How are prompt injection and sensitive data leakage handled?
10. Does Kong support MCP tool discovery and authorization in our deployed edition?
11. How are retries and failovers prevented from multiplying cost?
12. Can the gateway identify and block an agent that exceeds its budget?
13. How is Kong's own availability protected against becoming a single point of failure?

My recommendation: Establish Kong as the central LLM control plane, but use a separate authorization model for tools and data. Never treat successful LLM gateway authentication as permission to execute an agent's requested action.

# 5. Workshop area 4 – Agent visibility, registry and governance

Enterprise-wide control plane

I would make the Agent Registry a mandatory component of the enterprise architecture.

However, there is an important distinction between an Agent Registry and an Agent Management Platform.

My recommendation is that the registry should act as the authoritative system of record for agent ownership, identity mapping, security posture, lifecycle and governance, while discovering runtime resources from AWS and Azure.

It should not become the runtime execution engine.

## 5.1 What should the Agent Registry be?

| Capability                      | Should the registry provide it?            |
| ------------------------------- | ------------------------------------------ |
| Agent catalog                   | Yes                                        |
| Agent ownership and sponsorship | Yes                                        |
| Agent identity mapping          | Yes                                        |
| Runtime inventory               | Yes                                        |
| Model and provider inventory    | Yes                                        |
| Tool and MCP inventory          | Yes                                        |
| Data source mapping             | Yes                                        |
| Security posture                | Yes                                        |
| Lifecycle and approval records  | Yes                                        |
| Compliance dashboard            | Yes                                        |
| Agent deployment orchestration  | Integrate with CI/CD and IaC               |
| Runtime execution               | No                                         |
| Centralized policy enforcement  | Integrate with policy engines and gateways |

### 5.2 Comprehensive registry workshop questions

| ID     | Questions to ask                                                                          | Recommended solution                                                                                     |
| ------ | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| REG-01 | Is the registry a catalog, system of record, orchestration point or governance dashboard? | Define it as the authoritative governance and inventory system.                                          |
| REG-02 | Is every production agent required to be registered?                                      | Make registration mandatory before production deployment.                                                |
| REG-03 | What is the unique identifier for an agent?                                               | Generate an immutable enterprise Agent ID.                                                               |
| REG-04 | Which fields are authoritative versus automatically discovered?                           | Define ownership and source-of-truth rules for every attribute.                                          |
| REG-05 | How is the agent linked to its Entra identity?                                            | Maintain Agent ID, SPN object ID, application ID and supported Agent ID references.                      |
| REG-06 | How is the agent linked to its AWS IAM role?                                              | Store AWS account, execution role ARN, runtime ARN and environment.                                      |
| REG-07 | How is the agent linked to Azure resources?                                               | Store subscription, resource group, Foundry project, agent resource and managed identity.                |
| REG-08 | How are models and providers linked?                                                      | Capture model name, version, provider, Kong route and approved model policy.                             |
| REG-09 | How are tools and MCP servers linked?                                                     | Maintain tool inventory, endpoint, owner, identity, permissions and risk classification.                 |
| REG-10 | How are data sources linked?                                                              | Capture data owner, classification, access mode, region and retention requirements.                      |
| REG-11 | How are budget and usage linked?                                                          | Integrate Kong token/cost metrics with cloud billing and application budgets.                            |
| REG-12 | What changes trigger reapproval?                                                          | Define material-change rules for permissions, models, tools, data and runtime.                           |
| REG-13 | What triggers recertification?                                                            | Schedule periodic ownership and access reviews.                                                          |
| REG-14 | How do we identify shadow agents?                                                         | Reconcile discovered cloud resources, Entra applications and Kong traffic against registry records.      |
| REG-15 | How do we identify dormant agents?                                                        | Track last invocation, last successful execution, last deployment and business owner confirmation.       |
| REG-16 | What happens if an agent is discovered but not registered?                                | Flag as ungoverned, alert its owner and quarantine or suspend based on risk.                             |
| REG-17 | How are agent versions tracked?                                                           | Maintain immutable deployment versions and configuration hashes.                                         |
| REG-18 | Can one business application have multiple agents?                                        | Support parent application and individual agent relationships.                                           |
| REG-19 | Can one agent run on multiple platforms?                                                  | Support a logical agent with platform-specific deployment records, if genuinely the same governed agent. |
| REG-20 | Who can modify registry information?                                                      | Use role-based access, approvals and audit logging.                                                      |

## 5.3 Recommended Agent Registry data model

I would propose the following entities.

Enterprise Agent ID

Immutable logical identity and governance record

Ownership

Sponsor, owner, business unit, application

Identity

Entra Agent ID, SPN, AWS IAM role, managed identity

Runtime

AgentCore, Foundry, Copilot, bespoke

Models

Provider, model, version, Kong route

Tools and A2A

MCP servers, APIs, other agents

Data

Data sources, classification, permissions

Security posture

Risk, findings, approvals, compliance

Operations

Usage, cost, health, deployment, last activity

Lifecycle and governance

Requested → Assessed → Approved → Provisioned → Active → Suspended → Retired

### 5.4 Which information should be authoritative?

| Attribute                  | Source of truth                             |
| -------------------------- | ------------------------------------------- |
| Business sponsor           | Agent Registry / business approval workflow |
| Technical owner            | Agent Registry                              |
| Agent identity             | Entra ID                                    |
| AWS execution role         | AWS IAM                                     |
| Azure managed identity     | Entra ID / Azure resource configuration     |
| Runtime configuration      | AWS AgentCore / Azure Foundry               |
| Model routing              | Kong                                        |
| Tool permissions           | Resource authorization system               |
| Data classification        | Enterprise data governance platform         |
| Runtime telemetry          | Dynatrace                                   |
| Deployment version         | CI/CD and IaC                               |
| Cost and token consumption | Kong and cloud billing                      |
| Security findings          | Security platform / SIEM                    |

Important: Do not make the registry a manually maintained spreadsheet. Use automated collectors, API integrations, event-driven updates and reconciliation jobs.

### 5.5 Registry changes that should trigger governance

I would define the following as material changes:

- New model or LLM provider.
- Model version upgrade.
- New MCP server or API tool.
- New A2A relationship.
- New data source or classification increase.
- New permissions or privilege escalation.
- Runtime migration from AWS to Azure or vice versa.
- Change in agent autonomy.
- Change from read-only to write-enabled operations.
- Change in network connectivity.
- Change in identity or service principal.
- Change in business sponsor or technical owner.

These changes should trigger risk-based reassessment rather than automatically forcing a complete approval process for every minor configuration update.

# 6. Workshop area 5 – Monitoring, observability and incident management

Dynatrace integration

Dynatrace should provide operational visibility into the agent execution lifecycle, not just CPU, memory, latency and HTTP errors.

The goal is to understand what an agent did, why it did it, which resources it accessed and whether the action was successful and authorized.

## 6.1 Comprehensive monitoring workshop questions

| ID     | Questions to ask                                                                       | Recommended solution                                                                   |
| ------ | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| MON-01 | Can we trace a request from the user through the agent, model, tools and final action? | Implement distributed tracing with OpenTelemetry context propagation.                  |
| MON-02 | Can we distinguish different agents?                                                   | Use immutable Agent ID as a telemetry attribute.                                       |
| MON-03 | Can we identify which user initiated an action?                                        | Record a privacy-safe user identifier and trusted identity context.                    |
| MON-04 | Can we identify the LLM model and provider used?                                       | Capture provider, model, version and Kong route.                                       |
| MON-05 | Can we capture tool execution details?                                                 | Capture tool name, execution status, duration and authorization decision.              |
| MON-06 | Can we identify failed or unauthorized tool calls?                                     | Emit security events for denied actions, abnormal failures and repeated attempts.      |
| MON-07 | Can we identify prompt injection attempts?                                             | Integrate prompt security signals and content guardrail results.                       |
| MON-08 | Can we detect infinite loops?                                                          | Monitor repeated tool sequences, excessive agent steps and session duration.           |
| MON-09 | Can we monitor token consumption and cost?                                             | Correlate Kong usage with agent ID, model and application.                             |
| MON-10 | Can we detect model outages?                                                           | Monitor provider health, error rates, timeouts and circuit-breaker events.             |
| MON-11 | Can we detect abnormal agent behavior?                                                 | Use baselines for unusual access, tool usage, model calls and data volume.             |
| MON-12 | What status changes flow back into the registry?                                       | Feed health, risk, suspension, ownership and lifecycle events into the registry.       |
| MON-13 | Which events trigger alerts?                                                           | Define severity-based event and alert policies.                                        |
| MON-14 | Which events trigger throttling or suspension?                                         | Integrate policy enforcement with Kong and runtime control APIs.                       |
| MON-15 | Can an operator immediately terminate an agent?                                        | Provide a centrally controlled emergency kill-switch workflow.                         |
| MON-16 | Who receives the alert?                                                                | Define application, platform, security and SOC ownership.                              |
| MON-17 | How long are traces and audit records retained?                                        | Define retention based on regulatory, privacy and incident investigation requirements. |
| MON-18 | Are prompts and responses stored?                                                      | Apply data minimization, masking and configurable retention.                           |
| MON-19 | Can we reconstruct an agent's actions during an incident?                              | Maintain immutable audit events, trace identifiers and tool/action records.            |
| MON-20 | How are dormant or unhealthy agents detected?                                          | Combine activity metrics, deployment state and registry ownership.                     |

## 6.2 Recommended end-to-end tracing model

This is one of the most important architecture requirements to establish.

[LLM Observability in Production: Tracing & Evaluation](https://images.openai.com/static-rsc-4/eumc74Zv12Wf_nc1RlcPU9dukVY6gW5NKmYvKzkc_Qw0B-uDDgCzo3MZlFRwyvuUpq6yvJUyE2GTvm7lc0qwl3Dxp-9yRGu64hkCdI_keuB4qryMm-fWFyst5z0oIUUfFxPMfsfGa4k9_fyvst2_RN4VtOqfAtLMFyuNrHEYvrM?purpose=inline)

[cloudrps.com](https://cloudrps.com/blog/llm-observability-production-tracing/?utm_source=chatgpt.com)

An example execution:

```
User Request
    |
    v
Entra Authentication
    |
    v
Agent Invocation
    |
    +---- Agent ID: AGT-001
    |
    v
Agent Runtime
    |
    +---- LLM Request
    |       |
    |       v
    |    Kong Gateway
    |       |
    |       v
    |    Azure OpenAI
    |
    +---- Tool Invocation
    |       |
    |       v
    |    MCP Server
    |       |
    |       v
    |    Enterprise API
    |
    +---- Data Retrieval
    |
    v
Action / Business Transaction
    |
    v
Final Outcome
```

Every span should preserve the appropriate trace context and link to the same logical execution.

### Recommended telemetry attributes

| Attribute                    | Purpose                                  |
| ---------------------------- | ---------------------------------------- |
| `agent.id`                   | Unique enterprise agent identifier       |
| `agent.version`              | Deployed version                         |
| `agent.runtime`              | AgentCore / Foundry / Copilot / bespoke  |
| `agent.environment`          | Dev / Test / Prod                        |
| `agent.owner`                | Application or technical owner reference |
| `identity.client_id`         | Calling workload/client identity         |
| `identity.subject_hash`      | Privacy-safe user reference              |
| `llm.provider`               | AWS / Azure / other                      |
| `llm.model`                  | Model name and version                   |
| `kong.route`                 | Approved model route                     |
| `tool.name`                  | Executed tool                            |
| `tool.authorization`         | Allowed / Denied                         |
| `tool.outcome`               | Success / Failure                        |
| `data.classification`        | Data sensitivity category                |
| `security.policy_result`     | Guardrail and authorization outcome      |
| `gen_ai.usage.input_tokens`  | Input token consumption                  |
| `gen_ai.usage.output_tokens` | Output token consumption                 |
| `trace_id`                   | Cross-platform execution correlation     |

Use established OpenTelemetry semantic conventions where available, supplemented with enterprise-specific attributes.

Important privacy consideration: Do not blindly send complete prompts, responses, access tokens, credentials, personal data or sensitive retrieved documents to Dynatrace. Use selective capture, redaction and access-controlled retention.

## 6.3 Define an operational response matrix

| Event                                   | Recommended action                        | Responsible team      |
| --------------------------------------- | ----------------------------------------- | --------------------- |
| Repeated unauthorized tool calls        | Alert and temporarily block the tool      | Security / platform   |
| Excessive token usage                   | Throttle or block through Kong            | AI platform           |
| Prompt injection detected               | Block or quarantine request               | AI security           |
| Suspicious data access                  | Suspend access and investigate            | SOC / data security   |
| Infinite execution loop                 | Terminate execution and alert             | Runtime operations    |
| Model provider outage                   | Controlled failover                       | AI platform           |
| Agent identity compromised              | Revoke identity and suspend agent         | IAM / SOC             |
| Sponsor leaves organization             | Initiate ownership reassignment           | Business / registry   |
| Unregistered agent detected             | Quarantine or block according to risk     | Platform governance   |
| Production agent inactive beyond policy | Initiate retirement review                | Application owner     |
| New unauthorized model endpoint         | Block egress and create security incident | Network / AI platform |

### 6.4 The emergency kill switch

This should be a mandatory capability, not an optional operational feature.

I would design a centralized suspension workflow that can:

1. Mark the agent as `SUSPENDED` in the registry.
2. Block new invocations at the enterprise ingress.
3. Revoke or disable the agent's workload identity and relevant permissions.
4. Block its Kong model routes.
5. Disable or restrict tool and MCP access.
6. Terminate active sessions where supported.
7. Preserve audit logs and investigation evidence.
8. Notify the application owner, platform owner and SOC.

One important nuance: disabling an Entra service principal alone does not necessarily stop an already-running agent or invalidate every previously issued access token immediately.

Therefore, the kill switch must cover runtime, identity, network and gateway enforcement points.

# 7. Additional mandatory production-readiness areas

The five areas above are necessary, but they are not sufficient to productionize enterprise agents.

I would add the following eight workstreams to the workshop. These are areas that frequently get overlooked when organizations focus primarily on identity, runtime and monitoring.

## 7.1 AI safety, prompt injection and guardrails

Mandatory

This is different from traditional application security. An agent can be authenticated, authorized and technically secure while still making an unsafe decision.

Questions to ask

1. How do we protect agents against direct prompt injection?
2. How do we prevent indirect prompt injection from documents, websites, emails and retrieved content?
3. Can retrieved data influence the agent's system instructions?
4. How do we prevent an agent from executing instructions contained in untrusted data?
5. How do we prevent sensitive information from being returned to unauthorized users?
6. Can guardrails differ by agent risk classification?
7. How do we prevent unsafe tool execution?
8. How do we protect persistent agent memory against poisoning?
9. Can agents override their own system instructions or security policies?
10. How do we evaluate guardrail effectiveness before production?

Recommended solutions

| Control                    | Implementation                                                        |
| -------------------------- | --------------------------------------------------------------------- |
| Prompt injection defense   | Input screening, prompt separation and instruction hierarchy          |
| Indirect injection defense | Treat external documents and retrieved content as untrusted data      |
| Sensitive data protection  | PII detection, redaction and DLP                                      |
| Output validation          | Response inspection and structured output validation                  |
| Tool execution protection  | Allowlisted tools and schema validation                               |
| Memory protection          | Source validation, provenance, access control and poisoning detection |
| Dangerous actions          | Explicit authorization and human approval                             |
| Guardrail testing          | Adversarial testing and continuous evaluations                        |

A critical design principle: The LLM must never be the final authority for determining whether it is allowed to perform an action.

The actual authorization decision must be enforced outside the model.

## 7.2 Tool, MCP and A2A security

Mandatory

I would dedicate a separate workshop to this because MCP and agent-to-agent communication significantly expand the attack surface.

Questions to ask

1. Who is allowed to publish an MCP server?
2. Who approves an MCP server before it becomes available?
3. Does each MCP server have its own identity?
4. Does each tool have a separate permission scope?
5. Can agents dynamically discover and invoke tools?
6. Can one agent invoke another agent without explicit authorization?
7. How is the original user identity propagated across agents?
8. How do we prevent confused-deputy attacks?
9. Can an agent modify tool descriptions or schemas at runtime?
10. How are tool versions and vulnerabilities managed?
11. Can a compromised MCP server access other agents?
12. Are MCP and A2A endpoints restricted to approved network locations?

Recommended solutions

- Establish an enterprise MCP server registry.
- Use authenticated connections and explicit authorization for every tool.
- Use separate read and write scopes.
- Restrict dynamic tool discovery to approved catalogs.
- Maintain tool owner, version, endpoint, identity and risk metadata.
- Require explicit trust relationships between agents.
- Validate A2A caller identity, audience and delegated permissions.
- Prevent unrestricted agent-to-agent communication.
- Use API schemas and input validation to constrain tool arguments.
- Monitor tool invocation patterns and anomalous behavior.

## 7.3 Data security, privacy and RAG governance

Mandatory

RAG introduces another important security boundary: the agent must only retrieve information that the invoking user or approved workload is authorized to access.

Questions to ask

1. What data classification can each agent access?
2. Are sensitive data sources allowed for external model providers?
3. Does Kong perform appropriate PII and sensitive data inspection?
4. How is authorization enforced at retrieval time?
5. Are vector databases partitioned by application, user or business domain?
6. Can an agent retrieve another user's conversation history?
7. How are embeddings protected?
8. How are documents and data sources classified?
9. How do we manage data retention and deletion?
10. Can retrieved data be used for model training?
11. How is data residency enforced across AWS and Azure?
12. How do we prevent cross-tenant data leakage?

Recommended solutions

| Area                | Control                                                         |
| ------------------- | --------------------------------------------------------------- |
| Data classification | Mandatory classification before onboarding                      |
| RAG authorization   | Retrieval-time authorization and ACL filtering                  |
| Vector databases    | Tenant and application isolation                                |
| Encryption          | TLS and approved KMS/Key Vault-managed encryption               |
| Data leakage        | DLP and sensitive data redaction                                |
| Data residency      | Approved regions and private network paths                      |
| Data retention      | Retention and deletion policies                                 |
| Data provenance     | Source document, owner and retrieval audit trail                |
| Training usage      | Explicit approval of provider data usage and retention settings |

One question I would strongly challenge the team with:

If a user cannot access a document directly, how can we guarantee that the agent cannot retrieve and disclose that same document on their behalf?

This should be demonstrated through a negative authorization test, not simply answered through architecture documentation.

## 7.4 Secure SDLC, DevSecOps and IaC

Mandatory

Agents should be provisioned through a controlled software delivery pipeline, not manually deployed by developers.

Questions to ask

1. Are agents deployed using Terraform or another approved IaC framework?
2. Are agent runtime configurations version-controlled?
3. Are model, tool and MCP configurations part of the deployment artifact?
4. Are container images and dependencies scanned?
5. Are agent prompts and system instructions version-controlled?
6. Are changes to tool permissions subject to code review?
7. Are security policies enforced before deployment?
8. How are vulnerabilities in agent frameworks and SDKs identified?
9. How do we prevent secrets from being committed to source control?
10. Can a developer deploy an agent directly to production?
11. How do we perform rollback?
12. Are production deployments signed and traceable to approved source code?

Recommended CI/CD security gates

1. Source code validation

   SAST, dependency scanning, secret scanning and license checks.
2. Infrastructure validation

   Terraform scanning, IAM policy analysis and network policy checks.
3. Agent configuration validation

   Approved model, tools, permissions, prompts and resource limits.
4. AI security testing

   Prompt injection, data leakage, unsafe actions and authorization tests.
5. Approval and deployment

   Security gates, change approval and signed deployment artifacts.
6. Continuous compliance

   Configuration drift detection, runtime policy verification and audit evidence.

## 7.5 Human-in-the-loop and business action controls

This is particularly important for agents that can make changes to enterprise systems.

Questions to ask

1. Which agent actions can be performed autonomously?
2. Which actions require human approval?
3. Can an agent update production infrastructure?
4. Can an agent execute financial transactions?
5. Can an agent delete or modify business records?
6. Who approves high-impact operations?
7. Can the approval be delegated to another agent?
8. How do we prevent an agent from approving its own action?
9. Can approvals expire?
10. Is there an audit record of the proposed action, approval and actual execution?

Recommended action classification

| Action category                        | Required control                                 |
| -------------------------------------- | ------------------------------------------------ |
| Read-only                              | Normal authorization                             |
| Low-impact update                      | Scoped authorization and audit                   |
| Business-critical update               | Human approval                                   |
| Financial transaction                  | Dual approval where required                     |
| Production infrastructure modification | Change approval and execution policy             |
| Destructive action                     | Explicit confirmation and elevated authorization |
| Privileged access modification         | Security approval and privileged access controls |

I would introduce an Agent Action Authorization Framework that classifies tool actions by risk, not simply by the agent's overall risk classification.

For example, the same agent might be allowed to read an AWS Trusted Advisor recommendation autonomously but require approval before modifying a production resource.

## 7.6 Resilience, availability and disaster recovery

Questions to ask

1. What is the availability target for each production agent?
2. What happens if Kong is unavailable?
3. What happens if Entra ID cannot issue or validate tokens?
4. What happens if Dynatrace is unavailable?
5. What happens when the LLM provider experiences an outage?
6. Is cross-region failover required?
7. Can an agent resume an interrupted execution safely?
8. How are duplicate actions prevented during retries?
9. Are agent sessions recoverable?
10. What are the RTO and RPO requirements?

Recommended solutions

- Define SLOs for agent availability, latency and successful completion.
- Implement circuit breakers and bounded retries.
- Use idempotency keys for business transactions.
- Provide approved model failover through Kong.
- Avoid silently switching to models with different security or data residency properties.
- Define graceful degradation when the model or tool is unavailable.
- Define recovery and session expiration behavior.
- Ensure observability outages do not silently disable security controls.
- Test recovery through chaos and failure-injection exercises.

## 7.7 AI evaluation, quality and model governance

An agent may pass every infrastructure security test and still produce unreliable or harmful business outcomes.

Questions to ask

1. Who approves a model for production?
2. How are model versions evaluated?
3. How do we measure accuracy and hallucination rates?
4. How do we evaluate agent tool-selection accuracy?
5. How do we evaluate the quality of agent decisions?
6. Are regression tests run after model or prompt changes?
7. How do we detect model behavior changes?
8. Are agents tested against adversarial inputs?
9. Can the organization reproduce a previous agent execution?
10. Who owns the evaluation datasets and acceptance criteria?

Recommended solutions

- Approved model catalog.
- Model risk assessment.
- Standard evaluation datasets.
- Prompt and agent version control.
- Automated regression tests.
- Red-team testing.
- Human evaluation for high-risk use cases.
- Continuous production quality monitoring.
- Model retirement and upgrade processes.

## 7.8 Compliance, audit and regulatory requirements

Questions to ask

1. Which regulatory obligations apply to agents?
2. Are agents accessing financial, personal or regulated information?
3. Can we demonstrate who approved an agent?
4. Can we demonstrate which permissions it had at a particular point in time?
5. Can we reconstruct a business-critical agent action?
6. How are third-party model providers assessed?
7. Are records retained according to enterprise policies?
8. Are data processing and cross-border transfer requirements satisfied?
9. Can auditors access evidence without obtaining production runtime access?
10. Are security exceptions time-bound and reviewed?

Recommended control frameworks

| Framework                                  | How to use it                           |
| ------------------------------------------ | --------------------------------------- |
| NIST AI RMF / Generative AI Profile        | AI risk governance and trustworthy AI   |
| NIST CSF 2.0                               | Enterprise cybersecurity governance     |
| NIST SP 800-53                             | Security and privacy controls           |
| OWASP Top 10 for Agentic Applications 2026 | Agent-specific threat modeling          |
| ISO 27001                                  | Information security management         |
| ISO 42001                                  | AI management system                    |
| CIS Benchmarks                             | Cloud and infrastructure hardening      |
| MITRE ATLAS                                | AI-specific adversarial threat modeling |

I would use NIST AI RMF as the governance foundation, NIST 800-53 for control mapping and OWASP Agentic Applications for application-level threat modeling.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nist.gov\&sz=32)

NIST+3



# 8. Important architectural decisions specific to your technology stack

This is where I would spend additional time in the workshop because your architecture has three central technologies and multiple execution platforms.

## 8.1 Entra ID – identity architecture decisions

Microsoft Entra Agent ID is worth evaluating rather than assuming traditional SPNs will be sufficient for every agent.

Microsoft documents integration with non-Microsoft platforms, including AWS Bedrock, through mechanisms such as its authentication SDK/sidecar and workload identity federation.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learn.microsoft.com\&sz=32)

Microsoft Learn+1



| Decision                           | Recommendation                                                 |
| ---------------------------------- | -------------------------------------------------------------- |
| Agent identity                     | Prefer dedicated agent identity where supported                |
| Legacy or conventional integration | Dedicated SPN with certificate or federated credentials        |
| Agent-to-agent identity            | Explicitly governed identity and trust relationship            |
| Agent sponsorship                  | Mandatory accountable human sponsor                            |
| Identity lifecycle                 | Automated expiration, inactivity and recertification           |
| User delegation                    | Explicit delegated OAuth flows, not shared service credentials |
| Cross-cloud access                 | Short-lived federated credentials wherever supported           |

An interesting capability to discuss with the Entra team is agent lifecycle governance. Microsoft documents periodic reconfirmation, sponsor requirements and inactivity-based lifecycle policies. However, the lifecycle policies are currently marked as preview, so I would not make them the sole production enforcement mechanism.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learn.microsoft.com\&sz=32)

Microsoft Learn+1



## 8.2 Kong – central LLM governance decisions

I would establish a mandatory Kong policy for every production agent.

An example policy model:

| Agent   | Model access   | Token quota | Data classification | Allowed providers       |
| ------- | -------------- | ----------- | ------------------- | ----------------------- |
| AGT-001 | GPT model A    | 100K/day    | Internal            | Approved Azure provider |
| AGT-002 | Claude model B | 50K/day     | Confidential        | Approved AWS provider   |
| AGT-003 | GPT model C    | 20K/day     | Public              | Approved providers      |

These are illustrative quotas, not recommended defaults.

Kong should enforce the model-level policies, and the registry should maintain the approved relationship between agent, owner and model route.

I would additionally ask:

- Can Kong identify the initiating user and agent independently?
- Can a compromised agent use another agent's Kong credentials?
- Can Kong enforce provider-specific data classification restrictions?
- Are model credentials isolated from individual agents?
- Does Kong expose usage and policy decisions through APIs for registry reconciliation?
- Is the gateway's management plane protected separately from its data plane?

## 8.3 Dynatrace – operational governance decisions

Dynatrace supports AI observability using OpenTelemetry, including agent execution paths, LLM calls, tool use, latency and token consumption.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.dynatrace.com\&sz=32)

Dynatrace Docs+2



I would establish three dashboards:

Dashboard A – Agent operational health

- Active agents.
- Successful versus failed executions.
- Execution latency.
- Model latency.
- Tool failures.
- Runtime availability.
- Agent error rates.

Dashboard B – Security and governance

- Unauthorized tool invocations.
- Prompt injection detections.
- Unapproved model access.
- Abnormal agent behavior.
- Identity failures.
- Agents without owners.
- Unregistered agents.
- Suspended agents.

Dashboard C – Cost and business usage

- Token consumption by agent.
- Model cost by application.
- Cost by business unit.
- Cost per successful execution.
- Tool invocation volume.
- Failed execution cost.
- Budget threshold breaches.

Do not rely on Dynatrace alone for the audit record. Maintain authoritative security and administrative events in your enterprise logging/SIEM platform as well.

# 9. Recommended enterprise control ownership model

One of the most important workshop outcomes should be agreement on who owns each control.

Without clear ownership, controls will exist in architecture documents but may not be implemented or operated.

| Control domain            | Primary owner               | Supporting technology             |
| ------------------------- | --------------------------- | --------------------------------- |
| Agent onboarding          | AI Platform Governance      | Agent Registry                    |
| Business accountability   | Business/Application Owner  | Entra ID / Registry               |
| Agent identity            | IAM Team                    | Entra ID                          |
| AWS runtime permissions   | AWS Cloud Security          | AWS IAM                           |
| Azure runtime permissions | Azure Cloud Security        | Azure RBAC                        |
| Model access              | AI Platform Team            | Kong                              |
| Tool/MCP authorization    | API / AI Security           | Kong and resource authorization   |
| Data access               | Data Security / Data Owners | Data platforms                    |
| Runtime security          | Cloud Platform Team         | AgentCore / Foundry               |
| Secrets management        | IAM / Cloud Security        | Secrets Manager / Key Vault       |
| Network security          | Network Security            | AWS VPC / Azure VNet              |
| Observability             | SRE / Platform Operations   | Dynatrace                         |
| Security monitoring       | SOC                         | SIEM                              |
| AI safety                 | AI Security Team            | Guardrails / evaluation framework |
| CI/CD security            | DevSecOps                   | Terraform / CI/CD                 |
| Lifecycle management      | AI Governance / IAM         | Registry / Entra ID               |
| Incident response         | SOC / Platform Operations   | Central kill switch               |

# 10. Recommended workshop structure

I would not try to cover all these areas in one meeting. Organize this as a structured architecture and security workshop with clear deliverables.

## Suggested workshop agenda

Two-day architecture workshop · Suggested duration

Day 1 – Governance and security architecture

| Session                                      | Duration |
| -------------------------------------------- | -------- |
| Enterprise agent architecture and principles | 45 min   |
| Onboarding and governance                    | 45 min   |
| Identity and access management               | 90 min   |
| Runtime security across platforms            | 75 min   |
| Kong AI Gateway security                     | 45 min   |
| MCP and A2A security                         | 45 min   |

Day 1 outcome

Agreed identity architecture, onboarding model and common runtime security baseline.

Day 2 – Operations and production readiness

| Session                                | Duration |
| -------------------------------------- | -------- |
| Agent Registry and lifecycle           | 60 min   |
| Dynatrace and end-to-end observability | 60 min   |
| AI safety and data security            | 60 min   |
| DevSecOps and deployment controls      | 45 min   |
| Human approval and action governance   | 30 min   |
| Incident management and kill switch    | 30 min   |
| Decisions, gaps and action owners      | 45 min   |

Day 2 outcome

Production security requirements, operational ownership and implementation roadmap.

# 11. The 15 most important questions I would personally challenge the teams with

If I were leading this workshop as the Sr. Agentic Architect, these are the questions I would prioritize. They are designed to uncover architectural gaps rather than simply confirm whether a product feature exists.

| #  | Architecture challenge                                                                               | Why it matters                                           |
| -- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 1  | Does every agent have a unique, governed identity across AWS and Azure?                              | Prevents shared identity and accountability gaps.        |
| 2  | How do we propagate user identity when an agent invokes another agent or tool?                       | Prevents confused-deputy and privilege escalation risks. |
| 3  | Without AgentCore Identity, what is our complete outbound credential management strategy?            | Prevents unmanaged credentials and shared access.        |
| 4  | Can an agent bypass Kong and directly invoke an LLM provider?                                        | Ensures centralized model governance.                    |
| 5  | Can Kong identify the exact agent and enforce agent-specific model permissions and budgets?          | Enables granular AI governance.                          |
| 6  | How do we guarantee that an agent cannot retrieve data the user is not authorized to access?         | Prevents indirect data leakage.                          |
| 7  | Who approves new MCP servers, tools and A2A integrations?                                            | Prevents uncontrolled tool proliferation.                |
| 8  | How do we prevent prompt injection from triggering unauthorized tool execution?                      | Protects against agent-specific attacks.                 |
| 9  | Can we reconstruct an entire execution from user request to final business action?                   | Provides forensic traceability.                          |
| 10 | Is the Agent Registry authoritative, and how do we reconcile it against actual cloud inventory?      | Prevents shadow and orphaned agents.                     |
| 11 | Can we suspend an agent across Entra, Kong, AWS and Azure within a defined incident response SLA?    | Enables effective emergency response.                    |
| 12 | What changes to an agent trigger mandatory security reassessment?                                    | Prevents configuration drift and privilege creep.        |
| 13 | Who approves autonomous actions that modify business-critical systems?                               | Prevents unintended business impact.                     |
| 14 | Are all agents subject to common CI/CD security and AI evaluation gates?                             | Prevents insecure production deployments.                |
| 15 | Can we demonstrate the security posture and compliance of every production agent from one dashboard? | Establishes enterprise-wide accountability.              |

# 12. My recommended implementation priorities

I would divide the implementation into three phases.

Phase 1 – Security foundation

P0

Before production onboarding

- Entra-based identity architecture.
- Dedicated agent identities and execution roles.
- Kong mandatory LLM routing.
- Tool and data authorization.
- Secrets management.
- Network isolation and egress restrictions.
- Agent onboarding and approval workflow.
- Minimum security baseline.

Phase 2 – Governance and operational control

P1

Before scaling enterprise adoption

- Central Agent Registry.
- Automated AWS and Azure inventory.
- Dynatrace end-to-end tracing.
- Agent-specific quotas and budgets.
- MCP and A2A governance.
- Centralized security event monitoring.
- Emergency kill switch.
- Access reviews and lifecycle management.

Phase 3 – Advanced agent governance

P2

Enterprise optimization and continuous assurance

- Automated agent risk scoring.
- AI security testing and red teaming.
- Agent behavior anomaly detection.
- Human-in-the-loop orchestration.
- Automated compliance evidence.
- Model quality and drift monitoring.
- Continuous policy validation.
- Automated retirement and remediation.

# 13. What I would expect as final workshop deliverables

Do not conclude the workshop with only meeting notes. Require the teams to produce these artifacts.

| Deliverable                               | Expected outcome                                            |
| ----------------------------------------- | ----------------------------------------------------------- |
| 1. Enterprise Agent Security Architecture | Approved logical and deployment architecture                |
| 2. Identity Architecture                  | Entra, AWS IAM and Azure identity integration design        |
| 3. Agent Onboarding Framework             | Request, risk assessment, approval and provisioning process |
| 4. Common Security Baseline               | Mandatory controls across all runtimes                      |
| 5. Kong Security Policy                   | Model routing, access, quotas and guardrail requirements    |
| 6. MCP/A2A Security Standard              | Tool authentication and authorization requirements          |
| 7. Agent Registry Data Model              | Authoritative agent inventory and lifecycle schema          |
| 8. Dynatrace Observability Standard       | Trace, metric, log and event requirements                   |
| 9. Incident Response Playbook             | Suspension, containment and recovery procedures             |
| 10. Secure Agent CI/CD Standard           | Deployment security gates and policy-as-code                |
| 11. AI Risk Assessment Template           | Agent-specific security and business risk classification    |
| 12. Production Readiness Checklist        | Go/no-go requirements for production                        |

## 14. Production readiness acceptance criteria

I would establish a minimum go-live checklist. The following is a proposed enterprise baseline, not a claim that these controls are automatically provided by the platforms.

Production readiness tracker

0/16 complete

GOVERNANCE

Business sponsor and technical owner registered

Agent Registry record and lifecycle state established

IDENTITY

Unique agent identity and runtime identity established

Inbound authentication and authorization tested

Outbound API, tool and data permissions approved

GATEWAY

Kong mandatory model routing verified; direct bypass blocked

SECURITY

Secrets and credentials secured

Network egress and private connectivity validated

TOOLS

MCP and A2A access explicitly authorized

AI SAFETY

Prompt injection and data leakage tests passed

MONITORING

Dynatrace tracing and operational alerts verified

OPERATIONS

Token, cost and execution limits configured

Human approval configured for high-impact actions

RESILIENCE

Rollback, kill switch and incident playbook tested

DEVSECOPS

CI/CD security and deployment approval gates passed

COMPLIANCE

Audit logging, retention and privacy requirements satisfied

Reset checklist

I would make successful completion of all applicable P0 controls a prerequisite for production approval. Any exception should have a documented risk owner, compensating control, expiration date and formal acceptance.

# 15. Reference documentation for the workshop

These are useful technical references to distribute to the respective teams before the workshop.

| Area                                 | Official reference                                                                                                                                                                          |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AWS AgentCore inbound authentication | [AgentCore Inbound and Outbound Authentication](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html?utm_source=chatgpt.com)                                    |
| AWS AgentCore security               | [AgentCore Runtime Security Best Practices](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html?utm_source=chatgpt.com)                      |
| AWS AgentCore JWT                    | [JWT Authorizer Configuration](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/inbound-jwt-authorizer.html?utm_source=chatgpt.com)                                            |
| Entra Agent ID                       | [Microsoft Entra Agent ID](https://learn.microsoft.com/en-us/entra/agent-id/?utm_source=chatgpt.com)                                                                                        |
| Entra Agent lifecycle                | [Agent Identity Lifecycle Policies](https://learn.microsoft.com/en-us/entra/id-governance/agent-lifecycle-policies?utm_source=chatgpt.com)                                                  |
| Azure Foundry identity               | [Foundry Agent Identity](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/agent-identity?utm_source=chatgpt.com)                                                                |
| Azure Foundry security               | [Foundry Agent Service](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview?view=foundry\&utm_source=chatgpt.com)                                                            |
| Kong AI Gateway                      | [Kong AI Gateway Security Capabilities](https://developer.konghq.com/ai-gateway/?utm_source=chatgpt.com)                                                                                    |
| Dynatrace AI Observability           | [Dynatrace AI Observability](https://docs.dynatrace.com/docs/observe/dynatrace-for-ai-observability?utm_source=chatgpt.com)                                                                 |
| Dynatrace OpenTelemetry              | [OpenTelemetry Integration](https://docs.dynatrace.com/docs/observe/dynatrace-for-ai-observability/get-started/opentelemetry?utm_source=chatgpt.com)                                        |
| OWASP Agentic Security               | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/?utm_source=chatgpt.com)                                       |
| NIST AI Governance                   | [NIST Generative AI Risk Management Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence?utm_source=chatgpt.com) |

## My final architectural recommendation

If I were accountable for this enterprise architecture, I would establish five non-negotiable principles:

1\. Identity-first architecture: Every agent must have an identifiable owner, a unique identity and a separately governed execution identity. Entra ID should provide the enterprise identity foundation, while AWS IAM and Azure authorization enforce resource access.

2\. Kong as the mandatory LLM control plane: All production LLM traffic must go through approved Kong routes. Direct model access must be prevented through enforceable network and resource policies.

3\. Independent tool authorization: Agent authentication does not grant permission to invoke every tool. Every MCP server, API, database and A2A interaction must enforce its own authorization boundary.

4\. Centralized governance and observability: The Agent Registry provides the authoritative governance view, while Dynatrace provides execution visibility. Neither should be mistaken for the other.

5\. Lifecycle and emergency controls: Every agent must be onboarded, approved, monitored, periodically reviewed and safely retired. Security teams must be able to suspend a compromised agent across the identity, runtime, gateway and tool layers.

The most important architectural gap I would investigate first is the absence of AWS AgentCore Identity. You can absolutely build a secure architecture without using it, but you must explicitly demonstrate how outbound credentials, user delegation, tool authentication, token exchange, rotation and revocation are handled. Inbound Entra authentication alone does not solve those problems.

I would make that the first major architecture decision in the workshop, followed by Kong bypass prevention and the end-to-end kill-switch design.

For the next stage, I would turn this into a senior-leadership workshop PowerPoint with an architecture diagram, 100+ prioritized questions, decision log, RACI and production security control matrix.

🛡️Review agent security posture monthlyTap to set up

