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

