# Aura Customer Support Bot

An intelligent customer support bot built with A2A (Agent2Agent) SDK that handles customer queries and escalates to humans.

## Features

- **Knowledge Base Query**: Search the Aura Electronics knowledge base for solutions
- **Automated Solutions**: Provide clear steps and policies from the knowledge base
- **Human Escalation**: Automatically escalate critical issues to Tier 2 support

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## Usage

### Running the Agent

```bash
# Run locally
python -m src --host localhost --port 5000

# Or using Docker
docker-compose up
```

### Available Functions

#### Query Knowledge Base
Search the knowledge base for customer issues:
- Extracts relevant policies and steps based on search terms

#### Escalate to Human
Escalate complex or sensitive issues to a Tier 2 specialist:
- Generates a ticket ID with context and reasoning

## Examples

### Support Query
```
"How do I pair my AuraSync earbuds?"
"I want a refund for my order."
```

### Escalation
```
"I'm very angry and want to talk to a manager."
"This charge is fraudulent."
```

## Configuration

The agent runs on port 5000 by default. You can customize the host and port using command line options:

```bash
python -m src --host 0.0.0.0 --port 8080
```

## Dependencies

- a2a-sdk: A2A framework for agent communication
- OpenAI: For agent conversation handling

## Environment Variables

- `OPENAI_API_KEY`: Required for agent conversation handling
- `PORT`: Server port (optional, default: 5000)
- `HOST`: Server host (optional, default: localhost)