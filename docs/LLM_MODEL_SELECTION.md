# LLM Model Selection Strategy

## Overview
The NuSy proxy team uses intelligent routing to select the most appropriate LLM model based on:
1. **Role** - Architecture roles use xAI (Grok) for deep reasoning, development roles use OpenAI
2. **Task Complexity** - Simple queries use fast models, critical decisions use reasoning models
3. **Cost Optimization** - Balance performance and cost for each use case

## Current Model Configuration (Nov 2025)

### OpenAI Models
Used for: PM, Developer, QA, UX, Coordinator proxies

| Complexity | Model | Use Case | Pricing (per 1M tokens) | Context |
|------------|-------|----------|-------------------------|---------||
| **SIMPLE** | `gpt-5-nano` | Ultra-fast, most cost-efficient | $0.05 / $? | 400K |
| **MODERATE** | `gpt-5.1` | Flagship for coding/agentic tasks | $1.25 / $10.00 | 400K |
| **COMPLEX** | `gpt-5.1` | Best for architecture with reasoning | $1.25 / $10.00 | 400K |
| **CRITICAL** | `o3` | Deep reasoning for system-wide decisions | $2.00 / $8.00 | 200K |

**Model Capabilities:**
- **gpt-5-nano**: Ultra-fast GPT-5 variant. Most cost-efficient option for simple queries and completions.
- **gpt-5.1**: Latest flagship model with configurable reasoning. Best for coding, agentic tasks, and architecture.
- **o3**: Advanced reasoning model (April 2025). For complex multi-step problems requiring deep analysis.

### xAI Models
Used for: Architect, Ethicist, Researcher proxies

| Complexity | Model | Use Case | Pricing (per 1M tokens) | Context |
|------------|-------|----------|-------------------------|---------|
| **ALL** | `grok-4-fast` | Fast reasoning across all complexities | $0.20 / $0.50 | 2M |

**Model Capabilities:**
- **grok-4-fast**: Latest xAI model (Nov 2024). Optimized for reasoning with massive 2M token context window. Excellent for architecture design and ethical reasoning.

## Role-to-Provider Mapping

### OpenAI Roles (Development & Execution)
- **PM Proxy**: Product strategy, hypothesis generation, backlog management
- **Developer Proxy**: Code implementation, technical tasks
- **QA Proxy**: Testing, validation, quality assurance
- **UX Proxy**: User experience, interface design
- **Coordinator Proxy**: Orchestration, workflow management

### xAI Roles (Architecture & Reasoning)
- **Architect Proxy**: System design, architecture decisions
- **Ethicist Proxy**: Ethical review, principles alignment
- **Researcher Proxy**: Research, analysis, investigation

## Task Complexity Detection

The router automatically detects complexity based on tool names:

```python
# CRITICAL complexity (reasoning models)
- "security", "critical", "consultation"
- "ethical", "review_"

# COMPLEX complexity  
- "design", "architecture", "adr", "evaluate"

# MODERATE complexity
- "write", "implement", "create", "generate"
- "test", "qa", "validate"

# SIMPLE complexity
- "read_", "query_", "get_", "list_"
```

## Cost Optimization Strategy

### High-Volume Tasks → Efficient Models
- Code completion: `gpt-5-nano` ($0.05/$?)
- Quick queries: `gpt-5-nano` ($0.05/$?)
- Standard development: `gpt-5.1` ($1.25/$10, with reasoning)

### Critical Tasks → Reasoning Models
- Architecture decisions: `grok-4-fast` ($0.20/$0.50) or `o3` ($2.00/$8.00)
- Ethical reviews: `grok-4-fast` (massive context, excellent reasoning)
- System-wide changes: `o3` (deep reasoning)

### Context Window Selection
- **Small context needs** (< 200K tokens): OpenAI models
- **Large context needs** (> 200K tokens): `grok-4-fast` (2M context)

## Example Usage

```python
from santiago_core.services.llm_router import LLMRouter, TaskComplexity

router = LLMRouter()

# Simple PM task: Use gpt-5-nano
config = router.get_config('pm_proxy', TaskComplexity.SIMPLE)
# → openai / gpt-5-nano

# Complex architecture task: Use grok-4-fast
config = router.get_config('architect_proxy', TaskComplexity.COMPLEX)
# → xai / grok-4-fast

# Critical security review: Use o3
config = router.get_config('pm_proxy', TaskComplexity.CRITICAL)
# → openai / o3
```

## Performance Characteristics

### Speed
1. **Fastest**: `gpt-5-nano` (ultra-fast, optimized for speed)
2. **Fast**: `gpt-5.1` (flagship with configurable reasoning)
3. **Moderate**: `grok-4-fast` (reasoning with 2M context)
4. **Slower**: `o3` (deep reasoning, intentionally uses more compute)

### Reasoning Quality
1. **Best**: `o3` (deep reasoning, most compute time)
2. **Excellent**: `grok-4-fast` (reasoning model with 2M context)
3. **Very Good**: `gpt-5.1` (flagship with configurable reasoning)
4. **Good**: `gpt-5-nano` (fast, efficient)

### Context Capacity
1. **Largest**: `grok-4-fast` (2M tokens)
2. **Large**: All others (200K tokens)

## Future Considerations

### GPT-5 Series Now Available ✅
As of November 2025, the GPT-5 series is in production:
- **gpt-5.1**: Flagship for coding/agentic tasks ($1.25/$10, 400K context) ✅ IN USE
- **gpt-5-mini**: Fast reasoning ($0.25/$2, 400K context) - available
- **gpt-5-nano**: Ultra-fast, cost-efficient ($0.05/?, 400K context) ✅ IN USE

Current mapping:
- SIMPLE → `gpt-5-nano` (most cost-efficient)
- MODERATE/COMPLEX → `gpt-5.1` (flagship with reasoning)
- CRITICAL → `o3` (deepest reasoning)

### Additional Providers
Consider adding:
- **Anthropic Claude**: Strong reasoning, good for architecture
- **Google Gemini**: Multi-modal capabilities
- **Local Models**: For data privacy, offline work

## Monitoring & Adjustment

Track these metrics to optimize model selection:
- **Cost per task type**: Identify expensive operations
- **Response quality**: A/B test different models
- **Latency**: Monitor response times by model
- **Token usage**: Track context window utilization
- **Error rates**: Monitor API failures by provider

Adjust routing based on:
- New model releases
- Pricing changes
- Performance improvements
- User feedback
- Cost constraints

## Configuration

Models are configured in `santiago_core/services/llm_router.py`:

```python
MODEL_MAP = {
    (LLMProvider.OPENAI, TaskComplexity.SIMPLE): "gpt-5-nano",
    (LLMProvider.OPENAI, TaskComplexity.MODERATE): "gpt-5.1",
    (LLMProvider.OPENAI, TaskComplexity.COMPLEX): "gpt-5.1",
    (LLMProvider.OPENAI, TaskComplexity.CRITICAL): "o3",
    (LLMProvider.XAI, TaskComplexity.SIMPLE): "grok-4-fast",
    # ... etc
}
```

API keys are loaded from `.env`:
```bash
OPENAI_API_KEY=sk-proj-...
XAI_API_KEY=xai-...
```

## Verification

To verify current model selection:
```bash
python -c "
from dotenv import load_dotenv
load_dotenv()
from santiago_core.services.llm_router import LLMRouter, TaskComplexity

router = LLMRouter()
for complexity in TaskComplexity:
    config = router.get_config('pm_proxy', complexity)
    print(f'{complexity.value:12} -> {config.model}')
"
```

To see available OpenAI models:
```bash
python -c "
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
models = client.models.list()
for m in sorted([m.id for m in models.data if 'gpt' in m.id or 'o1' in m.id or 'o3' in m.id or 'o4' in m.id]):
    print(m)
"
```
