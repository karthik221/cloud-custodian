I would approach this as an Azure Strategic Architecture and Workload Alignment Session, rather than a conventional vendor review or technical status meeting.

As a Senior Lead, your role is to bring three groups together:

1. Azure vendor team: Understand Microsoft's roadmap, architectural direction, service changes, capacity outlook, and how they can better support the organization.
2. Application and development teams: Surface workload needs, architectural dependencies, upcoming changes, operational challenges, and future demand.
3. Cloud leadership / architecture: Connect business and technology priorities, identify risks and opportunities, and translate the discussion into an actionable cloud strategy.

The most important thing is to avoid making this a session where Microsoft presents slides and development teams simply listen.

You want a two-way strategic discussion where both sides understand what is coming, what needs to change, and what actions need to happen over the next 12–18 months.

I recommend a 90-minute session, supported by a structured facilitation document.

# 1. Recommended session structure

Recommended format# Azure Strategic Alignment & Architecture Review

Cloud Vendor + Application Engineering + Architecture

Duration: 90 minutes | Frequency: Quarterly or semi-annually

## Agenda

1

Opening & strategic context

Purpose, expectations, and desired outcomes

0:00–0:15

15 min

2

Application and workload outlook

Development team priorities, architecture, and demand

0:15–0:30

15 min

3

Architecture evolution & platform roadmap

Dremio, Azure services, AI, analytics, and architectural changes

0:30–0:55

25 min

4

Capacity, cost & infrastructure planning

Azure capacity, reservations, commitments, and optimization

0:55–1:10

15 min

5

Vendor partnership & open issues

Support, escalation, collaboration, and unresolved blockers

1:10–1:20

10 min

6

Decisions, actions & closing

Commitments, owners, next steps

1:20–1:30

10 min

# 2. Your opening remarks – 15 to 20 minutes

This is probably the most important part of your role as facilitator.

You should establish the context, explain why the session matters, set expectations for both teams, and frame the conversation around the next 12–18 months.

I would structure your opening into five sections.

## Part A – Welcome and purpose (3 minutes)

Suggested speaking notes:

"Thank you, everyone, for making the time today.

The objective of this session is to bring our Azure vendor partners and our application and development teams together to have a forward-looking discussion about our Azure environment.

We have an increasing dependency on cloud platforms to support our business applications, data platforms, analytics, and emerging technology capabilities.

As our workloads evolve, so do our infrastructure requirements, architectural dependencies, capacity needs, and expectations from our cloud providers.

We want to make sure that we are not just reacting to immediate technical requirements or resolving issues as they arise. We want to be more proactive in understanding where our architecture is heading, what changes are coming, and how we can collectively prepare for them.

This is an opportunity for both sides to share perspectives.

We want the development teams to articulate where their platforms and workloads are going, what challenges they are experiencing, and what they anticipate needing from Azure.

Equally, we want our Azure partners to share their perspective on the platform roadmap, emerging capabilities, architectural recommendations, and opportunities where they can help us improve our environment.

Ultimately, the goal is to move from a transactional vendor relationship to a more strategic and collaborative partnership."

## Part B – Why are we having this discussion now? (3–4 minutes)

Frame the discussion around four drivers.

1. Architecture is evolving

Our application landscape is not static. We are seeing changes in how applications consume cloud services, how data is stored and processed, and how platforms integrate with one another.

We need visibility into architectural changes that could influence our existing Azure footprint.

2. Data and AI are changing workload requirements

Data platforms, analytics, AI, and potentially new workloads are creating different infrastructure and capacity requirements.

We need to understand what the development teams are planning and whether our existing Azure architecture is positioned to support those requirements.

3. Capacity and financial planning need to become proactive

We should not wait until teams encounter capacity constraints or increased consumption before engaging Microsoft.

We need to understand future demand, regional capacity considerations, consumption patterns, and opportunities to optimize costs through Azure reservations and other commitment mechanisms.

4. We want to get more value from our Azure partnership

We want Microsoft to be more than a point of escalation when something goes wrong.

We should be leveraging their architecture expertise, product roadmap visibility, engineering resources, and proactive recommendations.

## Part C – What do we want to accomplish? (3 minutes)

"I would like us to leave this meeting with a much clearer understanding of five things."

- Future workload direction: What are the development teams planning over the next 12–18 months?
- Architectural evolution: What major platform changes, integrations, or technology decisions are being considered?
- Azure roadmap alignment: Are there changes or capabilities in Azure that we should be preparing for?
- Capacity and commercial planning: What demand should we factor into our future Azure capacity and reservation strategy?
- Partnership opportunities: Where can Microsoft provide more proactive support and add value?

Emphasize that the objective is not necessarily to solve every issue during this meeting. It is to identify the right issues, establish priorities, and agree on ownership.

## Part D – Set expectations for the discussion (3 minutes)

I would explicitly establish the following ground rules:

- Be forward-looking, not just focused on current incidents.
- Encourage open discussions about architectural challenges and concerns.
- Surface dependencies early, especially those that could affect production workloads.
- Distinguish between confirmed plans and potential future initiatives.
- Where there are technical disagreements, capture them for deeper architectural discussion.
- Focus on outcomes, decisions, and actions rather than lengthy product presentations.

One important statement:

"I would encourage both teams to be candid. If there are limitations in the current Azure services, concerns around platform direction, or gaps in how we are supporting our workloads, this is the right forum to bring them forward."

## Part E – Transition into the discussion (2–3 minutes)

"I would like to start by hearing from the development teams.

Before we get into the Azure roadmap or specific services, it is important that we understand where the workloads are today and where they are heading.

Once we establish that context, we can have a much more meaningful discussion with Microsoft about how Azure can support those requirements and what we need to plan for.

Let's use this as a working session rather than a presentation-driven meeting."

# 3. Main discussion topics and questions

This is the core of your facilitation guide. I would organize the conversation into five themes.

## Theme 1: Application and workload evolution

Development teams leadObjective: Understand how application workloads and their Azure dependencies are likely to change.

Questions to ask:

1. What are the major changes planned for your application or platform over the next 12–18 months?
2. Do you anticipate significant increases in data volumes, transaction volumes, compute, storage, or network consumption?
3. Are there plans to introduce new services, technologies, or integrations?
4. Are there architectural changes being considered that could impact the current Azure footprint?
5. Are there any known scalability, resiliency, performance, or availability concerns?
6. Are there dependencies on specific Azure regions, services, or capabilities that we should be aware of?

Your follow-up as facilitator:

- Is this a committed roadmap item or still under consideration?
- What Azure services will be affected?
- What additional capacity or infrastructure might be required?
- When do you expect the change to happen?
- Does this require Microsoft engagement now?

The goal is to turn general statements such as "we expect significant growth" into actionable workload forecasts.

## Theme 2: Dremio and data platform strategy

Joint discussionThis is an important topic because Dremio is already part of the application team's data architecture.

Rather than simply asking whether Dremio will continue to be used, I would frame the conversation around its strategic role.

Suggested opening:

"Today, we understand that the development teams are leveraging Dremio as a SaaS-based data platform.

As the organization's data and analytics strategy evolves, we want to understand how this platform fits into the future architecture and what that means for our Azure environment."

Questions for the development teams:

- What role does Dremio currently play in our data architecture?
- Is it primarily used for data virtualization, lakehouse analytics, SQL query federation, or a combination?
- What are the major use cases currently supported?
- Do you anticipate increased adoption across other application or analytics teams?
- Will data volumes, query concurrency, or workload complexity increase?
- Are there plans to expand into AI, advanced analytics, or additional data engineering workloads?
- Are there any plans to change the current Dremio architecture or its integration with Azure services?
- Are there opportunities to leverage Azure-native services alongside or instead of parts of the current architecture?

Questions for Microsoft:

- How does Microsoft see the evolution of lakehouse architectures on Azure?
- What is Microsoft's recommended architecture for Dremio SaaS running against Azure data services?
- Are there any emerging Azure capabilities that could complement our current implementation?
- How should we think about integration with Azure Data Lake Storage, Microsoft Fabric, and other data services?
- Are there architectural considerations around networking, identity, data access, latency, and security?
- What should we consider if Dremio usage expands significantly over the next 12–18 months?

A particularly valuable question:

"Are there architectural changes in the Azure data ecosystem that we should be aware of today, which could influence our investment or dependency on the current Dremio architecture over the next 12–18 months?"

This encourages Microsoft to provide strategic guidance without making the discussion an unnecessary Dremio-versus-Microsoft product comparison.

## Theme 3: Azure roadmap and architectural changes

Microsoft leadsObjective: Understand what is changing in Azure and whether those changes affect existing or future workloads.

Questions:

- What are the major Azure platform developments over the next 12–18 months that are relevant to our workloads?
- Are there any significant changes to Azure services that our teams currently depend on?
- Are there any planned deprecations, retirements, SKU changes, or regional availability considerations?
- Are there new capabilities around data, AI, analytics, networking, and compute that we should evaluate?
- Are there opportunities to modernize existing architectures using newer Azure services?
- Are there known limitations around service quotas, regional capacity, or performance?
- What architectural patterns would Microsoft recommend for our workload profile?

I would specifically ask Microsoft to distinguish between:

- Generally available capabilities.
- Public preview capabilities.
- Planned roadmap items.
- Strategic recommendations that require further validation.

This avoids building future architecture plans around capabilities that are not yet production-ready.

## Theme 4: Capacity planning, reservations and cost optimization

Joint discussionThis is where you want to connect the development roadmap to commercial and infrastructure planning.

Suggested framing:

"We want to move toward a more predictive approach to Azure consumption and capacity planning. As teams forecast future workload growth, we should understand what opportunities exist to plan ahead, optimize consumption, and potentially leverage Azure reservations or other commitment-based pricing models."

Questions for development teams:

- What are your expected compute, storage, and database consumption trends?
- Are there predictable baseline workloads that run consistently?
- Do you expect increased demand due to new applications, data growth, or AI workloads?
- Are there any upcoming migrations or major deployments?
- Are there workloads that are currently over-provisioned or underutilized?

Questions for Microsoft:

- Based on our consumption profile, where do you see opportunities for Azure Reservations?
- Are there workloads suitable for Azure Reserved VM Instances, Azure Savings Plans for Compute, or reserved capacity for eligible services?
- Are there opportunities to optimize Azure SQL, storage, networking, or other service costs?
- Can Microsoft help us build a 12-month capacity forecast?
- Are there regional capacity constraints we should plan for?
- Can we establish a recurring capacity and consumption review with Microsoft?

One important distinction: Reservations are not universally available across Azure services. Eligibility, flexibility, scope, and commitment terms vary by service. For Dremio SaaS specifically, we should not assume that Dremio subscription costs or its underlying SaaS infrastructure are eligible for Azure reservations.

Desired outcome: A joint Azure consumption and capacity planning exercise with identified workloads, forecasts, and potential commitment opportunities.

## Theme 5: How can Microsoft become a better partner?

Open discussionI would dedicate meaningful time to this topic.

You want to move beyond the standard vendor relationship.

Ask the development teams:

- Where do you feel Microsoft support has been effective?
- Where have you experienced challenges or delays?
- Are there recurring technical issues that require better escalation?
- Are there areas where Microsoft could provide more architectural guidance?
- What support would help accelerate delivery or reduce operational complexity?

Ask Microsoft:

- What additional resources can you make available to our development teams?
- Can we establish regular architecture advisory sessions?
- Can we have proactive reviews of major architectural changes?
- Can Microsoft provide early visibility into relevant service roadmaps and upcoming changes?
- Can we establish a clearer escalation path for production-critical issues?
- Can we jointly identify opportunities for optimization and modernization?

A strong question to close this section:

"If you were in our position, managing this Azure environment and planning for the next 18 months, what are the three things you would prioritize that we may not be considering today?"

This often generates a more valuable discussion than simply asking Microsoft what services they want us to adopt.

# 4. How to steer the conversation as the Senior Lead

This is where you add the most value.

You are not expected to be the deepest technical expert in every application or Azure service. Your responsibility is to connect the dots, challenge assumptions, and ensure the conversation produces actionable outcomes.

I would use the following approach.

| If the discussion becomes... | Your intervention |
| --- | --- |
| Too technical | "Can we connect this back to the broader architectural impact?" |
| Too focused on current incidents | "What does this mean for our future workload direction?" |
| A Microsoft product presentation | "How does this specifically address our application team's requirements?" |
| Too theoretical | "Can we identify a concrete use case in our environment?" |
| Focused on cost only | "What is the impact on performance, scalability, and operational risk?" |
| Unclear on ownership | "Who needs to take this forward, and by when?" |
| Focused on a future possibility | "Is this a committed initiative or something we are exploring?" |

I would also use three recurring questions throughout the meeting:

1. What changes? What is different from our current architecture?
2. What is the impact? Does it affect capacity, cost, security, performance, availability, or operations?
3. What action is required? Do we need a decision, investigation, roadmap update, or vendor engagement?

These three questions will keep the session focused.

# 5. Capture outcomes in a structured action tracker

Do not allow the meeting to end with only discussion notes.

Use this table throughout the session.

| Topic | Observation / decision | Owner | Target date |
| --- | --- | --- | --- |
| Dremio architecture | Validate future platform direction | Development + Architecture | TBD |
| Data growth | Develop 12-month consumption forecast | Development team | TBD |
| Azure roadmap | Identify relevant upcoming service changes | Microsoft | TBD |
| Capacity planning | Assess reservation opportunities | Cloud FinOps + Microsoft | TBD |
| Architecture | Review future data/AI requirements | Architecture + Microsoft | TBD |
| Vendor partnership | Define escalation and advisory model | Cloud leadership + Microsoft | TBD |

I would classify every outcome into one of four categories:

- Decision: Something agreed upon during the meeting.
- Action: Something that needs to be completed.
- Risk: Something that could affect workload delivery or stability.
- Opportunity: Something that could improve cost, architecture, performance, or business value.

# 6. Closing remarks – 3 to 5 minutes

Your closing should reinforce the strategic intent and create accountability.

Here is how I would deliver it.

Suggested closing script:

"Thank you, everyone. I think this has been a valuable discussion, and I appreciate the openness from both the development teams and our Microsoft partners.

A few important themes came through today.

First, our Azure environment needs to evolve alongside our application and data platforms. We need to maintain visibility into where our workloads are heading, particularly as we see increased requirements around data, analytics, and AI.

Second, we need to be more proactive about capacity and financial planning. Understanding future consumption patterns early will allow us to make better infrastructure decisions, take advantage of appropriate commercial opportunities, and avoid reacting to capacity constraints when they arise.

Third, our architectural decisions should be informed by both our internal technology roadmap and Microsoft's platform direction. We want to ensure that the investments we make today continue to support our longer-term objectives.

And finally, I want to emphasize the importance of the partnership. We would like to establish a more proactive engagement model with Microsoft, where we have regular architecture discussions, better visibility into relevant roadmap changes, and earlier involvement when significant workload changes are being planned.

I would ask that we take the actions captured today, assign clear ownership, and ensure that we follow through on them.

We should also treat this as an ongoing engagement rather than a one-time meeting. Ideally, we should establish a regular forum where we can revisit workload evolution, architectural changes, capacity, and emerging opportunities.

Thank you again for your time and contributions."

# 7. Suggested presentation deck

For the actual meeting, I would use an 8-slide PowerPoint deck. Keep it relatively light on text and use the facilitation document as your speaking guide.

Proposed PowerPoint structure

8 slides

Cloud Computing’s Impact on Enterprise Architecture, Governance, and Project Delivery

01. Session purpose

Strategic alignment, goals and outcomes.

Cloud Strategy Keynote Template | Nulivo Market

02. Why now?

Workload evolution, data, AI and capacity.

Effective Tech Strategy Planning for Growth

03. Workload outlook

Development roadmap for 12–18 months.

Architecture Benefits Of Databricks Lakehouse Platform at Landon Artis blog

04. Data platform evolution

Dremio, Azure data services, AI and analytics.

Cloud Strategy PowerPoint Template | Nulivo Market

05. Azure roadmap

Service changes, modernization and dependencies.

Transforming Our Internal Microsoft Azure Spend Forecasting

06. Capacity and FinOps

Forecasting, reservations and optimization.

Top 10 Business Technology Partnership PowerPoint Presentation Templates in 2025

07. Strengthening partnership

Support, escalation and architecture advisory.

Top 10 Restructuring Timeline PowerPoint Presentation Templates in 2026

08. Decisions and next steps

Actions, owners, dates and follow-up.

# 8. My recommendation: Make this a recurring strategic forum

I would not position this as a one-off Azure meeting.

Establish a recurring Azure Workload & Architecture Alignment Forum with the following operating model:

| Element | Recommendation |
| --- | --- |
| Frequency | Quarterly |
| Duration | 90 minutes |
| Chair | Cloud / Infrastructure Senior Lead |
| Participants | Microsoft, development leads, solution architects, cloud engineering, FinOps |
| Core focus | Architecture, roadmap, workload evolution, capacity, cost |
| Output | Decisions, risks, action tracker and forward-looking roadmap |

I would also introduce a simple forward-looking view:

12–18 month strategic outlook

1. 0–3 months: Understand
   Baseline workloads, identify open architectural issues, establish consumption and capacity visibility.
2. 3–6 months: Plan
   Validate architectural direction, identify Azure modernization opportunities, assess reservations and capacity requirements.
3. 6–12 months: Execute
   Implement agreed optimizations, address architectural gaps, and prepare for new workloads.
4. 12–18 months: Evolve
   Reassess data and AI architecture, platform capabilities, scalability, and future cloud strategy.

# 9. The actual facilitation document

I would use the following as the working document for the meeting. It is designed to be shared with the Azure vendor team and development leads before the session, so participants arrive prepared rather than seeing the questions for the first time.

Writing

# Azure Strategic Alignment & Workload Architecture Review

**Meeting:** Azure Vendor & Development Teams Strategic Alignment\
**Duration:** 90 minutes\
**Facilitator:** Cloud / Infrastructure Senior Lead\
**Participants:** Microsoft Azure Account & Technical Teams, Application Development Leads, Solution Architects, Cloud Engineering, FinOps

## 1\. Meeting purpose

Establish a forward-looking discussion between Microsoft Azure and internal development teams to understand workload evolution, architectural changes, Azure platform direction, capacity requirements, and opportunities to strengthen the partnership.

The objective is to proactively align our Azure environment with application and business requirements over the next 12–18 months.

## 2\. Desired outcomes

By the end of the session, we aim to:

- Understand major application and workload changes planned over the next 12–18 months.
- Identify architectural changes and Azure dependencies that require attention.
- Understand the future role of Dremio and the broader data and analytics architecture.
- Obtain visibility into relevant Azure roadmap developments.
- Identify capacity requirements and potential reservation opportunities.
- Identify areas where Microsoft can provide greater architectural and operational support.
- Agree on clear actions, owners, and timelines.

## 3\. Agenda

| Topic | Duration | Lead |
| --- | --- | --- |
| Opening and strategic context | 15 min | Senior Lead |
| Application and workload outlook | 15 min | Development Teams |
| Architecture, Dremio and Azure roadmap | 25 min | Joint |
| Capacity, reservations and optimization | 15 min | Joint / Microsoft |
| Partnership and open issues | 10 min | Joint |
| Decisions and closing | 10 min | Senior Lead |

## 4\. Discussion guide

### A. Application and workload evolution

- What are the major workload changes anticipated over the next 12–18 months?
- What growth is expected in compute, storage, data volumes and transactions?
- Are there new applications, integrations, or platform dependencies planned?
- Are there anticipated scalability, performance, resiliency, or availability concerns?
- Are any major migrations or architectural changes being considered?

### B. Data platform and Dremio strategy

- What is the current role of Dremio in our data architecture?
- How do we see its role evolving over the next 12–18 months?
- Will adoption, data volumes, query concurrency, or analytics use cases increase?
- Are there plans to expand into AI, advanced analytics, or additional data engineering workloads?
- Are changes anticipated to the current Dremio SaaS architecture or its Azure integrations?
- What Azure-native capabilities could complement our current architecture?
- What architectural considerations should we plan for around storage, networking, security, identity, and performance?

### C. Azure roadmap and architectural direction

- What upcoming Azure developments are most relevant to our workloads?
- Are there service retirements, deprecations, SKU changes, or regional considerations?
- What emerging capabilities should we evaluate for data, AI, analytics, compute, and networking?
- Are there opportunities to modernize existing architectures?
- What are Microsoft's recommendations based on our current workload profile?

### D. Capacity, consumption and reservations

- What are the expected Azure consumption trends over the next 12 months?
- Which workloads have predictable baseline consumption?
- Where could Azure Reservations or Savings Plans provide commercial value?
- Are there regional capacity or quota constraints?
- Can Microsoft support a joint capacity forecast and cost optimization assessment?

### E. Strengthening the Microsoft partnership

- What additional architecture and engineering support can Microsoft provide?
- Can we establish proactive architecture reviews?
- Can Microsoft provide earlier visibility into relevant platform roadmap changes?
- How can we improve technical escalation and issue resolution?
- What additional resources, programs, or expertise could benefit development teams?
- What three opportunities would Microsoft prioritize for our Azure environment?

## 5\. Key outputs and action tracker

| Discussion item | Classification | Owner | Due date | Status |
| --- | --- | --- | --- | --- |
| Dremio future architecture | Action | TBD | TBD | Open |
| Workload growth forecast | Action | TBD | TBD | Open |
| Azure roadmap assessment | Action | TBD | TBD | Open |
| Reservation opportunities | Action | TBD | TBD | Open |
| Architecture review | Action | TBD | TBD | Open |
| Vendor escalation model | Action | TBD | TBD | Open |

## 6\. Follow-up and governance

- Distribute meeting notes and decisions.
- Confirm owners and target dates for all actions.
- Escalate critical architectural dependencies where required.
- Establish a recurring quarterly alignment meeting.
- Review progress against the 12–18 month workload and architecture outlook.

**Success measure:** A shared understanding of our future Azure workload requirements, a prioritized set of architectural and capacity initiatives, and a more proactive working relationship with Microsoft.

## 10. One final piece of advice

As the Senior Lead, I would make one thing particularly clear at the beginning:

"We are not here simply to understand what Azure can offer us. We are here to align what our workloads need with where Azure is going, and to make sure we are making the right architectural and investment decisions together."

That statement sets the right tone. It establishes that the development teams own their workload direction, Microsoft brings its platform expertise, and you are facilitating the strategic alignment between the two.

It also positions you as a cloud strategy and architecture leader rather than simply the person coordinating a vendor meeting.


========================

=================================

Thanks, everyone. The goal today is to agree on a reusable way for teams to build and operate agents on Amazon Bedrock AgentCore. We’re not trying to choose one business use case or lock every team into one agent framework. We’re defining the shared platform patterns that let teams build safely and consistently.

The constraints we’re designing around are: model inference to Bedrock goes through Kong; agent identities and API authorization use Entra ID service principals; Dynatrace is our observability destination; and AgentCore Gateway is out of scope. Agents can also have IAM execution roles for AWS resource access.

I’d like us to leave with agreement on the three patterns, the identity model, how tools and optional memory fit, and the scope of a first proof of concept.”
1:30–3:00 | Explain the architecture principles
“The key design choice is to separate responsibilities. AgentCore Runtime hosts and runs agent code. Kong is the model access path. Entra establishes who is calling which API. IAM gives an agent permissions to AWS resources. Dynatrace is where we want teams to follow operational traces.

That means an agent should not have Bedrock credentials and call Bedrock directly. It should use a shared model client configured for Kong. It also means an Entra service principal and an AWS IAM role are different identities serving different purposes.

We should standardize these integration points and operational expectations, while leaving room for teams to choose the framework and the business logic that fits their work.”
3:00–5:30 | Walk through the single-agent pattern
“The simplest pattern is one application calling one agent hosted on AgentCore Runtime.

The calling application presents an Entra access token intended for the entry-agent API. The runtime validates the token. The agent handles the request and, when it needs a model, calls Kong. Kong applies the organization’s model policies and routes to Bedrock.

The agent’s Entra identity is not the same thing as the application’s identity. The caller has its own identity. The agent has its own service principal for outbound calls, such as calling Kong or an MCP server. The agent also has an AWS IAM execution role, used only for permitted AWS resource access.

For the first pattern, we should show one trace across the request path: application, AgentCore Runtime, Kong, Bedrock, and back. This establishes the foundation for the more complex patterns.”
5:30–8:00 | Explain multi-agent collaboration
“The second pattern introduces a supervisor or entry agent and one or more worker agents. The supervisor accepts the request, delegates a bounded subtask to a worker, and combines the result.

Each deployable agent has its own Entra service principal. When the entry agent calls a worker, it requests a token for the worker API using its own identity. When the worker calls Kong, it gets a token intended for the Kong API using the worker’s identity. Tokens are audience-specific; we shouldn’t reuse a token issued for one API at another API.

We should begin with a small, explicit workflow: one supervisor, one worker, a defined request and response schema, and a cap on delegation and tool calls. This gives us a useful multi-agent demonstration without starting with open-ended agent-to-agent routing.”
8:00–10:00 | Make the identity and Conditional Access separation clear
“I want to be precise about what we mean by ‘the agents use Entra.’

Each agent should have a dedicated workload identity, separate from the calling application and separate from other agents. The identity team can decide the registration and naming conventions, but the design should preserve one identity per independently deployable agent.

Conditional Access for workload identities belongs in Entra. It is a separate policy scope from user Conditional Access. Entra evaluates the applicable policy when the service principal requests a token. AgentCore then validates the token when it receives the API call. Those are related controls, but they are not the same step.

We should ask the identity team to confirm the app roles or claims, audiences, token version, credential approach, and Conditional Access scope. If location-based policies are required, we need to verify that agent token requests come from a suitable controlled egress path.”
10:00–12:00 | Cover MCP and tool calls
“The third pattern adds tools. We should distinguish local, approved tools from remote MCP tools.

A local tool runs within the agent’s environment. An MCP tool is offered by a separately managed MCP server. In both cases, the model should only be able to request tools that the platform or application has explicitly allowed. The agent validates the tool name and arguments, applies timeouts and output limits, and records the result.

For MCP, the agent uses its own identity to request a token for the MCP API. The MCP server makes the final authorization decision for each tool. We should not let the agent discover arbitrary servers or URLs.

For the PoC, I suggest one harmless local tool and one optional mocked MCP tool. We can prove the integration and authorization pattern without connecting a production system or giving the agent consequential permissions.”
12:00–14:30 | Place memory and knowledge in the picture
“Memory and knowledge are separate capabilities, and teams should adopt them only when the use case needs them.

Short-term memory is session context: what has been said in the current conversation. Long-term memory is durable information such as a preference or summary that may be useful in a later session. A knowledge base is different: it contains approved source material that the agent retrieves to answer a question. Workflow state is different again; it tracks process progress, such as which approval step is complete.

There’s an important policy detail here. If every model inference must go through Kong, we need to review managed memory strategies and managed knowledge-base ingestion carefully. Some managed features can make model or embedding calls outside the agent’s Kong client path.

For the PoC, I suggest memory is off by default. We can demonstrate short-term storage if desired, and keep long-term summaries behind Kong by having the agent generate them through the Kong client before storing them. For knowledge, retrieve source chunks separately and send those chunks to the model through Kong. Let’s treat any managed model calls outside Kong as an exception that needs an explicit decision.”
14:30–16:00 | Observability and operations
“Teams need to be able to follow one request end to end. We should use OpenTelemetry instrumentation in agent code and configure Kong telemetry to preserve trace context. The shared telemetry should include agent name, environment, workflow, model alias, tool name, request ID, latency, and outcome.

We should avoid putting credentials, access tokens, or sensitive prompts and responses into telemetry by default.

There is an integration task to resolve: AgentCore’s service-generated telemetry is delivered to CloudWatch, while application and Kong telemetry can be sent through OTLP to Dynatrace. If Dynatrace needs to be the unified operational view, we need to agree on how the CloudWatch telemetry reaches Dynatrace and confirm the traces can be correlated.”
16:00–18:00 | Propose the PoC and framework approach
“For the reference PoC, I recommend LangGraph for the multi-agent workflow because its state and transitions are explicit and reviewable. I’m proposing that as the example implementation, not as the required framework for every team. AgentCore Runtime can host different frameworks, and Strands is a strong AWS-oriented alternative.

The part we should standardize is the platform contract: the request and response shape, Kong model client, Entra token provider, MCP client, tool authorization, memory and knowledge interfaces, and OpenTelemetry fields. That allows a team to use a different framework without changing the platform controls.

The PoC should deliver two runnable variants: a single agent and an entry-plus-worker multi-agent flow. Both should call a mock model locally and use Kong for real inference. MCP should be optional, with a mocked path for local runs. The PoC should also show a real or mocked Entra token boundary and a trace that connects the components.”
18:00–20:00 | Close with decisions and next steps
“To close, I’d like us to confirm these decisions:
1. Do we agree on the single-agent, supervisor-worker, and MCP workflow patterns?
2. Does the identity team agree that each independently deployed agent gets its own Entra workload identity, with separate identities for calling applications?
3. What token claims, audiences, app roles, credentials, and workload Conditional Access rules should the PoC use?
4. What Kong endpoint and authentication method should the model client target?
5. Which Dynatrace OTLP path should we use, and how will we bring in AgentCore’s CloudWatch telemetry?
6. Are we comfortable with LangGraph as the reference PoC while keeping framework choice open?
7. Who will own the first single-agent and multi-agent demonstrations?
Once those owners and decisions are clear, we can build the paved road and run the PoC against these acceptance points: model inference only through Kong; caller and agent identities kept distinct; tools explicitly authorized; optional features disabled by default; and a trace that lets us investigate a request across the workflow.”

Suggested closing line: “The outcome we want is a repeatable platform pattern that teams can adopt without inheriting each other’s business logic or being forced into one framework.”



==============================
==========================================



# MCP Lifecycle & Governance: Strategic Questions for an Enterprise Architecture Review

If an Enterprise Architecture team is presenting an enterprise MCP (Model Context Protocol) lifecycle and governance framework, with Kong API Gateway as the standard gateway and Microsoft Entra ID as the identity provider, I would approach the discussion from the perspective of an enterprise architect, Python platform engineer, and agentic AI architect.

The objective should not simply be to validate whether MCP servers can be registered through Kong and authenticated through Entra ID.

The bigger questions are:

1. Are we creating a secure, scalable, reusable enterprise MCP ecosystem?
2. Who governs what an AI agent can discover, access, and execute?
3. How do we manage MCP servers throughout their lifecycle?
4. How do we prevent agentic AI from becoming an uncontrolled integration layer?
5. Are we establishing standards that will remain relevant as agentic architectures evolve?

I would divide the discussion into 12 governance areas, with questions designed to challenge the architecture constructively and identify opportunities to introduce new standards.

# 1. MCP architecture and enterprise reference architecture

Best MCP Registries in 2026: Compared for Developers and Enterprises

[truefoundry.com](<https://www.truefoundry.com/blog/best-mcp-registries?utm_source=chatgpt.com>)

Start by understanding the architectural boundaries.

Questions to ask:

1. Are we treating Kong as an MCP gateway, an API gateway with MCP support, or both? What responsibilities belong to the gateway versus the MCP server?
2. Will all MCP servers be required to register through Kong, including internally hosted and third-party MCP servers?
3. Are we establishing a centralized MCP registry or relying on Kong's service and route catalog as the source of truth?
4. How will agents discover available MCP servers and their tools?
5. Are we distinguishing between MCP server registration, MCP server discovery, and MCP server invocation?
6. What is the reference architecture for agent-to-MCP-to-enterprise-system communication?
7. How do we support multiple MCP transports and versions without introducing inconsistent security patterns?
8. How will the architecture support MCP servers deployed across Azure, on-premises, and other cloud environments?

Potential governance standard to propose:

Establish an Enterprise MCP Reference Architecture with mandatory patterns for:

- MCP server hosting.
- Gateway registration.
- Identity and authorization.
- Tool discovery.
- Backend connectivity.
- Logging and observability.
- Version management.
- Network segmentation.

An especially important question:

> Does Kong provide the complete MCP control plane, or are we expecting a separate enterprise MCP management layer for registry, discovery, lifecycle, and policy enforcement?

This is an important distinction. An API gateway does not automatically provide every capability needed for MCP governance.

# 2. Identity, authentication and authorization – Entra ID

Autenticación y autorización de API: información general - Azure API Management | Microsoft Learn

[learn.microsoft.com](<https://learn.microsoft.com/es-es/azure/api-management/authentication-authorization-overview?utm_source=chatgpt.com>)

This is arguably one of the most important discussions.

A common mistake is to assume that authenticating an AI agent through Entra ID automatically authorizes every tool that the agent can invoke.

Authentication and authorization must be treated separately.

Questions to ask:

1. What is the identity model for MCP clients, agents, MCP servers, and backend systems?
2. Will each agent have its own Entra ID application identity or service principal?
3. Are we using OAuth 2.0 authorization code flow, client credentials, or on-behalf-of (OBO) flow depending on the interaction?
4. How will we distinguish user-delegated access from agent-initiated service-to-service access?
5. Will each MCP server have its own Entra ID application registration?
6. How will Kong validate JWT tokens, including issuer, audience, expiry, signature, and scopes?
7. Who owns token acquisition, validation, refresh, and propagation?
8. How do we prevent a token issued for one MCP server from being reused against another?
9. Will tool-level permissions be enforced, or will authorization only happen at the MCP server level?
10. How will we implement least-privilege permissions for individual tools?
11. How will we handle managed identities and workload identity federation for MCP servers running in Azure?
12. What happens when a user loses access to a backend system but an agent still has previously acquired credentials?

### A particularly influential question

> Are we implementing identity propagation end-to-end, such that the MCP server can enforce the actual user's permissions in the target enterprise system, rather than relying only on the AI agent's application identity?

This is a critical Zero Trust consideration.

### Governance standards to propose

- Every production MCP server must have a registered workload identity.
- Every agent must have an identifiable application or workload identity.
- No shared credentials across unrelated agents or MCP servers.
- OAuth scopes and application roles must follow least privilege.
- Token audiences must be explicitly validated.
- User-delegated and application-level access must be clearly distinguished.
- Secrets must be stored in an enterprise secrets manager, not environment files or source code.
- High-risk tools must require explicit authorization beyond basic MCP server access.

# 3. MCP server registration and onboarding lifecycle

This is where you can influence the actual operating model.

Questions to ask:

1. Who is authorized to register a new MCP server with Kong?
2. Is registration self-service or controlled through an architecture approval process?
3. What information must a team provide before registration?
4. Will every MCP server undergo security assessment before becoming discoverable?
5. Are we maintaining an approved list of MCP server owners and business sponsors?
6. How do we distinguish development, testing, staging, and production MCP servers?
7. What is the process for onboarding external or vendor-provided MCP servers?
8. Can a team register a new MCP server without a defined business owner?
9. How are deprecated or abandoned MCP servers identified?
10. What happens if a registered MCP server becomes non-compliant?

### Suggested enterprise MCP onboarding lifecycle

## Proposed MCP governance lifecycle

1. Request & business justification
   Business use case, business owner, technical owner, data classification.
2. Architecture review
   MCP design, Python implementation standards, hosting, transport, backend integrations.
3. Security & identity review
   Entra ID registration, OAuth scopes, threat modeling, secrets, authorization.
4. Testing & certification
   Functional tests, security scans, tool-level authorization, performance and resilience.
5. Kong registration
   Service onboarding, routing, policies, authentication, rate limits and observability.
6. Production approval
   Architecture sign-off, operational ownership, documentation and support model.
7. Continuous monitoring
   Usage, failures, suspicious tool calls, policy violations and drift.
8. Versioning, recertification & retirement
   Periodic reviews, deprecation, access revocation and server removal.

Potential standard to introduce:

No MCP server should be promoted to production without an enterprise MCP onboarding checklist and a formal registration record.

# 4. MCP tool-level governance and authorization

High-priority governance opportunityThis is where I would push the architecture team beyond conventional API governance.

In traditional API architecture, access is often granted at the API or resource level. With MCP, an individual server can expose multiple tools, each with different capabilities and risk levels.

For example:

| MCP server | Tool | Risk |
| --- | --- | --- |
| HR MCP | Get employee details | Medium |
| HR MCP | Update employee details | High |
| Finance MCP | Get invoice status | Low |
| Finance MCP | Approve invoice | Critical |
| IT MCP | Search knowledge base | Low |
| IT MCP | Disable user account | Critical |

If access is granted to the entire MCP server, are we inadvertently granting access to all its tools?

Questions to ask:

1. Are we governing access at the MCP server level or individual tool level?
2. Can we assign different authorization policies to individual tools within the same MCP server?
3. Can Kong enforce tool-level policies, or must the MCP server implement them?
4. Who approves tools that can perform write, update, delete, approve, or execute operations?
5. Can we classify tools according to risk levels?
6. Will destructive operations require human-in-the-loop approval?
7. How do we prevent an agent from invoking a tool outside its intended business context?
8. Can tool permissions be restricted by user, agent, business role, environment, and data classification?

### A governance standard worth proposing: MCP Tool Risk Classification

Level 1 – Read-only

Low risk

Search, retrieve, summarize, and read enterprise data.

Level 2 – Controlled read

Moderate risk

Access sensitive employee, customer, financial, or confidential information.

Level 3 – Write operations

High risk

Create records, update systems, submit requests, modify configurations.

Level 4 – Critical actions

Critical risk

Approve payments, change access permissions, execute privileged commands, delete critical records.

Each level should have different approval, authentication, authorization, monitoring, and audit requirements.

A powerful question to ask:

> Should MCP tool permissions be managed as independently governed enterprise capabilities, rather than inheriting blanket permissions from the MCP server registration?

I would strongly advocate for this.

# 5. MCP server development standards – Python engineering perspective

This is an opportunity to influence the engineering standards, particularly if teams are building MCP servers using Python.

The objective should be to avoid every team implementing MCP servers differently.

Questions to ask:

1. Will we establish an approved Python MCP server framework or reference implementation?
2. Are teams expected to use an approved MCP SDK and supported version?
3. Will we publish standard templates for building MCP servers?
4. How will we enforce consistent input validation and output schemas?
5. Are tool descriptions and parameter descriptions required to follow a standard?
6. How will we manage exceptions, timeouts, retries, and connection failures?
7. Will all MCP tools implement structured error responses?
8. How will we handle asynchronous operations and long-running tools?
9. Will we enforce dependency scanning, container scanning, and software bill of materials (SBOM)?
10. How will we prevent developers from exposing internal Python functions directly as MCP tools without security review?

### Python engineering standards I would recommend

| Area | Proposed standard |
| --- | --- |
| SDK | Approved and version-pinned MCP SDK |
| Framework | Enterprise Python MCP starter template |
| Validation | Pydantic or equivalent schema validation |
| Authentication | Entra ID-integrated identity pattern |
| Logging | Centralized structured JSON logging |
| Secrets | Azure Key Vault or approved secrets manager |
| Testing | Unit, integration, contract and security tests |
| Packaging | Approved dependencies and lockfiles |
| Deployment | Approved container images |
| Security | SAST, SCA, secret scanning, container scanning |
| API contracts | Versioned tool schemas |
| Documentation | Standard tool catalog and ownership metadata |

### A useful architectural question

> Can we establish an enterprise-approved MCP server starter kit that comes with authentication middleware, structured logging, telemetry, input validation, exception handling, and security controls built in?

This could significantly reduce implementation inconsistencies.

### Example: Standardized MCP tool definition

For example, an MCP server should not expose a generic tool called `execute_query` that accepts arbitrary SQL.

Instead, teams should expose business-specific, narrowly scoped tools.

python

```python
from pydantic import BaseModel, Field

class InvoiceRequest(BaseModel):
    invoice_id: str = Field(
        min_length=1,
        max_length=50,
        description="Enterprise invoice identifier"
    )

async def get_invoice_status(
    request: InvoiceRequest,
    authenticated_user: str
):
    # Validate the user's business-level permissions.
    # Retrieve only authorized invoice information.
    # Apply timeout and audit logging.
    # Return a structured response.
    ...
```

The important principle is that an MCP tool should expose a controlled business capability, not unrestricted backend functionality.

# 6. Data governance, privacy and information protection

This is especially important because agents can retrieve information from multiple enterprise systems and combine it into a single response.

Questions to ask:

1. How will MCP servers inherit enterprise data classification standards?
2. Can we identify whether a tool exposes public, internal, confidential, or restricted data?
3. Are we enforcing row-level and field-level security at the backend?
4. Can an agent retrieve data that its invoking user would not normally be allowed to access?
5. How are PII, financial data, employee records, and regulated information protected?
6. Are sensitive data fields masked before being returned to the LLM?
7. What information is sent to model providers during tool invocation?
8. How do we prevent sensitive data from appearing in MCP logs and telemetry?
9. Are MCP tool outputs subject to DLP policies?
10. What are the retention and deletion requirements for MCP interaction records?

### Suggested new standard: Data Classification Metadata for Every Tool

Every MCP tool should declare:

- Data classification.
- Business data owner.
- Data source.
- Permitted user populations.
- Read/write capability.
- PII exposure.
- Retention requirements.
- Applicable regulatory restrictions.

Influential question:

> Can we make data classification a mandatory part of MCP tool registration, so that data protection policies are enforced consistently rather than depending on each development team?

I would also introduce the concept of data authorization at the point of retrieval, rather than relying exclusively on the agent or LLM to decide what information it should access.

# 7. Agentic AI security and prompt injection

Critical risk areaTraditional API security does not fully address agentic AI risks.

MCP introduces a new attack surface because tool descriptions, tool results, and external data can influence the behavior of an LLM.

Questions to ask:

1. How are we protecting MCP servers against prompt injection originating from retrieved documents or tool outputs?
2. Do we treat MCP tool responses as untrusted input?
3. Can an agent be manipulated into invoking an unintended tool?
4. How do we prevent unauthorized tool chaining?
5. Can one MCP tool's output influence another tool's execution without policy validation?
6. Are we scanning MCP server dependencies for malicious packages?
7. How are we validating third-party MCP servers before onboarding?
8. How do we protect against tool poisoning and malicious tool descriptions?
9. Are agents allowed to dynamically discover and invoke any registered MCP server?
10. Can we disable a compromised MCP server or tool centrally?

### Governance standards to propose

- Treat all external MCP tool outputs as untrusted data.
- Do not use LLM-generated reasoning as an authorization decision.
- Validate tool arguments on the server side.
- Require independent authorization for sensitive operations.
- Maintain approved MCP server and tool allowlists.
- Conduct prompt-injection and tool-abuse testing.
- Establish an emergency kill switch for tools and MCP servers.
- Require security review for changes to tool descriptions and schemas.

A question that can elevate the discussion:

> Are we governing not just what an agent can connect to, but also what an agent is allowed to do with the information and capabilities it discovers through MCP?

This is an important distinction between API governance and agentic governance.

# 8. Observability, auditing and operational governance

The architecture should establish end-to-end traceability.

Consider this scenario:

An employee asks an AI agent to check an invoice. The agent invokes a Finance MCP server through Kong, which accesses an ERP system.

Can we trace the entire transaction?

Questions to ask:

1. Can we trace a request from the user prompt to the agent, MCP server, individual tool, and backend API?
2. Does Kong generate or propagate a correlation ID across the entire flow?
3. Can we identify which user and which agent initiated a particular tool invocation?
4. Are tool invocations logged individually?
5. Can we distinguish successful, denied, failed, and timed-out tool calls?
6. Can we monitor unusual tool invocation patterns?
7. Can we detect an agent invoking an unusually large number of tools?
8. Can we identify repeated authorization failures?
9. What is the audit retention period?
10. Can security teams reconstruct the sequence of actions performed by an agent?

### Proposed enterprise observability model

## End-to-end MCP audit trail

User / Business Identity

Entra ID identity and authorization context

AI Agent

Agent ID, session ID, model and request ID

Kong Gateway

Authentication, authorization, policy decisions and correlation ID

MCP Server and Tool

Server ID, tool name, arguments metadata, outcome and duration

Enterprise Backend

Backend identity, operation, transaction reference and result

Centralized monitoring and audit

SIEM, security analytics, distributed tracing, alerting and compliance reporting.

A key point: do not assume that Kong alone can capture the full agent-to-tool execution context. The agent runtime, MCP server, and backend must also propagate appropriate trace and audit information.

Potential governance standard:

Every production MCP tool invocation must produce an auditable event with:

- User or calling workload identity.
- Agent identifier.
- MCP server identifier.
- Tool name.
- Correlation and trace identifiers.
- Authorization outcome.
- Timestamp and duration.
- Backend transaction reference, where applicable.

Avoid logging raw prompts, access tokens, secrets, or unrestricted sensitive tool arguments.

# 9. MCP versioning, change management and deprecation

MCP is an evolving protocol. The enterprise architecture should avoid tightly coupling agents to individual MCP server implementations.

Questions to ask:

1. Who owns MCP protocol version adoption across the enterprise?
2. How will we manage backward compatibility when an MCP server changes its tool schema?
3. If a tool's input parameters change, how will dependent agents be notified?
4. Will we maintain versioned tool contracts?
5. Can an MCP server support multiple versions simultaneously?
6. How will we manage breaking changes?
7. What is the approval process for introducing new tools to an existing server?
8. Will every material change trigger security recertification?
9. How will we identify agents consuming deprecated MCP tools?
10. What is the process for revoking a server's Kong registration and Entra ID permissions?

### Proposed standard

Introduce an MCP Change Management Policy:

- Semantic versioning for MCP server releases.
- Explicit versioning for tool contracts.
- Compatibility testing before production promotion.
- Consumer impact assessment before breaking changes.
- Defined deprecation notice periods.
- Automated dependency discovery.
- Mandatory reapproval for material security changes.

A particularly good question:

> If an MCP server changes its tool description, schema, or permissions, do we treat this as a normal application release or as a potentially security-relevant change requiring recertification?

I would advocate for risk-based recertification.

# 10. Third-party MCP servers and supply chain governance

This area deserves special attention because MCP servers can be developed internally, sourced from vendors, or obtained from public repositories.

Questions to ask:

1. Are public GitHub MCP servers allowed in the enterprise?
2. Is there an approved MCP server catalog?
3. Can development teams directly install community-maintained MCP servers?
4. Who validates the publisher and source code?
5. How do we identify malicious dependencies or compromised packages?
6. Are we requiring source code review for third-party MCP servers?
7. How do we manage vendor updates and security patches?
8. Can a third-party MCP server send data outside the enterprise?
9. What happens if a vendor discontinues support?
10. Are we tracking software licenses and intellectual property risks?

### Suggested governance standards

- Maintain an approved MCP server repository.
- Require software provenance and SBOM.
- Conduct dependency and vulnerability scanning.
- Require vendor and source-code risk assessments.
- Block unapproved external MCP endpoints.
- Apply network egress restrictions.
- Maintain an inventory of third-party MCP dependencies.
- Require explicit approval for data transfers to external providers.

Influential question:

> Should third-party MCP servers go through the same onboarding and certification process as enterprise APIs, with additional AI-specific security checks?

My recommendation would be yes.

# 11. Scalability, resilience and runtime governance

The team may focus heavily on registration and authentication. However, MCP servers are also runtime dependencies of agents.

Imagine an enterprise agent depending on five MCP servers. If one server is unavailable, what happens to the overall agent workflow?

Questions to ask:

1. What are the expected availability SLAs for enterprise MCP servers?
2. Will Kong enforce rate limiting and request quotas?
3. How will we prevent one agent from overwhelming a shared MCP server?
4. Are we implementing concurrency limits and backpressure?
5. What happens when an MCP server becomes unavailable?
6. Are retry policies standardized?
7. How do we prevent duplicate execution of non-idempotent tools?
8. Are long-running operations handled asynchronously?
9. How will we monitor tool response latency and error rates?
10. Will critical MCP servers have disaster recovery and failover arrangements?

### Suggested standards

| Capability | Governance recommendation |
| --- | --- |
| Availability | Service-tier-based SLAs |
| Rate limits | Per agent, client and tool |
| Timeouts | Standardized per tool risk and operation |
| Retries | Bounded retries with backoff |
| Idempotency | Required for retryable write operations |
| Circuit breakers | For unstable downstream services |
| Scaling | Autoscaling and capacity management |
| Health checks | Standard health and readiness checks |
| DR | Recovery objectives based on business criticality |

Important question:

> Will we govern MCP servers as production enterprise services with SLAs, SLOs, capacity planning, and operational ownership, rather than treating them as lightweight AI utilities?

This is a very strong architecture discussion point.

# 12. Enterprise MCP operating model and ownership

One of the biggest governance gaps in emerging AI platforms is unclear ownership.

Who is accountable when something goes wrong?

For example:

- The agent team says the MCP server returned bad information.
- The MCP team says the backend API returned bad information.
- The API team says the request was authorized through Kong.
- The security team says the identity token was valid.

There needs to be an explicit operating model.

### Questions to ask

1. Who owns the enterprise MCP platform?
2. Who approves new MCP server registrations?
3. Who owns the Entra ID application registrations?
4. Who manages Kong policies and gateway configurations?
5. Who owns individual MCP servers and their exposed tools?
6. Who is responsible for tool-level authorization?
7. Who handles security incidents involving agents?
8. Who owns the enterprise MCP catalog?
9. Who performs periodic compliance assessments?
10. Who can revoke an MCP server or individual tool in an emergency?

### Proposed ownership model

| Stakeholder | Responsibility |
| --- | --- |
| Enterprise Architecture | Reference architecture and design standards |
| AI Platform Team | Agent runtime and MCP platform capabilities |
| API Platform Team | Kong gateway, policies and routing |
| IAM/Security Team | Entra ID, OAuth, permissions and security controls |
| MCP Server Owner | Tool functionality, business logic and operations |
| Data Governance | Data classification and access policies |
| SOC | Threat detection and incident response |
| Business Owner | Business justification and risk acceptance |

I would recommend establishing an Enterprise MCP Governance Council with representation from Enterprise Architecture, AI Platform, API Platform, Cybersecurity, IAM, Data Governance, and business stakeholders.

# 13. Five additional strategic areas that can influence future standards

These are areas I would raise if the architecture presentation is focused primarily on today's MCP onboarding process.

## A. MCP registry versus gateway registry

A gateway registry and an MCP registry solve related but different problems.

Ask:

> Are we planning to establish a central enterprise MCP catalog that maintains server metadata, tool definitions, ownership, risk classifications, supported versions, and consumer dependencies independently of the gateway routing configuration?

A potential standard:

The enterprise MCP catalog should maintain:

- MCP server name and unique identifier.
- Business capability.
- Technical and business owner.
- Kong registration reference.
- Entra ID application identity.
- Tool names and descriptions.
- Risk classification.
- Data classification.
- Environment and version.
- Approved consumers.
- Lifecycle status.

This would help prevent Kong from becoming the only place where MCP inventory is maintained.

## B. Agent-to-agent and multi-agent governance

As agentic architecture evolves, agents may invoke other agents, which then invoke MCP servers.

Ask:

> How will we govern delegated authority when an agent invokes another agent that subsequently invokes an MCP tool?

For example:

Orchestrator Agent

HR Agent

Finance Agent

HR MCP

Employee tools

Finance MCP

Invoice tools

Each delegated interaction needs traceable identity and authorization.

Potential standard:

- Explicit agent identity.
- Delegation boundaries.
- Permission inheritance rules.
- No automatic privilege escalation.
- End-to-end auditability.
- Explicit authorization for cross-agent actions.

## C. Human-in-the-loop governance

Ask:

> Should human approval be a standard capability for high-impact MCP tools, rather than something every agent development team implements independently?

I would suggest defining reusable approval patterns for:

- Financial transactions.
- User access modifications.
- Data deletion.
- External communications.
- Production infrastructure changes.
- Sensitive employee-data operations.

Approval should be enforced at a trusted execution boundary, not simply requested by the LLM.

## D. MCP discovery and shadow MCP prevention

Ask:

> How do we ensure that teams do not independently expose MCP endpoints outside Kong, creating shadow MCP servers that bypass enterprise identity and governance?

Potential standards:

- Approved network paths.
- Private connectivity wherever applicable.
- Egress restrictions.
- Endpoint discovery and scanning.
- CI/CD compliance checks.
- Automated inventory reconciliation.
- Detection of unregistered MCP services.

## E. MCP governance automation

This is an opportunity to move from manual governance to policy-as-code.

Ask:

> Can we automate MCP compliance validation in the CI/CD pipeline, so that non-compliant MCP servers cannot be deployed or registered into production?

For example:

yaml

```yaml

mcp_governance:
  identity:
    entra_id_required: true
    workload_identity_required: true
    token_validation_required: true

  gateway:
    kong_registration_required: true
    approved_environment_required: true

  security:
    tool_risk_classification_required: true
    input_validation_required: true
    secrets_scanning_required: true
    dependency_scanning_required: true

  observability:
    structured_logging_required: true
    distributed_tracing_required: true
    audit_events_required: true

  lifecycle:
    business_owner_required: true
    technical_owner_required: true
    versioning_required: true
    security_review_required: true
```

This is illustrative policy configuration, not a built-in Kong or MCP configuration format.

The broader opportunity is to make governance enforceable and measurable, rather than relying on documentation and review meetings.

# 14. Important Kong + Entra ID architecture considerations

There are a few implementation-specific points I would explicitly validate with the architecture team rather than assuming they are covered by the standard.

Kong's current AI Gateway documentation describes an AI MCP Proxy that can expose existing APIs as MCP tools or proxy upstream MCP servers. It also documents per-tool ACL controls in supported configurations. This means the architecture should evaluate the capabilities already available before building custom governance components.

Kong Docs

+1

| Architecture capability | What to validate |
| --- | --- |
| MCP protocol support | Which Kong MCP proxy mode is being standardized? |
| Authentication | Are we using OIDC or the MCP-specific OAuth implementation? |
| Tool authorization | Are per-tool ACLs enabled and centrally governed? |
| Registry | Is Konnect Catalog being used, or is a separate registry required? |
| Observability | Are MCP-specific audit logs and metrics enabled? |
| Identity propagation | Does the upstream receive the correct delegated identity? |
| External MCP | How are third-party upstream servers authenticated? |

### Three questions I would definitely ask about Kong

1. Are we using Kong purely as a reverse proxy or as an MCP-aware gateway?

There is a difference between forwarding HTTP traffic and understanding MCP methods, tool discovery, tool invocation, and tool-level access controls.

2. Can we enforce tool-level authorization centrally?

Kong documents ACL functionality for controlling which authenticated consumers can discover and invoke individual tools. Validate the applicable plugin version, licensing, and deployment configuration.

Kong Docs

3. Is the identity model compatible with MCP's OAuth authorization requirements?

The MCP authorization specification emphasizes resource-specific token audiences and prohibits blindly forwarding an incoming MCP access token to downstream services.

GitHub

### One important Entra ID consideration

I would specifically ask whether the team has evaluated the On-Behalf-Of (OBO) flow.

For example:

- Employee signs into an enterprise AI application.
- AI agent receives the user's authenticated context.
- Agent invokes an MCP server through Kong.
- Kong or the appropriate token-exchange component obtains a token for the downstream resource.
- The backend evaluates the user's delegated permissions.

Microsoft documents OBO patterns for agents operating on behalf of signed-in users. Kong also documents an Entra ID integration pattern for MCP.

Microsoft Learn

+1

One nuance: the exact token exchange and propagation design must be agreed upon. Do not simply forward the incoming token to every MCP server and backend.

# 15. The 15 most influential questions to ask in the architecture presentation

If you only have 30–45 minutes to participate in the architecture review, I would prioritize these.

These are deliberately phrased as constructive architectural challenges rather than objections.

| # | Question | Why it matters |
| --- | --- | --- |
| 1 | Are we establishing a centralized enterprise MCP registry, separate from Kong's gateway configuration? | Enterprise discovery and inventory |
| 2 | Is Kong responsible for MCP discovery, authentication, authorization, or all three? | Clear architectural boundaries |
| 3 | Are we authenticating individual agents or relying on a shared application identity? | Agent accountability |
| 4 | How do we propagate user identity end-to-end using Entra ID and OBO? | User-level authorization |
| 5 | Can we enforce authorization at individual MCP tool level? | Least privilege |
| 6 | Will each MCP tool have a risk classification? | Risk-based governance |
| 7 | Who approves write and destructive operations? | Human accountability |
| 8 | Will we establish an enterprise Python MCP starter kit? | Engineering consistency |
| 9 | How will we prevent prompt injection and malicious tool descriptions? | Agentic AI security |
| 10 | Can we trace every tool invocation from user request to backend transaction? | Auditability |
| 11 | How will we govern third-party and community MCP servers? | Supply chain security |
| 12 | Will MCP tool schema changes require versioning and recertification? | Change governance |
| 13 | How do we prevent shadow MCP servers outside Kong? | Centralized control |
| 14 | Can we automate MCP governance through CI/CD and policy-as-code? | Governance scalability |
| 15 | Who owns the lifecycle, SLA, retirement, and emergency revocation of MCP servers? | Operational accountability |

# 16. New enterprise standards I would propose

Rather than simply asking questions, I would try to leave the meeting with agreement to establish some additional standards.

Here is the framework I would advocate.

# Proposed Enterprise MCP Governance Framework

Suggested standards for architecture board consideration

1. Identity and access governance

- Entra ID integration mandatory.
- Unique workload identity for each production MCP server.
- Explicit agent identity.
- Least-privilege OAuth permissions.
- User delegation where business authorization requires it.
- Tool-level authorization.

2. MCP onboarding and registry governance

- Centralized MCP catalog.
- Mandatory business and technical ownership.
- Approved Kong registration.
- Standard onboarding checklist.
- Environment segregation.
- Third-party MCP assessment.

3. Engineering governance

- Approved Python MCP starter kit.
- Standard tool schemas and validation.
- Secure coding standards.
- Automated testing and scanning.
- Container and dependency security.
- Standardized error handling.

4. Agentic AI security governance

- Tool risk classification.
- Prompt-injection testing.
- Tool allowlisting.
- Human approval for critical actions.
- Controlled agent-to-agent delegation.
- Emergency tool revocation.

5. Data governance

- Mandatory data classification.
- Backend authorization.
- PII protection.
- Data minimization.
- DLP and retention requirements.
- Sensitive output handling.

6. Operational governance

- Centralized observability.
- End-to-end tracing.
- SLA/SLO requirements.
- Rate limiting.
- Version management.
- Periodic security recertification.
- Defined decommissioning process.

7. Governance automation

- CI/CD policy checks.
- Automated compliance validation.
- Registry synchronization.
- Continuous configuration monitoring.
- Automated alerts for policy violations.

# 17. Suggested implementation roadmap

One thing I would recommend is not trying to implement all governance requirements at once.

A phased approach is more realistic.

1. Phase 1 – Establish the foundation
   Must have- Enterprise MCP reference architecture.
   - Kong and Entra ID integration standards.
   - MCP onboarding and registration process.
   - Central inventory and ownership.
   - Standard Python MCP starter kit.
   - Basic security and audit requirements.
2. Phase 2 – Introduce advanced governance
   Next priority- Tool-level access control.
   - Tool risk classification.
   - Data classification.
   - End-to-end tracing.
   - Third-party MCP certification.
   - Versioning and change management.
   - Human-in-the-loop patterns.
3. Phase 3 – Automate and scale
   Strategic- Policy-as-code.
   - Automated MCP certification.
   - Continuous compliance monitoring.
   - Agent identity and delegation governance.
   - Shadow MCP detection.
   - Enterprise MCP usage analytics.
   - Automated lifecycle management.

# 18. How to make your contribution stand out in the meeting

I would bring up three ideas that go beyond the typical architecture presentation.

### Idea 1: Establish an MCP Governance Scorecard

Every MCP server should have a compliance scorecard.

For example:

| Governance dimension | Compliance |
| --- | --- |
| Entra ID authentication | Pass / Fail |
| Kong registration | Pass / Fail |
| Workload identity | Pass / Fail |
| Tool-level authorization | Pass / Fail |
| Data classification | Pass / Fail |
| Security testing | Pass / Fail |
| Audit logging | Pass / Fail |
| Business ownership | Pass / Fail |
| Versioning | Pass / Fail |
| Operational SLA | Pass / Fail |

This can eventually become an automated production-readiness gate.

### Idea 2: Introduce a central MCP kill switch

Imagine a compromised MCP server or an agent invoking an unexpected critical tool.

Can security teams immediately:

- Disable the MCP server.
- Block an individual tool.
- Revoke the associated identity.
- Terminate or invalidate relevant sessions and credentials.
- Block a particular agent from accessing the MCP ecosystem.

This is a valuable enterprise resilience requirement.

### Idea 3: Establish an enterprise MCP capability marketplace

Instead of every AI development team building its own integrations, establish a governed catalog of reusable business capabilities.

For example:

| Domain | Reusable MCP capabilities |
| --- | --- |
| HR | Employee lookup, leave balance, policy search |
| Finance | Invoice lookup, payment status, budget retrieval |
| IT | Incident search, service requests, knowledge retrieval |
| CRM | Customer lookup, account details, opportunity search |
| Data | Dataset discovery, metadata retrieval, approved queries |

Agents can consume approved tools instead of reinventing integrations.

This improves reuse, security consistency, and cost efficiency.

# 19. My recommended closing statement for the meeting

I would use something like this to influence the architecture discussion without sounding like you are challenging the team's overall direction.

Writing

One area I would like us to consider as we finalize the enterprise MCP architecture is moving beyond MCP server registration and gateway-level authentication towards a comprehensive MCP governance framework.

While Kong and Entra ID provide important foundations for gateway management and identity, I believe we should also standardize tool-level authorization, agent identity and delegation, data classification, risk-based tool governance, end-to-end auditability, and MCP lifecycle management.

In particular, I would like us to explore three capabilities:

1. **Centralized MCP Registry:** A governed enterprise catalog that captures MCP server ownership, tool definitions, permissions, risk classifications, versions, and approved consumers.
2. **Tool-Level Governance:** A standardized model to classify and authorize individual MCP tools based on business risk, user identity, agent identity, and data sensitivity.
3. **Automated MCP Compliance:** Integration of security, identity, architecture, and operational checks into the MCP onboarding and CI/CD lifecycle.

This would allow us to establish not just a standardized way of exposing MCP servers through Kong, but a scalable, secure, reusable, and auditable enterprise agentic AI ecosystem.

## My final recommendation: Focus on these five themes

If I were participating as a senior Python and agentic AI architect, these would be my strongest positions:

# 01

Identity is not authorization

Entra ID authenticates the caller, but the enterprise must still govern which agent, user, and individual tool can perform which action.# 02

MCP registry is not just gateway registration

We need an enterprise catalog with ownership, capabilities, dependencies, risk classification, and lifecycle status.# 03

Govern tools, not just servers

Every tool needs an explicit business purpose, permission boundary, risk classification, and audit trail.# 04

Make security and governance automated

Use Python reference implementations, CI/CD gates, policy-as-code, and automated certification rather than relying on manual approvals.# 05

Govern the agentic ecosystem, not just MCP

Include agent identities, delegation, multi-agent interactions, human approvals, prompt injection, and autonomous action boundaries.

The single most important question I would ask the Enterprise Architecture team:

> Are we designing a centralized MCP gateway onboarding process, or are we establishing an enterprise-wide governance framework for how AI agents discover, access, invoke, and execute business capabilities securely?

That question shifts the conversation from infrastructure standardization to strategic enterprise agentic AI architecture.

Useful technical references to support the discussion:

- [Kong – MCP Traffic Gateway](<https://developer.konghq.com/mcp/?utm_source=chatgpt.com>)
- [Kong – AI MCP Proxy and tool-level ACL](<https://developer.konghq.com/plugins/ai-mcp-proxy/?utm_source=chatgpt.com>)
- [MCP – Authorization specification](<https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/authorization.mdx?utm_source=chatgpt.com>)
- [Kong – Secure MCP with Microsoft Entra ID](<https://developer.konghq.com/cookbooks/secure-mcp-entra-id/?utm_source=chatgpt.com>)
- [Microsoft – Agent OAuth and On-Behalf-Of flow](<https://learn.microsoft.com/en-us/entra/agent-id/agent-on-behalf-of-oauth-flow?utm_source=chatgpt.com>)
