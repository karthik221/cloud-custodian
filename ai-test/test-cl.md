# Securing agents on AgentCore and Foundry with Entra ID, Kong and Dynatrace: workshop question bank

## Framing assumptions to confirm first

- **Entra ID is the only identity plane.** AgentCore and Foundry are runtimes, not identity authorities. Every principal (human, agent, tool, MCP server) resolves to an Entra object.
- **Kong is the single choke point for model traffic.** Direct egress to Bedrock, Azure OpenAI or any other model endpoint is blocked at the network and IAM layers, so Kong can't be bypassed.
- **Dynatrace is the telemetry sink, not the system of record.** The registry is the system of record, and Dynatrace feeds status back into it.
- **The AgentCore Identity gap is the main design problem.** Without its token vault and outbound credential management, you must supply:
  - inbound JWT validation against Entra (AgentCore Runtime and Gateway both support custom JWT authorizers pointed at the Entra OIDC discovery URL)
  - outbound token acquisition (OBO, client credentials or workload identity federation)
  - secret and token storage (Secrets Manager or Key Vault, short TTL, no long-lived keys in agent code)
- **Check Entra Agent ID maturity** (blueprints, agent identities, agent users) before committing. Verify its current GA/preview status and what it supports for non-Microsoft runtimes. Many shops will run SPN/managed identity now with an Agent ID migration path.

---

## 1. Onboarding

| Question | Probe | Possible solution |
|---|---|---|
| **Who can request an agent, and who sponsors it?** | Can anyone request one? Is the sponsor an accountable owner with budget authority? Is there a technical owner as well as a business owner? | Any employee can request. A sponsor must be a named, active Entra user at manager level or above, and a separate technical owner is mandatory. Both are stored as Entra owner attributes and registry fields. Sponsor attestation is required at intake. |
| **Which agent types need different paths?** | Bespoke (LangGraph, Strands, etc.), managed platform (AgentCore, Foundry), SaaS agents, low-code (Copilot Studio) | One common intake form and control baseline, with type-specific tracks. Bespoke gets the full SDLC and security review. Managed platform gets the reference-architecture check. SaaS gets third-party risk assessment plus data-flow review. Low-code gets guardrailed environments, DLP policies and a connector allow-list. |
| **What risk factors drive fast path vs enhanced review?** | Data classification, write/act authority, external exposure, autonomy level, financial impact, regulated process, cross-cloud reach, number of tools, user population | Tiering score (T1 to T4). Fast path means read-only, internal data only, human-in-loop, no external tools, and a pre-approved pattern. Enhanced review is triggered by any of: PII/NPI, write actions, money movement, customer-facing, autonomous or multi-agent (A2A), or new MCP servers. Tier drives the control set, review depth and recertification cadence. |
| **What is auto-provisioned after approval?** | Is it a golden path or a ticket queue? | Via IaC (Terraform/Bicep pipeline): Entra app/agent identity, owner groups, Kong consumer and route with rate limits and model allow-list, runtime project/account scaffold, Dynatrace tagging and dashboards, budget and quota, registry record, secret paths and a baseline guardrail config. Nothing is hand-built. |
| **What happens to rejected, abandoned or POC requests?** | Do POCs escape governance? | Time-boxed sandbox tier (for example 30 days) with synthetic data only, a separate network and a hard budget cap, and no production connectors. Auto-expiry with owner notification at 7 days. Rejected requests are logged with the reason. Abandoned requests trigger identity deletion and resource teardown through the same pipeline. |

---

## 2. Identity

| Question | Probe | Possible solution |
|---|---|---|
| **When does the agent act as itself vs on behalf of the user?** | Which tools require user context? Can the agent ever exceed the user's rights? | Define two explicit modes. **Autonomous** (agent identity, client credentials) is for batch and event-driven work, with its own scoped permissions. **Delegated** (OBO) is for user-initiated work, where effective permission is the intersection of the user's and the agent's rights. Never let an agent hold a superset of the user's access in delegated mode. Log both principals (`sub` and `act`) on every call. |
| **How are model, data, API, tool, MCP and A2A permissions granted?** | Where is the policy decision made? Is it per tool or per agent? | Model access: Kong consumer plus model allow-list. Data/API: Entra app roles and scopes, with resource-side enforcement. Tools/MCP: allow-list per agent in the registry, enforced at an MCP gateway or in AgentCore Gateway with JWT scopes per tool. A2A: agent-to-agent calls require a token with an audience for the target agent, and a declared dependency edge in the registry. All grants are requested through the pipeline (access-as-code), not granted ad hoc. |
| **How is least privilege established and periodically certified?** | Who reviews? Is evidence-based usage compared against grants? | Start deny-by-default. Compare granted vs actually used permissions (Entra sign-in logs, CloudTrail, Kong logs) and auto-flag unused ones. Run quarterly access reviews for T1-T2 and semi-annual for lower tiers (Entra access reviews, with the sponsor attesting). Auto-remove permissions unused for 90 days. |
| **What happens when the sponsor leaves or the platform changes?** | Orphaned agents are a common failure | An HR/Entra leaver event triggers a 14-day reassignment window, then the agent moves to restricted mode (read-only), then to suspended. Platform migration is treated as a new onboarding event with an identity re-bind. The old identity is disabled and credentials are rotated and revoked. The registry records lineage. |
| **Who can immediately suspend the agent during an incident?** | Is it a 24/7 role? Does it need approval? | A defined "break-glass" set: SOC, the platform on-call and the sponsor. Suspension must not need a change ticket. Suspension should be executable in layers: disable the Entra identity or revoke its refresh and sessions, block the Kong consumer, and disable the runtime endpoint. A single runbook or API triggers all three. |

**Additional identity points:** token lifetimes should be short and Continuous Access Evaluation (CAE) used where supported. Use federated credentials rather than secrets for cross-cloud workload auth (AWS role to Entra app). Never reuse one SPN across agents. For Foundry, prefer managed identity for Azure resources. Plan agent-to-MCP auth explicitly, since MCP servers rarely validate Entra tokens out of the box.

---

## 3. Runtime

| Question | Probe | Possible solution |
|---|---|---|
| **Which controls are common across AgentCore, Foundry, Copilot Studio and bespoke runtimes?** | Define a platform-neutral baseline | A **control baseline** independent of runtime: Entra auth, Kong for all model calls, a standard tool/MCP gateway, content safety/guardrails policy, mandatory telemetry (OpenTelemetry) to Dynatrace, budget limits, a registry ID injected into all traces, network egress policy, secret handling and a kill switch. Then map each runtime's native features (Bedrock Guardrails, Azure AI Content Safety, Copilot Studio DLP) as implementations of the same control IDs. Where a runtime can't meet one, it needs a documented exception. |
| **Where are authentication, authorization, routing validation and rate limits enforced?** | Avoid enforcement only in agent code | **AuthN:** at the runtime edge (JWT authorizer) and again at Kong. **AuthZ:** coarse in the gateway, fine-grained at the tool or resource. **Routing validation:** Kong allow-lists model, version and region per consumer. **Rate limits:** Kong (tokens per minute, requests per minute, per-consumer budget), plus per-agent concurrency in the runtime. Keep enforcement outside the agent's own code, so a compromised or looping agent can't disable it. |
| **How are tools, MCP servers, secrets and network access controlled?** | Who approves a new MCP server? | **Tools/MCP:** approved MCP server catalog, with the registry holding the allow-list. Treat third-party MCP servers as third-party software (pin versions, scan, review tool descriptions for prompt injection). Prefer an MCP gateway with auth, logging and schema validation. **Secrets:** Secrets Manager/Key Vault with rotation, never in prompts or env files. **Network:** VPC/VNet isolation, private endpoints, egress deny-by-default with FQDN allow-lists, and no direct internet from the agent runtime. |
| **How are loops, model outages and tool failures detected and stopped?** | What is the "circuit breaker" design? | Hard limits in the platform: maximum steps/iterations, maximum tokens, maximum wall-clock, maximum tool calls and a spend cap per session. Kong circuit breaking and failover to a secondary model or region, but only within an approved model list. Dynatrace anomaly detection on call-rate and cost spikes triggers an automatic throttle. Tool calls need timeouts, retries with backoff and idempotency keys. Define degraded behavior explicitly (fail closed for write actions, fail soft for read). |
| **Who owns rollback, kill switch and recovery?** | Is there a clear RACI? | The platform team owns the kill switch mechanism, the agent owner owns rollback of the agent version, and the sponsor owns the business decision to resume. Require versioned, immutable agent artifacts (prompt, tools, model, config) so rollback is a redeploy. Run recovery drills at least yearly for T1-T2. |

---

## 4. Visibility and Registry

| Question | Probe | Possible solution |
|---|---|---|
| **Is the registry a catalog, system of record, orchestration point or dashboard?** | Pick one primary role | **System of record for governance state** (identity, owner, tier, approvals, allowed tools/models), with discovery feeds and dashboards as secondary views. It should not be a runtime dependency on the hot path, so an outage doesn't stop agents. It can drive policy-as-code (OPA) through published, signed snapshots. |
| **Which fields are authoritative vs automatically discovered?** | Prevent drift | **Authoritative (human/pipeline-declared):** owner, sponsor, tier, purpose, approved data classes, approved tools/models. **Discovered:** runtime, deployed version, observed models and tools, observed data access, actual spend, last-active time. Alert on drift between declared and discovered. |
| **How are owner, identity, runtime, models, data, tools and budget linked?** | One key across all systems | A single **agent ID** that appears in the Entra object (tag/extension attribute), the Kong consumer, cloud resource tags, Dynatrace entity tags and trace attributes, and cost allocation tags. The registry stores the graph of those links. |
| **What changes trigger reapproval, recertification or suspension?** | Define materiality | **Reapproval:** new tool or MCP server, new data class, model change to a different provider or tier, autonomy increase, new user population, or a platform move. **Recertification:** time-based by tier. **Suspension:** policy violation, sponsor loss, expired attestation, security finding, or unexplained drift. |
| **How are shadow and dormant agents identified?** | Discovery sources | **Shadow:** Entra app and service principal scans, cloud account scans (AgentCore/Foundry resources), Kong consumers not in the registry, Dynatrace-detected LLM calls, Copilot Studio tenant inventory, and egress logs to model endpoints. **Dormant:** no invocations in 60-90 days leads to owner notice, then disable, then delete credentials, then retire. |

---

## 5. Monitoring

| Question | Probe | Possible solution |
|---|---|---|
| **Can an operator trace request → agent → model → tool → data → action → outcome?** | Is correlation guaranteed across Kong, runtime and tools? | Use W3C trace context end to end and propagate it through Kong, the runtime, MCP calls and downstream APIs. Use OpenTelemetry GenAI semantic conventions for model and tool spans. Add custom attributes: agent ID, user and delegated principal, session, tool name, data classification and outcome. Be deliberate about prompt and response capture, using redaction or sampling plus restricted access for sensitive content. Add an immutable audit log of actions as a separate record, not only traces. |
| **What status changes flow back into the registry?** | Define the event contract | Events for: deployed or version changed, first or last seen, new model or tool observed, policy violation, budget breach, throttled, suspended, certified, and drift detected. Use a webhook or event bus from Dynatrace and Kong to the registry API, so registry state is evidence-based. |
| **Which events trigger alert, throttle, human approval, suspension or retirement review?** | A defined response ladder | A **progressive ladder**: **Alert** (anomalous token use, elevated error rates) → **Throttle** (cost or rate spike, loop detected) → **Human approval** (high-risk action, first use of a new tool, guardrail near-miss) → **Suspend** (confirmed prompt injection or data exfiltration signals, repeated policy violation, unauthorized tool or model call) → **Retirement review** (dormancy, sponsor loss, persistent low value). Express these as codified rules, with the action and owner for each. |
| **What changes trigger reapproval, recertification or suspension?** | *(duplicate of 4.4)* | Same as 4.4, but emphasize the **detection** side: Dynatrace detects the change (a new tool in traces, a model not in the allow-list, a data class beyond the approved set) and the registry decides on the action. |
| **How are shadow and dormant agents identified?** | *(duplicate of 4.5)* | Same as 4.5, with the monitoring angle: scheduled Dynatrace and log queries for unregistered agent IDs or consumers, and "last invoked" metrics for dormancy. |

*Items 5.4 and 5.5 repeat 4.4 and 4.5 in your list. I assume that was a copy/paste slip, but if you intended different questions (for example, operational alert-tuning or SLO breaches), tell me and I'll replace them.*

---

## Areas likely missing that are mandatory for production

1. **Threat modeling for agents.** Cover prompt injection (direct and indirect), tool poisoning in MCP, confused-deputy, excessive agency, data exfiltration through tools, memory poisoning and agent-to-agent trust abuse. Map to OWASP LLM/Agentic Top 10 and MITRE ATLAS.
2. **Guardrails and content safety.** Input/output filtering, PII redaction at Kong, grounding checks, and topic restrictions, plus who tunes them and how false positives are handled.
3. **Data governance.** Data classification mapped to model and region, retention of prompts, traces and memory, no training on your data, DLP, cross-cloud data movement (relevant for Azure data to AWS runtime) and the right to erasure.
4. **Agent memory and state security.** Session and long-term memory isolation per user, encryption, TTL and poisoning controls.
5. **Evaluation and release gating.** Regression evals, red-team tests and safety evals as pipeline gates. Model version pinning and a process for model deprecation and upgrades.
6. **Human-in-the-loop design.** Approval thresholds, an approver identity that can't be the requester, timeouts, and approval fatigue.
7. **Cost and FinOps.** Per-agent budgets, token quotas in Kong, showback/chargeback, and runaway-spend alarms.
8. **Resilience.** SLOs, multi-region model failover, quota and capacity planning (provisioned throughput), DR and a tested kill-switch drill.
9. **Supply chain.** Model provenance, framework and MCP package pinning, SBOM, image signing and third-party agent (SaaS) vendor assessments.
10. **Compliance and audit.** Regulatory mapping (for a financial institution: model risk management such as SR 11-7, third-party risk, record retention, explainability, and EU AI Act or NIST AI RMF alignment), plus evidence collection that is automatic.
11. **Incident response.** Agent-specific playbooks, forensic retention of traces, containment steps, communication and a post-incident feedback loop to controls.
12. **Multi-agent / A2A governance.** Trust boundaries, delegation depth limits, loop prevention across agents, and an identity chain that preserves the original user.
13. **Policy-as-code.** OPA/Rego (or Cedar for AgentCore Gateway policies) for consistent decisions across both clouds, with versioned, tested policy and a decision log.
14. **Lifecycle and change management.** Versioning, canary releases, deprecation, and decommissioning with identity and data cleanup.
15. **User transparency and accountability.** Disclosure that users are interacting with an agent, a feedback and escalation path, and clear accountability for outcomes.
16. **Cross-cloud connectivity and trust.** How AWS-hosted agents reach Azure/Databricks data (private link, federation), and how Entra trust is extended into AWS without long-lived secrets.

---

## Suggested workshop decisions to force

- Delegated vs autonomous: which tools may use which mode, per tier?
- What is the minimum enforcement that must sit outside agent code?
- Is Entra Agent ID adopted now, or is SPN/managed identity the interim with a migration plan?
- How do we replace the AgentCore Identity token vault (OBO exchange service, secrets pattern, and rotation owner)?
- One agent ID across Entra, Kong, cloud tags and Dynatrace: who owns the standard?
- Kill-switch layers and who holds the keys.
- Tier definitions and the recertification cadence that follows.

I can turn this into a workshop deck, a facilitator guide with timeboxed agenda, or a decision-record template. Which would be most useful?
