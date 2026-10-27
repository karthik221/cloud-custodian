# Enterprise Agentic Runtime Standard: AWS Bedrock AgentCore vs. Azure AI Foundry

Architecture decision assessment · October 2026 · Enterprise multi-cloud environment

## 1. Executive recommendation

For your environment, I would not select a standard based on which cloud has the better agent runtime in isolation. I would evaluate which platform can meet your enterprise requirements with the least architectural friction, lowest total cost of ownership, and strongest security and operational controls.

Your three established enterprise choices are important:

Identity: Microsoft Entra ID

The common identity provider for users and agents, with explicit workload identity, delegated access, and authorization requirements.

Observability: Dynatrace

The enterprise monitoring destination for distributed traces, latency, errors, service health, and agent-level operational signals.

AI Gateway: Kong

The mandatory policy enforcement and routing layer for all LLM requests, including authentication, model routing, quotas, and gateway-level audit.

My initial architectural position is:

- Azure AI Foundry is a strong candidate for teams building managed, configuration-driven agents, especially where Entra ID, Azure-native security, and managed enterprise tooling are central.
- AWS Bedrock AgentCore is a strong candidate for teams requiring framework portability, customized agent execution, isolated sessions, specialized runtimes, and modular agent infrastructure.
- Neither is automatically the winner once Kong and Dynatrace are mandatory enterprise standards. The decisive issue is how completely each runtime can integrate with them without bypassing required controls or introducing substantial custom engineering.

One important distinction: the relevant Azure product is now documented as Microsoft Foundry / Foundry Agent Service, formerly Azure AI Foundry Agent Service in earlier documentation. The AWS comparison is against Amazon Bedrock AgentCore, not simply the Amazon Bedrock model inference API.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



## 2. What exactly are we comparing?

[Amazon AWS Logo PNG Images (Transparent HD Photo Clipart)](https://images.openai.com/static-rsc-4/PNR2CIDFYlrDJpVElSjdHo1sB1l5sAHN9WEb478MheJfB7ibs6dwFQPcQ1Vd8IrsXD1WP6cbAvi3H8Q-0cRbEUyVhZ970KKy1m-CyBB6vEgAt2Y7E7OQURdHYaIie6HP224oe3YxpsoFJfp66kcCY-KRLrkRsl_zN13IQpvQfYA?purpose=inline)

## Amazon Bedrock AgentCore

A modular, managed platform for running and operating agents. It supports multiple agent frameworks and models, isolated execution, memory, identity, tool connectivity, browser and code execution, observability, and evaluation capabilities.

Official reference: [AgentCore developer guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/?utm_source=chatgpt.com)

[How to Download Microsoft Azure Architecture Icons? | Arun Potti's Power Platform blog](https://images.openai.com/static-rsc-4/vtmsVnWXsBgoC163PPrJvMlsRWdk5Af_vq3QUu_ctSpO3WrpTunYlZ9mGy473bSCO8tt6P5h0Iv2utKnCuBRA7x1WXfz89We1FdKaYZgnuvVZnMCxZq3wBpwnKShlFj-O8tGGl8bnMOtxwyL052sAY_rDxfqFIp_1DggI-kRcFs?purpose=inline)

## Microsoft Foundry Agent Service

A managed agent development and runtime platform offering configuration-driven prompt agents, hosted agents for custom code, managed tools, model access, enterprise identity, safety controls, versioning, and integrated evaluation and monitoring.

Official reference: [Foundry Agent Service overview](https://learn.microsoft.com/en-us/azure/foundry/agents/overview?utm_source=chatgpt.com)

These products overlap, but they are not identical abstractions. AgentCore emphasizes modular runtime infrastructure that can be assembled around different frameworks; Foundry offers a more integrated developer experience with managed agent types and Azure platform services. A fair comparison must evaluate the same workload on both, rather than compare every feature of one product with only the agent execution feature of the other.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



## 3. The target enterprise architecture

I recommend separating the agent runtime decision from the enterprise control plane. The runtime executes an agent; the control plane establishes which agents can be built, which models and tools they can use, how they are secured, and how their quality and cost are measured.

Users, applications and developer teams

Web apps · APIs · Internal platforms · Workflows

Microsoft Entra ID

User authentication · Workload identities · Token claims

Kong AI Gateway — mandatory LLM path

Model routing · Authentication · Rate limits · Policy enforcement · Usage telemetry

[AWS Signature Version 4 - Overview (ODC) | OutSystems](https://images.openai.com/static-rsc-4/GQVvVReLOLyo2cBY9UK37We20aAcnvWntcQX1XnyDxgfrdFwuqaJ3trUP-TI8EIpo3kAeyf6I6PAuLfUpSW70V6jWDg3e9o7BUZ0xR6rMpElC58PChcOXH_P0iTds1kIBY4WUy4b34zkg7uvnuqDQfeFjnIsArb6kRNLe7zNXjo?purpose=inline)

AWS

Bedrock AgentCore Runtime, Gateway, Identity, Memory, Policy and Observability

[Офісний додаток Microsoft Azure SQL Edge - 3 year Subscription Commercial (DG7GMGF0GJC2_0001_P3Y_T) купити — Game-X](https://images.openai.com/static-rsc-4/qcOwOQ39nNj08oQpIsyEXEv3Je2dvZ44ZbKUTH0uDuEttPB-nk3qZo-WpYA7-4TaVqh8bTgyawoaqnTf3cxRsQS2omwS_J9mhHNtNGbiRKGYnwsfm6FGjsAN3_GNm22Ip_IlzoU8pIc3UN8lPGM8vlX3-ZIVX5myhr716Gt-Dig?purpose=inline)

Azure

Foundry Agent Service, hosted agents, managed tools and Azure identity/security services

Agent tool calls should pass through separately governed tool endpoints. They do not automatically need to traverse the LLM gateway unless they make a model request.

Dynatrace

OpenTelemetry traces, metrics, service health and operational alerts

Enterprise governance

Agent registry, evaluations, policy, audit, approved tools and cost allocation

### A critical design rule: Kong must not be bypassable

If your policy is that every LLM request must go through Kong, that must be enforced technically, not merely documented.

- The agent's initial model request, subsequent reasoning calls, tool-selection rounds, retries, and sub-agent model calls must use the approved gateway path.
- Direct access to provider inference endpoints should be blocked where feasible through network controls, endpoint restrictions, IAM/RBAC, and resource policies.
- Agent-native features that invoke a model internally must be assessed individually. Do not assume that a model connection or gateway configuration controls every internal model call.
- Token, model, and policy telemetry should be correlated between Kong and the runtime.

This is a go/no-go requirement for both candidates. If a managed agent mode cannot route all its internal LLM requests through Kong, it must either be excluded from the standard or be accompanied by a supported architecture that enforces the required path.

## 4. Detailed capability comparison

The table below compares production architecture capabilities, not marketing feature counts. “Strong” means a relatively direct platform capability; it does not mean every security or operational outcome is automatic.

| Capability                | AWS Bedrock AgentCore                                                         | Microsoft Foundry Agent Service                                                                         |
| ------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Runtime architecture      | Modular, managed agent infrastructure                                         | Integrated managed agent platform                                                                       |
| Agent development         | Bring your own framework, code, or managed harness                            | Configuration-driven prompt agents and custom hosted agents                                             |
| Framework portability     | Very strong; supports multiple open-source frameworks                         | Strong for hosted agents; supported framework choices depend on the agent type                          |
| Model portability         | Models inside and outside Bedrock, including compatible external providers    | Foundry model catalog and external models through supported connections                                 |
| Managed execution         | Isolated microVMs and managed instance options                                | Fully managed prompt-agent execution; managed container hosting for hosted agents                       |
| Custom orchestration      | Excellent for teams owning their agent loop                                   | Excellent with hosted agents; prompt agents abstract more of the loop                                   |
| Agent memory              | Dedicated short- and long-term memory service                                 | Conversation/thread state and platform integrations; custom state stores can be used where needed       |
| Tool integration          | Gateway can expose APIs, Lambda functions and MCP tools                       | Managed toolboxes, custom functions, MCP servers and platform tools                                     |
| Code execution            | Isolated Code Interpreter                                                     | Managed Code Interpreter tool                                                                           |
| Browser automation        | Dedicated managed Browser capability                                          | Browser/web tools and custom integrations, depending on configuration                                   |
| Multi-agent design        | Framework-neutral; custom coordination and supported protocols                | Custom multi-agent orchestration; A2A and hosted-agent patterns                                         |
| Agent identity            | AgentCore Identity supports external identity providers, including Entra ID   | Native Entra identity and dedicated identity for hosted agents                                          |
| Policy enforcement        | AgentCore Policy, IAM, Gateway controls and optional Bedrock Guardrails       | Entra/Azure RBAC, content filters, networking and gateway policies                                      |
| Quality evaluation        | AgentCore Evaluations and custom evaluators                                   | Built-in evaluations and monitoring, with additional evaluation frameworks                              |
| Operational telemetry     | AgentCore Observability, CloudWatch and OpenTelemetry-compatible integrations | Platform tracing, metrics, evaluations and Application Insights integrations                            |
| Deployment and release    | Custom deployment pipelines and runtime configuration                         | Managed agent versions, endpoints and publishing workflows                                              |
| Enterprise portability    | Strong when you own the framework and avoid proprietary abstractions          | Strongest when custom code and standard protocols are used; greater coupling with native platform tools |
| Native platform advantage | AWS services, IAM, AWS operational ecosystem                                  | Azure identity, data services, Microsoft ecosystem and enterprise developer experience                  |

These capability differences are grounded in the vendors' published platform documentation. Exact availability, protocol support, regional availability, and preview versus generally available status should be verified for the specific deployment configuration.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



### How I would interpret the comparison

AgentCore has the architectural advantage when runtime freedom matters most. It is particularly suitable when teams need to bring their own orchestration framework, isolate complex agent sessions, build custom tools, or move between model providers without rewriting the agent.

Foundry has the developer-experience advantage when managed conventions matter most. It is particularly suitable when teams want a managed agent lifecycle, native enterprise identity, standard platform tools, and fewer infrastructure decisions.

Neither advantage is universal. A team building a simple enterprise knowledge agent may gain more from Foundry's managed experience, while a team building a complex software-engineering or data-analysis agent may gain more from AgentCore's modular execution options.

## 5. Kong AI Gateway: the most important integration test

Your Kong requirement materially affects the decision, so I would treat it as a mandatory architecture evaluation rather than an ordinary integration checkbox.

Kong supports model-provider routing, authentication, policy enforcement, usage telemetry, MCP traffic, and agent-to-agent traffic. However, the fact that Kong can proxy an LLM API does not prove that every managed agent service will route its internal inference calls through that proxy.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developer.konghq.com\&sz=32)

Kong Docs+1



## Integration assessment

Foundry: a documented gateway connection path

Foundry Agent Service documents bring-your-own-model connections to external gateways, including non-Azure gateways. The documented pattern allows agents to use a model endpoint behind an external gateway, with the gateway's endpoint, authentication and protocol configured as a model connection.

This is a promising route for Kong integration, but it must be tested for the precise model protocol, tool-call cycle, streaming behavior, retries and model features you intend to use.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learn.microsoft.com\&sz=32)

Microsoft Learn



AgentCore: a documented external inference path

AgentCore supports external model providers and offers inference-target routing through its own Gateway. A custom agent can also be designed to call the enterprise Kong endpoint directly.

Because AgentCore is modular, it offers flexibility in the agent's model client and orchestration code. But native features that perform their own model calls must be independently validated against the Kong requirement.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



### The architectural question: which gateway owns model governance?

AWS has its own AgentCore Gateway and inference-target functionality, while Foundry has integrations for external model gateways. Kong is already your enterprise AI Gateway.

I would therefore adopt the following rule:

- Kong owns enterprise LLM routing and provider-level policy enforcement.
- AgentCore Gateway or Foundry toolboxes may manage tool discovery and tool connectivity, but they must not create an alternate route to LLM providers that bypasses Kong.
- Do not introduce a second model gateway simply because the runtime vendor supplies one. Use the runtime's gateway only for functions that are compatible with the enterprise architecture.
- Avoid duplicating the same prompt sanitization, rate limits, or routing policies at multiple layers unless the duplication is intentional and its failure behavior is understood.

### Mandatory Kong proof-of-concept tests

| Test                            | Required evidence                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------------- |
| Initial inference               | Model call reaches Kong and the expected upstream provider                              |
| Multi-step agent loop           | Every subsequent model request also reaches Kong                                        |
| Tool-calling cycle              | The model's tool selection, tool execution, and next model request are correctly traced |
| Multi-agent workflow            | Calls made by every sub-agent use the approved model route                              |
| Streaming                       | Streaming responses work without breaking gateway controls                              |
| Retries and failover            | No hidden direct-provider retry or fallback occurs                                      |
| Embeddings and auxiliary models | All requests classified as LLM requests comply with the same policy                     |
| Network enforcement             | Direct provider inference is denied where required                                      |
| Audit correlation               | Kong, runtime, and Dynatrace records can be correlated for a single workflow            |

Decision gate: A runtime configuration that cannot demonstrate complete Kong enforcement must not pass the enterprise standard, regardless of its feature set or price.

## 6. Entra ID: user identity versus agent identity

Both products can participate in an Entra-based enterprise identity architecture. The important distinction is whether an agent acts as itself or acts on behalf of the initiating user.

| Identity requirement         | AgentCore                                                                                | Foundry                                                                               |
| ---------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Entra ID as enterprise IdP   | Supported through AgentCore Identity integrations                                        | Native platform identity integration                                                  |
| Dedicated agent identity     | AgentCore Identity and configured workload credentials                                   | Dedicated Entra identity supported for hosted agents                                  |
| User-delegated access        | Possible through supported OAuth/token-exchange flows; design and configuration required | On-Behalf-Of flows supported for applicable integrations and configurations           |
| Cloud resource authorization | AWS IAM roles and resource policies remain necessary                                     | Azure RBAC and resource permissions remain necessary                                  |
| Cross-cloud access           | Requires explicit federation, token exchange or credential brokering                     | Requires explicit AWS credential federation or another approved cross-cloud mechanism |
| Central user authorization   | Must be enforced in the application and tool layer                                       | Must be enforced in the application and tool layer                                    |

The published documentation confirms AgentCore Identity's support for external identity providers and Foundry's identity and security capabilities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



### Recommended identity pattern

1\. Entra ID authenticates the user

2\. Application validates user and agent permissions

3\. Runtime receives scoped user context and agent identity

4\. Kong validates inbound access; approved model credentials are applied upstream

5\. Tool authorization checks the actual resource and action

Use two explicitly defined execution modes:

- Delegated mode: the agent acts on behalf of a user and should not exceed that user's permissions. Token forwarding, On-Behalf-Of flows, audience validation, and token lifetime must be tested.
- Workload mode: the agent acts under its own managed identity and narrowly scoped permissions. This is appropriate for scheduled jobs, autonomous processing, and approved background tasks.

Do not treat a valid Entra token as sufficient authorization for every AWS or Azure resource. A token's issuer, audience, claims, and intended use must be validated, and the corresponding resource permissions must still be enforced.

For a multi-cloud enterprise, I would also require a standard for identity propagation: a stable correlation identifier, authenticated user or workload subject, agent ID, and delegated-versus-workload execution mode. Never rely on an untrusted request header as proof of user identity.

## 7. Security and guardrails

Guardrails need to be evaluated as multiple independent layers. Neither a runtime's safety features nor an AI Gateway alone provides complete protection against unsafe agent behavior.

| Security control            | AgentCore                                                                                                          | Foundry                                                                    | Enterprise standard                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- | --------------------------------------- |
| Input/output content safety | Bedrock Guardrails can be used with supported model paths; additional controls may be required for external models | Integrated content filters and configurable safety controls                | Required                                |
| Prompt injection defense    | Combine input/output safeguards, tool policies and application-level defenses                                      | Built-in content safety features, with application and tool-layer defenses | Required; test indirect injection too   |
| Tool authorization          | AgentCore Policy, Gateway and AWS IAM                                                                              | Entra identity, Azure RBAC and tool permissions                            | Deny by default                         |
| Least privilege             | AWS IAM and scoped credentials                                                                                     | Entra workload identities and Azure RBAC                                   | Required                                |
| Secrets management          | AWS Secrets Manager and supported identity integrations                                                            | Azure Key Vault and managed identity integrations                          | Required                                |
| Network isolation           | Runtime isolation and supported AWS networking controls                                                            | Supported virtual network isolation and hosted-agent networking options    | Required for sensitive workloads        |
| Sensitive data protection   | Configurable data handling, logging controls and optional guardrails                                               | Content filters, resource controls and configured data protections         | Required                                |
| Audit trail                 | AgentCore traces, CloudWatch and AWS audit services                                                                | Agent traces, Azure monitoring and Azure audit services                    | Central correlation and retention       |
| Human approval              | Must be designed into workflow/tool authorization where needed                                                     | Must be designed into workflow/tool authorization where needed             | Required for high-impact actions        |
| Model-provider controls     | AgentCore policies and provider-specific controls                                                                  | Foundry policies and provider-specific controls                            | Kong plus provider-specific enforcement |

The platform documentation describes AgentCore Policy as a mechanism for controlling tool actions and Foundry as providing content-safety, identity, RBAC and network controls. Those controls have different scopes; they should not be treated as interchangeable.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



### Recommended defense-in-depth model

Layer 1 — Enterprise gateway

Kong authenticates callers, applies approved model routing, enforces quotas, and applies configured prompt/response policies. Provider-native safeguards remain available where compatible.

Layer 2 — Runtime and agent policy

Restrict execution, memory access, model selection, tool discovery, and permitted actions. Keep the tool allowlist and agent permissions independent of instructions supplied to the model.

Layer 3 — Tool and data authorization

Recheck identity and resource permissions at every tool boundary. A model's decision to invoke a function must never be sufficient authorization to execute it.

Layer 4 — Business controls

Require approvals for destructive actions, financial transactions, production changes and other high-impact operations. Apply idempotency, transaction limits, rollback and audit requirements.

### User configurability and developer autonomy

A common failure in enterprise agent platforms is making every security or model change dependent on a central platform team. That limits developer productivity. Conversely, giving teams unrestricted access to models, tools and policies undermines governance.

I recommend a paved-road model with three configuration tiers:

| Tier             | Developer freedom                                                                          | Central restrictions                                                            |
| ---------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- |
| Standard agent   | Configure prompts, approved models, temperature, tool allowlists and evaluation thresholds | Approved templates, model access, mandatory gateway and telemetry               |
| Advanced agent   | Custom framework, orchestration, memory and tool implementations                           | Architecture review, approved network patterns, identity and security tests     |
| Restricted agent | Controlled access to sensitive data or high-impact actions                                 | Explicit approval, tighter permissions, mandatory evaluation and stronger audit |

Apply the same tiers to both runtimes. Use version-controlled configuration, policy-as-code, reusable templates, automated validation and controlled promotion between environments.

The winning runtime should allow developers to configure these choices without bypassing central security. It should also provide clear failure messages when a policy, quota, identity or model configuration is rejected.

## 8. Observability: Dynatrace as the common monitoring plane

Dynatrace should be the common operational view for both platforms, not merely a place to forward infrastructure metrics.

Dynatrace documents integrations for both AgentCore and Azure AI Foundry, and supports OpenTelemetry-based AI observability. Foundry hosted agents can export telemetry to an OTLP-compliant endpoint, while AgentCore exposes OpenTelemetry-compatible telemetry through its observability capabilities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.dynatrace.com\&sz=32)

Dynatrace Docs+2



## Target telemetry pipeline

Agent application and runtime

Agent steps · Tool calls · Retries · Memory · Exceptions

OpenTelemetry / OpenInference instrumentation

Consistent trace context and GenAI semantic attributes

Dynatrace AI Observability

Distributed traces · Agent topology · Latency · Token metrics · Errors · Evaluations

Kong and cloud-provider telemetry

Model selection · Gateway latency · Usage · Policy outcomes · Cloud infrastructure

Correlate gateway and runtime records using trace context and stable workflow identifiers. Some provider-side events may require additional instrumentation or a separate telemetry export.

### Observability comparison

| Requirement                 | AgentCore                                                                                                | Foundry                                                                                               |
| --------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Native runtime traces       | AgentCore Observability, with CloudWatch as its underlying telemetry destination for documented features | Managed agent tracing and Application Insights integration                                            |
| Export to Dynatrace         | Use supported OpenTelemetry/OpenInference paths and validate the exact runtime instrumentation           | Hosted-agent OTLP export is documented; validate prompt-agent and other agent-type paths individually |
| Tool-call tracing           | Supported, subject to framework and instrumentation path                                                 | Supported, subject to agent type and instrumentation                                                  |
| Model/token telemetry       | Runtime traces and provider usage data                                                                   | Runtime traces and provider usage data                                                                |
| Infrastructure telemetry    | AWS infrastructure monitoring and cloud-native telemetry                                                 | Azure infrastructure monitoring and cloud-native telemetry                                            |
| Native dashboard dependency | CloudWatch remains useful for AWS-native diagnostics and billing                                         | Application Insights remains useful for Azure-native diagnostics and billing                          |
| Central cross-cloud view    | Dynatrace plus normalized telemetry                                                                      | Dynatrace plus normalized telemetry                                                                   |

### My recommendation for Dynatrace

Use Dynatrace as the standard operational view, while retaining native cloud monitoring where it provides essential runtime diagnostics and billing detail.

Establish a common telemetry schema with at least:

- `agent.id`, `agent.version`, `agent.environment`, `agent.framework`
- `workflow.id`, trace ID, span ID, parent span ID
- `gen_ai.request.model`, provider and token-usage attributes where available
- Tool name, action category, duration, result status and retry count
- Gateway route, upstream model, policy outcome and request correlation ID
- Evaluation score, safety outcome, failure classification and latency

Do not send full prompts, responses, credentials, tokens or retrieved sensitive documents to Dynatrace by default. Establish data classification, redaction, sampling and retention rules first. Dynatrace's AI observability guidance also distinguishes monitoring guardrail outcomes from actually enforcing guardrails.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.dynatrace.com\&sz=32)

Dynatrace Docs+1



For an agentic application, a useful SLO should cover the complete user workflow, not just the model response. For example, measure end-to-end success rate, p95 workflow latency, tool failure rate, cost per successful task, and safety-policy violation rate.

## 9. Pricing and total cost of ownership

A fair price comparison must include the model, runtime, tools, gateway, telemetry, storage, engineering and operations. Comparing only the published runtime charge will produce misleading results.

### AWS AgentCore pricing

AgentCore publishes consumption-based prices for its modular capabilities. Its pricing model includes:

- Runtime compute, based on consumption for microVMs or managed-instance compute and management fees.
- Gateway invocations and semantic search/indexing.
- Identity token or API-key requests in applicable scenarios.
- Short- and long-term memory operations and storage.
- Browser and Code Interpreter execution.
- Observability data ingestion, storage and queries through CloudWatch.
- Evaluations and policy authorization.

For example, the published pricing page lists Gateway API invocations at $0.005 per 1,000 invocations and Gateway search at $0.025 per 1,000 invocations. These are individual component rates, not an estimate of a complete agent workload. Runtime rates and other components vary by the chosen execution mode and usage.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://aws.amazon.com\&sz=32)

AWS+1



Official pricing: [Amazon Bedrock AgentCore pricing](https://aws.amazon.com/bedrock/agentcore/pricing/?utm_source=chatgpt.com)

### Azure Foundry pricing

Foundry Agent Service's published pricing states that there is no additional charge for creating or running Foundry-native prompt agents and workflows themselves. That does not mean the full solution is free.

Charges can include:

- Model inference based on the model and its input/output usage.
- Code Interpreter sessions when used.
- File search and vector storage.
- Separately charged or licensed platform tools and data integrations.
- Compute for hosted agents and any associated resources.
- Network, logging, storage, monitoring and external service charges.

The pricing treatment differs between managed prompt agents and hosted agents, so use the correct agent type when estimating.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learn.microsoft.com\&sz=32)

Microsoft Learn+1



Official pricing: [Foundry Agent Service pricing](https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/?utm_source=chatgpt.com)

### Cost comparison by category

| Cost component                 | AgentCore                                                                                        | Foundry                                                                                           |
| ------------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| Managed prompt-agent execution | Metered runtime and underlying capability charges apply for applicable AgentCore execution modes | No additional prompt-agent service charge for native prompt agents; model and tool charges remain |
| Custom agent compute           | Runtime microVM consumption or managed-instance pricing                                          | Hosted-agent compute and related resource charges                                                 |
| Model inference                | Charged by the model provider; model calls can occur multiple times per workflow                 | Charged by the selected model/provider; multiple model calls can occur                            |
| Memory and retrieval           | AgentCore Memory and connected storage costs                                                     | Selected conversation state, file search, vector and external data resources                      |
| Tool execution                 | Gateway, Browser, Code Interpreter and downstream tool charges as applicable                     | Code Interpreter, managed tools, hosted compute and downstream tool charges as applicable         |
| Gateway                        | Kong costs, plus any AgentCore Gateway usage if used                                             | Kong costs; any other gateway or integration costs if used                                        |
| Monitoring                     | Dynatrace plus CloudWatch telemetry charges                                                      | Dynatrace plus any Application Insights/other Azure monitoring charges                            |
| Platform engineering           | Custom framework, deployment and integration effort                                              | Framework, deployment and integration effort, often reduced for native prompt-agent workflows     |
| Operations                     | Depends on how many modular capabilities are assembled                                           | Depends on agent type, tool choices and Azure integration depth                                   |

### Why I would not declare a cost winner yet

AgentCore's consumption model can be attractive for bursty workloads that spend significant time waiting for model or tool responses. Foundry's managed prompt agents can be cost-effective where their native execution path meets the requirements without requiring hosted-agent infrastructure.

However, Foundry's native prompt-agent path and a custom hosted-agent path are different cost and flexibility choices. Similarly, AgentCore microVM execution and managed instances have different utilization characteristics.

The biggest variable may be the number and length of model calls per successful business task, not the runtime fee. A workflow that performs several reasoning loops, repeatedly invokes tools and sends a large conversation history to the model can cost substantially more than a simple one-call agent on either platform.

### Cost model to use in the business case

For each runtime, calculate:

\\[ \begin{aligned} \text{Monthly TCO} ={}& \text{Model inference}\\\ &+\text{Runtime and tool execution}\\\ &+\text{Memory and retrieval}\\\ &+\text{Kong and telemetry}\\\ &+\text{Operations and engineering} \end{aligned} \\]

I would run the same representative workloads through both platforms and calculate:

\\[ \text{Cost per successful task} = \frac{\text{Total workload cost}}{\text{Successfully completed tasks}} \\]

Include failed runs, retries, evaluation overhead, gateway charges, monitoring charges and human-review costs. Use the same model, quality target, input data, expected output and security requirements for each candidate wherever technically possible.

## 10. Operational overhead and developer productivity

The relevant question is not simply how much infrastructure the vendor manages. It is how much work your platform team must do to make an agent secure, observable, deployable and supportable under enterprise standards.

| Operational area             | AgentCore                                                                               | Foundry                                                                         |
| ---------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Initial setup                | Moderate; select and assemble appropriate services                                      | Low for native prompt agents; moderate for hosted agents                        |
| Runtime infrastructure       | Managed microVM or instance options                                                     | Managed prompt execution or hosted agent compute                                |
| Custom framework maintenance | Flexible, but teams own framework-level decisions                                       | Teams own code and framework for hosted agents                                  |
| Identity integration         | Configure Entra-compatible authentication and AWS resource authorization                | More native Entra integration; resource permissions still require configuration |
| Kong integration             | Custom model client or supported external inference path; validate managed capabilities | Documented external gateway connection for supported model protocols            |
| Dynatrace integration        | Instrumentation/export configuration and validation                                     | OTLP support for hosted agents; validate other agent types                      |
| Tool management              | AgentCore Gateway and custom tool infrastructure                                        | Toolboxes, managed tools and custom endpoints                                   |
| Release management           | More responsibility for application packaging and deployment pipelines                  | Managed agent versions and publishing for supported agent types                 |
| Incident diagnosis           | CloudWatch and runtime traces, correlated with Dynatrace                                | Foundry/Application Insights and hosted-agent traces, correlated with Dynatrace |
| Cross-cloud standardization  | More framework and integration flexibility, but more design responsibility              | Simpler within Azure conventions; additional work for non-Azure resource access |
| Governance at scale          | Requires standard templates and centralized policies                                    | Requires standard templates and centralized policies                            |

The operational advantage depends on the agent type. A simple Foundry prompt agent will generally require less application infrastructure than a custom agent deployed on either platform. A complex custom Foundry hosted agent and an AgentCore application built with the same framework may have much more comparable operational responsibilities.

### Operational costs people often overlook

I would explicitly budget for:

1. Platform engineering: approved agent templates, SDK wrappers, deployment pipelines, runtime configuration and reusable tool contracts.
2. Security engineering: Entra integration, cloud permissions, secrets, network isolation, threat modeling and penetration testing.
3. AI quality operations: test datasets, regression evaluations, model changes, prompt versions, safety tests and quality drift.
4. SRE operations: alerts, incident response, service-level objectives, quotas, capacity, regional availability and recovery.
5. FinOps: token attribution, runtime costs, evaluation costs, gateway consumption, monitoring retention and budget enforcement.
6. Developer support: documentation, sample agents, troubleshooting, local development workflows and onboarding.

My expectation is that Foundry will have lower operational overhead for teams using native managed workflows, while AgentCore may provide greater architectural control at the cost of more design choices. That is a hypothesis to measure through the pilot, not a guaranteed platform-wide result.

## 11. Future-proofing and avoiding vendor lock-in

For a multi-cloud enterprise, future-proofing is not the number of models currently listed in a catalog. It is how much of your investment can survive changes in the runtime, model provider, cloud strategy or agent framework.

| Future-proofing factor           | AgentCore                                                                  | Foundry                                                                               |
| -------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Framework portability            | Strong, including several open-source frameworks                           | Strong for supported hosted-agent frameworks                                          |
| Model-provider portability       | Strong, including external models                                          | Supported external model connections, with feature compatibility to validate          |
| Standard protocols               | MCP, A2A and OpenTelemetry-compatible patterns                             | MCP, A2A and OpenTelemetry-supported paths, with availability depending on capability |
| Custom orchestration             | High flexibility                                                           | High with hosted agents; less exposed in native prompt agents                         |
| Proprietary service dependency   | Increases if relying heavily on AgentCore-specific services                | Increases if relying heavily on native Foundry tools and state abstractions           |
| Migration effort                 | Lower when the application owns orchestration and uses portable interfaces | Lower when custom agent code and external interfaces remain portable                  |
| Enterprise ecosystem integration | Strong in AWS-centric environments                                         | Strong in Microsoft/Azure-centric environments                                        |

AWS explicitly positions AgentCore for use with different frameworks and foundation models. Foundry also supports custom hosted agents and external model connections, so it should not be characterized as inherently locked to one model family.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.aws.amazon.com\&sz=32)

Amazon Bedrock AgentCore+1



### My recommended portability strategy

Regardless of the winning runtime, make the following enterprise standards mandatory:

- Model adapter: expose a common model-client interface that targets Kong rather than embedding provider-specific endpoints in agent code.
- Tool contract: define typed inputs and outputs, stable error codes, authorization requirements and versioned API schemas.
- Agent metadata: use a common agent manifest with owner, purpose, data classification, environment, approved models, permitted tools, identity mode and evaluation requirements.
- State and memory: isolate business state from runtime-specific conversation storage where long-term portability matters.
- Telemetry: standardize on OpenTelemetry/OpenInference conventions and a common correlation model.
- Policy: keep enterprise authorization and approval rules outside prompts and agent instructions.
- Deployment: use version control, automated evaluations, infrastructure as code and reproducible promotion across environments.

Do not create a universal abstraction that strips away every useful platform feature. Instead, define a portable core and allow platform-specific extensions when the benefit justifies the dependency.

## 12. Which use cases fit each runtime?

[The End of MCP for AI Agents? Why Code Execution is the Better Abstraction | FlowHunt](https://images.openai.com/static-rsc-4/3yaW0qMxVi90XeAAQo-CZLn-tHs2n2gxFqGZxCNV7AASkPirqqxw3lW1DTKnjdBYP1MT8cGoALLdbMMJA5-t3uE-T3Y1ZrjiF8wCRnt7Z4MLRVNRy1PZLNDyhyllbJzmCiZ4Yqno-h0tUo7gqkS7ltIk7yhIPgdtZgTghoEQNxY?purpose=inline)

AWS AgentCore — strong fit

- Complex agents using LangGraph, Strands or other supported frameworks.
- Coding, analysis and research agents needing isolated execution.
- Multi-agent applications with custom orchestration and persistent memory.
- Agents requiring custom browser or code execution capabilities.
- Workloads where teams want to compose modular runtime services.

Watch-outs: framework freedom increases responsibility for standardization, and every internal model call must respect Kong routing.

[Zeitnah und günstig digitalisieren mit Low-Code-Plattformen](https://images.openai.com/static-rsc-4/XXweK3w55SCsLitBf8oP7Q462LOe3aJZUji7teiiF0OCMBxuxz4oSjHAw1GSQXV5CmREFDSMxHIQU5uejPqt0UD7ifatFIfXYrUSU5oFlxzXN2WtM7DfMOag2x38k-YwXgRNU5fPPtMB8eG55qbapbcC-8X1ZS9mk8ULsUjAU9w?purpose=inline)

Microsoft Foundry — strong fit

- Internal knowledge assistants and business workflow agents.
- Agents integrated with Entra-secured enterprise applications.
- Teams wanting managed prompt-agent execution and standard platform tools.
- Custom hosted agents that need managed deployment and identity.
- Applications integrated with Azure data services and Microsoft ecosystem tools.

Watch-outs: native tools may create additional dependencies, and the precise agent type determines the gateway, network and telemetry integration path.

For both, I would separate read-only informational agents from agents capable of making changes. Read-only knowledge and advisory agents should be the initial baseline. Agents that modify infrastructure, grant access, update production systems or execute transactions require additional approval and risk controls regardless of runtime.

## 13. Weighted evaluation framework for the enterprise standard

I would use a weighted scorecard with a mandatory compliance gate. The weights below are a starting proposal for your stated architecture, not a claim that one vendor has already won.

## Interactive runtime scorecard

Rate each candidate from 1 (poor) to 5 (excellent) based on evidence from your pilot. Scores initially start at 3 to indicate that neither candidate has yet been validated.

### AWS Bedrock AgentCore

# 60.0 / 100

Weighted score

Kong enforcement and routing

20% weight · All LLM calls must traverse the enterprise gateway.

12345

Security and identity

15% weight · Entra integration, workload identity, least privilege and network controls.

12345

Agent capabilities

12% weight · Custom orchestration, tools, state, isolation and multi-agent workflows.

12345

Observability

12% weight · Dynatrace integration, complete traces, correlation and actionable alerts.

12345

Total cost of ownership

12% weight · Runtime, models, gateway, telemetry, engineering and support.

12345

Developer experience

8% weight · Onboarding, templates, SDKs, debugging and time to production.

12345

Guardrails and governance

8% weight · Input/output safety, tool policies, approvals, evaluations and audit.

12345

Future-proofing

8% weight · Framework/model portability, standards and exit strategy.

12345

Reliability and operations

5% weight · SLOs, scaling, recovery, regional support and incident management.

12345

### Microsoft Foundry Agent Service

# 60.0 / 100

Weighted score

Kong enforcement and routing

20% weight

12345

Security and identity

15% weight

12345

Agent capabilities

12% weight

12345

Observability

12% weight

12345

Total cost of ownership

12% weight

12345

Developer experience

8% weight

12345

Guardrails and governance

8% weight

12345

Future-proofing

8% weight

12345

Reliability and operations

5% weight

12345

### Mandatory compliance gate

A high weighted score cannot compensate for failing the enterprise gateway or security requirements.

AgentCore passes the mandatory tests?

Not yet validated

Pass — verified in testing

Fail — required control not enforced

Foundry passes the mandatory tests?

Not yet validated

Pass — verified in testing

Fail — required control not enforced

The compliance decision is still pending. Treat the scores as provisional until the mandatory controls have been tested.

Generate decision analysis

### How to interpret the scorecard

- 80–100: Strong candidate, assuming every mandatory control passes and the score is evidence-based.
- 70–79: Viable, but specific gaps should be addressed before standardization.
- Below 70: Not a strong enterprise-wide standard without material remediation.
- Less than five points between candidates: Treat the result as inconclusive; compare operational risk, workload fit and three-year TCO.

These are suggested governance thresholds, not industry-certified benchmarks. Use the same evaluators, workloads and scoring definitions for both vendors.

## 14. Recommended proof of concept

I would run a controlled, four-workload evaluation rather than an open-ended demo.

Workload A — Enterprise knowledge agent

Test document retrieval, grounded answers, access filtering, prompt injection resistance and answer quality.

Workload B — Multi-step tool-using agent

Test typed tool calls, MCP/API integration, retries, error recovery, delegated identity and authorization.

Workload C — Custom framework agent

Use the same supported framework and agent logic on both runtimes. Test execution isolation, memory, deployment and model-provider changes through Kong.

Workload D — Restricted enterprise agent

Test sensitive-data access, destructive-tool denial, approval gates, auditability and recovery from denied or failed actions.

### Suggested evaluation schedule

| Phase                                     | Duration  | Deliverable                                            |
| ----------------------------------------- | --------- | ------------------------------------------------------ |
| Requirements and architecture baseline    | 1 week    | Approved test cases, threat model and success criteria |
| Kong, Entra and Dynatrace integration     | 1–2 weeks | Verified identity, routing, telemetry and audit paths  |
| Build comparable agents                   | 2 weeks   | Four workloads deployed on both runtimes               |
| Security, performance and quality testing | 1–2 weeks | Test evidence, failure analysis and quality scores     |
| TCO analysis and architecture decision    | 1 week    | Cost model, weighted scorecard and recommendation      |

Planning estimate: approximately 6–8 weeks for a focused evaluation, assuming access to both environments, available platform engineers, existing Kong and Dynatrace infrastructure, and no major networking or identity blockers. This is a planning estimate, not a vendor implementation commitment.

### Required acceptance criteria

I would require evidence that:

- 100% of tested LLM requests, including multi-step and sub-agent calls, traverse Kong.
- Direct model-provider access is denied where policy requires it.
- User-delegated and workload-identity authorization behave as expected.
- Tool calls are authorized independently of model output.
- Representative traces reach Dynatrace with the required correlation attributes.
- Quality and safety thresholds are met on a shared evaluation dataset.
- Latency and cost per successful task meet the business targets.
- Teams can deploy, roll back and troubleshoot an agent without bypassing governance.

The 100% gateway-routing requirement is a hard architectural control. The other thresholds should be defined based on business risk and workload requirements, not chosen arbitrarily.

## 15. Final architecture decision

My recommendation is to standardize the enterprise control plane and developer experience first, then select the default runtime based on the evidence from the proof of concept.

If the organization wants one default, use the following decision logic:

### Choose Foundry as the default when…

- Most teams need managed prompt agents and standard enterprise workflows.
- Native Entra identity and Azure integration substantially reduce implementation effort.
- The external Kong connection satisfies every model-call requirement.
- Foundry meets the custom-agent, observability and safety requirements without costly workarounds.

### Choose AgentCore as the default when…

- Teams need extensive framework freedom and custom orchestration.
- Isolated execution, modular agent capabilities and specialized tools are central.
- Entra integration, Kong routing and Dynatrace telemetry pass the same mandatory tests.
- Its runtime flexibility produces a measurable advantage in developer productivity, workload fit or TCO.

### Retain both as approved runtimes when…

- The use cases are materially different.
- Both pass the same security, Kong and Dynatrace standards.
- The organization can support two deployment paths without duplicating governance, tooling and operational teams unnecessarily.

For your environment, I would lean toward Foundry as the initial default for standard enterprise workflow agents if the pilot confirms the Kong and Dynatrace integration requirements, while keeping AgentCore as an approved runtime for use cases where its custom execution and framework flexibility provide demonstrable value.

That is a conditional recommendation, not a claim that Foundry is categorically superior. If AgentCore delivers better measured outcomes for your most important workloads and passes the same mandatory controls, the evidence should override the initial preference.

The most important architectural decision is to prevent the enterprise from becoming dependent on either runtime for identity, model routing, tool authorization, observability semantics and agent governance. Standardize those contracts centrally, keep Kong as the mandatory model path, and let the runtime be replaceable behind the enterprise platform.

Evidence note: The capability and pricing comparison uses the vendors' published documentation available in October 2026. Actual costs, service availability, feature maturity and supported integrations should be confirmed in the deployment regions and service configurations selected for your organization.


=============================================================




No. You do not need to run a full measured proof of concept for every use case on both AWS Bedrock AgentCore and Microsoft Foundry. That would be expensive, slow, and largely redundant.

As a Senior Agentic Architect, I would recommend a tiered evaluation strategy: architecture-based elimination first, representative workload testing second, and targeted testing only for unresolved differences.

The key is to distinguish between:

- Capabilities that can be assessed from architecture and documentation — identity integration, supported frameworks, regional availability, deployment models, governance features and service limits.
- Capabilities that must be demonstrated in your environment — mandatory Kong routing, Entra token propagation, Databricks authorization, Dynatrace trace continuity, real workload performance and actual cost.

This approach gives leadership a defensible decision without requiring every development team to build the same agent twice.

## 1. Recommended evaluation strategy

## 1

Architecture and capability screening

All use cases — no duplicate builds

Evaluate documentation, service boundaries, identity patterns, supported frameworks, regional availability, security controls, service limits and licensing. Eliminate a runtime for a use case if it cannot satisfy a mandatory requirement.

## 2

Representative workload PoC

3–4 archetypes

Build representative agents on both platforms. Focus on the integration risks that documentation cannot prove, then measure functional quality, security, latency, cost and developer effort.

## 3

Targeted exception testing

Only where needed

If a specific use case has a unique requirement—such as long-running execution, isolated browser automation or specialized memory—test that capability only when the architecture review cannot resolve the question.

## 4

Publish standards and exceptions

Select a default runtime, define approved agent patterns, document exceptions, and require teams to meet the same enterprise controls.

## 2. How many use cases should you actually test?

I would start with four representative agent archetypes, not every individual use case.

| Representative archetype              | What it validates                                                                            |
| ------------------------------------- | -------------------------------------------------------------------------------------------- |
| 1. Enterprise RAG assistant           | Retrieval quality, permissions, Entra identity, Azure data access and Databricks integration |
| 2. Tool-using business agent          | MCP/API calls, Kong mediation, authorization, retries and error handling                     |
| 3. Code-first or multi-agent workflow | Framework flexibility, orchestration, state management, scalability and debugging            |
| 4. High-risk or sandboxed agent       | Prompt injection, guardrails, browser/code isolation, policy enforcement and auditability    |

Run the same archetypes on both platforms where the comparison is necessary. You do not need to recreate every business-specific workflow.

For example, if 15 teams have agents that all follow the same RAG pattern, one representative implementation can validate the runtime pattern. The teams' individual applications can then undergo conformance testing against the approved standard.

The important caveat: if a particular agent has materially different security, latency, data-access or execution requirements, it may need its own targeted test.

## 3. What should be tested once versus per use case?

Enterprise platform controls

Test once per platform pattern

Validate Entra authentication, Kong routing, Dynatrace trace correlation, private connectivity, secret management, deployment controls and baseline policy enforcement. Retest when the underlying architecture or configuration changes.

Workload performance and economics

Test by archetype

Measure task success, p95 latency, token usage, tool-call volume, throughput, retries, runtime consumption and cost per successful task under representative load.

Application conformance

Test each production agent

Validate that each agent uses approved tools and identity scopes, meets its own quality and safety requirements, respects data permissions, and emits the required telemetry. This is a lighter conformance test—not a full head-to-head runtime comparison.

This distinction matters because the platforms already provide different abstractions for managed agents, custom code, tools and telemetry. Foundry supports prompt-based and hosted code agents, while AgentCore provides modular runtime services that can be adopted independently. Those differences can be assessed at the architecture level before duplicating implementations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learn.microsoft.com\&sz=32)

Microsoft Learn+1



## 4. Use mandatory gates before a weighted scorecard

I would not let a high feature score compensate for a critical architectural failure.

| Mandatory gate | Pass criteria                                                                      |
| -------------- | ---------------------------------------------------------------------------------- |
| Entra ID       | Approved human and workload identity flows; least-privilege access                 |
| Kong           | All required model calls, including retries and secondary paths, pass through Kong |
| Dynatrace      | End-to-end trace correlation across runtime, gateway, model and tools              |
| Databricks     | Correct authentication and data permissions; unauthorized access is denied         |
| Security       | No unacceptable bypass, cross-user data leakage or uncontrolled tool execution     |
| Economics      | Meets the agreed budget and workload performance targets                           |

If a runtime fails a mandatory gate, either eliminate it for that workload or document a specific, approved remediation. Only score the eligible candidates against developer experience, portability, operational overhead, resilience and total cost of ownership.

## 5. A better way to reach the final decision

Use a two-level standard:

- Level 1 — Enterprise standard: Choose the preferred runtime for the common agent patterns, with reusable identity, gateway, telemetry, security and CI/CD integrations.
- Level 2 — Approved exceptions: Allow the alternative runtime only where a documented capability or business requirement justifies the additional operational complexity.

For your environment, Microsoft Foundry is a reasonable initial candidate for the default because of the Azure data estate and Entra ID alignment. AgentCore should remain a genuine contender, particularly for modular runtime capabilities and isolated execution. Neither should be declared the winner until the mandatory Kong and Dynatrace integrations are proven.

The final decision should be based on the smallest test set that resolves the meaningful uncertainties—not the largest number of duplicated demos.

## Tailor the evaluation to your environment

If you want to refine the test plan for your organization, these details would materially affect how many PoCs are necessary.

Answering these will help size the evaluation and avoid unnecessary duplicate testing.



Refine the test plan

==============================================
