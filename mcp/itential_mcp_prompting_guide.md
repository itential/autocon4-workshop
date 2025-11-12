# Itential MCP Agent Prompting Guide

Quick reference for working with itential-mcp tools through an AI agent or assistant.

## Basic Principles

- **Be as specific as possible**: Include exact names (device names, workflow names, service names)
- **Use provided data**: Reference the actual values returned from previous commands or close references (i.e. servicenow for ServiceNow)
- **Let the LLM work**: It will format results, monitor jobs, and summarize outputs automatically but you can ask for specific formats if you'd like (i.e. tables, markdown, etc.)

> ⚠️ **CRITICAL:** Every session starts with `@agent`
>
> If you don't invoke the agent, none of the skills (i.e., MCP) will work.
>
>_Agent mode is a feature of the AnythingLLM application we're using here_
>
> **Expected output:**
> ```
> Agent @agent invoked. Swapping over to agent chat. Type /exit to exit agent execution loop early.
> ```

---

## Platform Health & Discovery

### `get_health`

**Usage:**
```
check the Itential platform health
```

**Returns:**
- System status (MongoDB, Redis)
- Running applications and adapters
- Resource utilization
- Platform version

---

## Integration Management

### `get_integrations`

**Usage:**
```
show me all integrations
```

**Returns:**
- Integration names
- Integration models/types
- Configuration details

---

## Gateway Services

### `get_gateways`

**Usage:**
```
show the available automation gateways
```

**Returns:**
- Gateway cluster names
- Connection status
- Enabled/disabled state

### `get_services`

**Usage:**
```
list all gateway services
```

**Returns:**
- Service names
- Service types (ansible-playbook, python-script, etc.)
- Required input parameters
- Descriptions

### `run_service`

**Usage:**
```
run show version on device 8000v-1
```

or

```
check the routing table on device 8000v-1
```

**Agent Behavior:**
- Identifies the correct service
- Formats parameters properly
- Executes the service
- Summarizes output in tables or structured format

**Returns:**
- Command output (summarized and formatted)
- Execution status
- Return codes
- Elapsed time

---

## Workflow Operations

### `get_workflows`

**Usage:**
```
List all workflows
```

**Returns:**
- Workflow names
- API route names (needed for execution)
- Required input parameters
- Last execution time

### `start_workflow` + `describe_job`

**Usage:**
```
Run the ac4 workflow with:
- hostname: networkautomation.forum
- deviceName: 8000v-1
- interface: GigabitEthernet1.101
- changeRequest comments: "Testing interface configuration"

Monitor until complete
```

**Agent Behavior:**
1. Starts the workflow
2. Polls job status automatically
3. Shows progress updates
4. Summarizes final results with task outcomes

**Returns:**
- Job execution summary
- Task completion status
- Any errors or warnings
- Final workflow state

---

## Tips

1. **Start with discovery** — Use `get_*` commands to see what's available
2. **Copy exact names** — Device names and service names are case-sensitive
3. **Trust the agent** — It will format outputs appropriately (tables, summaries, etc.)
4. **Monitor workflows** — Always ask to monitor workflows to completion
5. **Be concise** — Short prompts work best for run_service tasks

---

## Common Patterns

#### Investigate then Act
```
1. "List all workflows"
2. "Show me the input parameters for the bgp_provisioning workflow"
3. "Run the bgp_provisioning workflow with [parameters]"
```

#### Device Operations
```
1. "What services can run commands on devices?"
2. "Run [command] on [device]"
3. "Summarize the results in a table"
```

#### Health Check
```
1. "Check platform health"
2. "Are there any issues with applications or adapters?"
```

---

## Do's & Don'ts

| ✅ Do | ❌ Don't |
|------|---------|
| Describe your goal clearly | Include job IDs manually — the agent tracks them |
| Provide exact names from discovery commands | Format JSON yourself — just describe what you want |
| Ask for summaries and tables | Specify tool names — describe the goal |
| Request monitoring for long-running tasks | Over-explain — be direct |