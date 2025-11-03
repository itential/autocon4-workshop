# Getting Started with Itential MCP Server

## What is MCP?

The Model Context Protocol (MCP) is an open standard introduced by Anthropic in November 2024 that solves the "universal language problem" in AI-tool integration. Just as USB-C provides a universal connector for devices, MCP provides a standardized way for any AI assistant to connect to external tools and data sources without requiring custom integration code.

Before MCP, every AI framework (LangChain, OpenAI, Google's dev kit) had its own proprietary way of connecting to external systems. Building an AI agent that could read emails, check calendars, and update databases meant writing separate integration code for each tool, with different authentication methods, error handling, and data formats.

**MCP operates on JSON-RPC 2.0 and provides three core capabilities:**

- **Tools**: Executable functions that perform actions (deploy infrastructure, send emails, create tickets)
- **Resources**: Access to data and information (read files, query databases, fetch metrics)  
- **Prompts**: Templated workflows that guide AI behavior for specific tasks

When an AI connects to an MCP server, it automatically discovers available capabilities through standardized methods. This means AI assistants can adapt to new tools without requiring updates or retraining. The protocol supports dynamic tool discovery, real-time notifications, and works across cloud providers, on-premises systems, and hybrid environments.

**Why MCP matters for enterprise infrastructure:**
- **Standardization** reduces complexity - what used to require bespoke development becomes configuration
- **Universal interoperability** - your integrations work with Claude, ChatGPT, or any MCP-compatible AI
- **Real-time adaptability** - AI agents learn about new capabilities automatically as infrastructure evolves


## Itential Brings Enterprise Infrastructure to AI

The Itential Model Context Protocol (MCP) server enables AI assistants like Claude to safely orchestrate network automation and infrastructure management across enterprise environments. 

The Itential MCP server exposes enterprise-grade infrastructure management capabilities to AI assistants through standardized tools.

### How It Works

The MCP architecture creates a secure bridge between AI and your infrastructure via the Itential Platform:

```
AI Assistant → Itential MCP Server → Itential Platform → Your Infrastructure
```

When you ask Claude "Show me all devices in the Atlanta datacenter", the AI:
1. Understands your natural language request
2. Calls the appropriate Itential MCP tool (`get_devices`)
4. Receives structured data from your Itential Platform
5. Formats and presents the results in a readable way

This means **AI makes decisions, Itential provides the execution and MCP provides the tool exposure**, ensuring enterprise-grade security and compliance at every step.

[Screenshot: Architecture diagram showing the flow from Claude to Infrastructure]


## Installation

### Option 1: Virtual Environment Installation (Recommended)

**Prerequisites**: Python >=3.10 is the minimal requirement for this installation method.

```bash
# Create a virtual environment
python -m venv <venv-dir>/itential-mcp-venv

# Activate the virtual environment
# On macOS/Linux:
source <venv-dir>/itential-mcp-venv/bin/activate

# On Windows:
<venv-dir>\itential-mcp-venv\Scripts\activate

# Install from PyPI
python -m pip install itential-mcp

# Verify installation
itential-mcp version
```

*Note: Remember to activate the virtual environment (`source <venv-dir>/itential-mcp-venv/bin/activate`) each time you want to use the itential-mcp command.*

### Option 2: Docker Container

For containerized deployments:

```bash
# Pull the latest version
docker pull ghcr.io/itential/itential-mcp:latest
```

[Screenshot: Docker Desktop showing the pulled Itential MCP image]

## Configuring Claude Desktop

Claude Desktop requires specific configuration to connect to the Itential MCP server using environment variables. Access the configuration through **Settings → Developer → Edit Config**.

[Screenshot: Claude Desktop Settings page with Developer tab highlighted]

### Environment Variable Configuration

**For Virtual Environment Installation:**
```json
{
  "mcpServers": {
    "itential-mcp": {
      "command": "<venv-dir>/itential-mcp-venv/bin/itential-mcp",
      "args": ["run"],
      "env": {
        "ITENTIAL_MCP_PLATFORM_HOST": "your-platform.example.com",
        "ITENTIAL_MCP_PLATFORM_CLIENT_ID": "your-client-id",
        "ITENTIAL_MCP_PLATFORM_CLIENT_SECRET": "your-client-secret",
        "ITENTIAL_MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Docker Configuration

If using Docker:

```json
{
  "mcpServers": {
    "itential-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "ITENTIAL_MCP_PLATFORM_HOST=your-platform.example.com",
        "-e", "ITENTIAL_MCP_PLATFORM_CLIENT_ID=your-client-id",
        "-e", "ITENTIAL_MCP_PLATFORM_CLIENT_SECRET=your-client-secret",
        "ghcr.io/itential/itential-mcp:latest"
      ]
    }
  }
}
```

*Note: Basic authentication is also supported using `ITENTIAL_MCP_PLATFORM_USER` and `ITENTIAL_MCP_PLATFORM_PASSWORD` instead of the OAuth variables above.*

After saving any configuration, restart Claude Desktop to activate the MCP server connection.

[Screenshot: Claude Desktop restart notification after configuration change]

## Verifying Your Connection

After configuration, verify the connection in your AI assistant:

### In Claude Desktop

1. Open a new conversation
2. Click the `Search and Tools` icon or type "Show MCP tools"
3. Look for "itential-mcp" in the connected servers list
4. Try a simple query: "Check the Itential platform health"

[Screenshot: Claude Desktop showing the MCP tools panel with Itential listed]

### In VS Code with Cline

1. Open the Cline chat (usually in the sidebar)
2. Check the status bar for "MCP: Connected"
3. Type: "@mcp list tools" to see available Itential tools
4. Try: "Using Itential MCP, check the platform health"

[Screenshot: Cline chat showing successful MCP tool listing]

## Your First Five Minutes with Itential MCP

Once connected, try these queries in order to build confidence:

### 1. Health Check (Read-only, Safe)
```
"Check if the Itential platform is healthy"
```
**What happens**: Uses `get_health` tool to verify platform status  
**Expected response**: Platform status, API availability, and component health

[Screenshot: Claude showing health check response with green status indicators]

### 2. Device Discovery (Read-only)
```
"Show me all devices in Itential"
```
**What happens**: Queries device inventory with filters  
**Expected response**: Formatted table of devices with management IPs

[Screenshot: Claude displaying device list in a formatted table]

### 3. Workflow Listing (Read-only)
```
"What automation workflows are available?"
```
**What happens**: Searches workflows by keyword  
**Expected response**: List of workflow names with descriptions

[Screenshot: Claude showing available workflows]

### 4. Configuration Check (Read-only)
```
"Get the show version for device switch-01?"
```
**What happens**: Retrieves device configuration  
**Expected response**: Show ver with output interpretation

[Screenshot: Claude displaying configuration with colored syntax]

### 5. Launch a Gateway Manager Service (python-script, ansible-playbook)
```
Launch service aws-ec2-list for region us-west-1
```
**What happens**: Initiates a service  
**Expected response**: Parse script response and gives me information about the output

[Screenshot: Claude displaying prompt and service output]

### 6. Launch a workflow
```
Launch Port Turn Up Service workflow
```

**What happens**: Ask for clarification on input parameters and initiates the workflow  
**Expected response**: Job ID and progress updates

[Screenshot: Claude showing workflow id and progress]

## Conclusion

You've successfully configured the Itential MCP server to work with your AI assistant, creating a powerful bridge between natural language and enterprise infrastructure management. This setup enables:

- **Natural language network operations** - Ask questions, get answers
- **Safe automation** - Start with read-only, progress to changes
- **Team collaboration** - Share configurations and patterns
- **Rapid troubleshooting** - AI-assisted problem resolution

The combination of Python virtual environments for isolation, flexible configuration options, and progressive learning examples ensures a smooth journey from setup to production use.

**Next Steps**:
1. Complete the first five queries
2. Create your own query templates
3. Share your configuration with your team
4. Join the community at [github.com/itential/itential-mcp](https://github.com/itential/itential-mcp)

Welcome to the future of infrastructure automation - where AI and enterprise systems work together seamlessly through the Model Context Protocol.



<br/><br/><br/>

## Appendix: Frequently Asked Questions

#### How do I test my connection?

To verify connectivity to the Itential platform:

```bash
itential-mcp test-connection
```

#### How do I enable debug mode?

To get detailed logging information:

```bash
ITENTIAL_MCP_LOG_LEVEL="DEBUG" itential-mcp run
```

#### How do I filter tools by tags?

You can include or exclude specific tool categories:

```bash
# Include only specific tool categories
ITENTIAL_MCP_INCLUDE_TAGS="devices,workflows" itential-mcp run

# Exclude specific tool categories  
ITENTIAL_MCP_EXCLUDE_TAGS="experimental,destructive" itential-mcp run
```

#### How do I update the Itential MCP server?

**For Virtual Environment Installation:**
```bash
# Activate virtual environment first
source <venv-dir>/itential-mcp-venv/bin/activate
pip install --upgrade itential-mcp
```

**For Docker**:
```bash
docker pull ghcr.io/itential/itential-mcp:latest
```

#### Where can I find more examples, documentation, etc.?

- Official documentation: [github.com/itential/itential-mcp](https://github.com/itential/itential-mcp)
- Community examples: Check the Issues and Discussions sections

#### How do I contribute or report issues?

- GitHub Issues: [github.com/itential/itential-mcp/issues](https://github.com/itential/itential-mcp/issues)
- Pull Requests: Fork the repository and submit Pull Requests
- Community Discussion: Join the GitHub Discussions