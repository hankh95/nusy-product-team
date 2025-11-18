# Santiago-PM Question Answering System

The Question Answering System provides intelligent question answering capabilities for the Santiago-PM team, integrating questionnaire-based data collection with Santiago Core neurosymbolic reasoning for prioritization decisions.

## Overview

This system enables the team to:

- **Ask complex questions** about product management, prioritization, and development
- **Get reasoned answers** using Santiago Core's neurosymbolic reasoning
- **Generate questionnaires** for gathering additional information when needed
- **Receive prioritization recommendations** based on workflow analysis and domain knowledge

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Team Member   │────│ Question Router  │────│  Answer Engine  │
│                 │    │                  │    │                 │
│ Asks Questions  │    │ Analyzes & Routes│    │ Generates       │
│                 │    │ Questions        │    │ Responses       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Questionnaire   │    │ Santiago Core    │    │ Workflow Engine │
│ System          │    │ Reasoning        │    │ Prioritization  │
│                 │    │                  │    │                 │
│ Generates Forms │    │ Domain Knowledge │    │ Task Ordering   │
│ for Research    │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Key Components

### QuestionAnsweringService

The main service that orchestrates question answering:

- **Question Analysis**: Determines domain and complexity level
- **Strategy Selection**: Chooses appropriate answering method
- **Integration**: Combines multiple reasoning sources

### QuestionAnsweringMCPService

MCP wrapper that provides standardized interface:

- **Operations**: answer, generate_questionnaire, analyze_response, prioritize
- **Contract**: Defined input/output schemas and cost models
- **Integration**: Works with EXP-040 MCP service registry

### Knowledge Domains

Questions are routed to appropriate domains:

- `product_management`: Feature prioritization, requirements
- `software_engineering`: Code quality, architecture decisions
- `system_architecture`: System design, scalability
- `team_dynamics`: Collaboration, communication
- `technical_debt`: Maintenance, refactoring
- `risk_management`: Risk assessment, mitigation

## Usage Examples

### Basic Question Answering

```python
from question_answering_service import QuestionAnsweringService

qa_service = QuestionAnsweringService()

# Ask a simple question
result = await qa_service.answer_question("How should we handle technical debt?")
print(result["answer"])
print(f"Confidence: {result['confidence']}")

# Ask a prioritization question
result = await qa_service.answer_question(
    "Which features should we prioritize: user authentication, payment processing, or admin dashboard?",
    context={"domain": "product_management"}
)
print(result["prioritized_items"])
```

### Questionnaire Generation

```python
# Generate a questionnaire for research
questionnaire = await qa_service.generate_questionnaire_for_topic(
    "user experience improvements",
    context={"description": "Gather requirements for UX enhancements"}
)

print(questionnaire["title"])
print(questionnaire["content"])  # Full markdown questionnaire
```

### MCP Integration

```python
from question_answering_mcp import create_question_answering_mcp_service

# Create MCP service
qa_mcp = create_question_answering_mcp_service()

# Use through MCP interface
response = await qa_mcp.execute({
    "operation": "answer",
    "params": {
        "question": "How do we improve code quality?",
        "context": {"domain": "software_engineering"}
    }
})
```

## Question Types

### Simple Questions
- **Pattern**: "How to...", "What is...", "Explain..."
- **Method**: Direct Santiago Core reasoning
- **Example**: "How should we structure our codebase?"

### Complex Questions
- **Pattern**: "Why...", "Should...", "Best way...", "Recommend..."
- **Method**: Combined reasoning with validation questionnaires
- **Example**: "Why is this feature important for our users?"

### Prioritization Questions
- **Pattern**: Contains "prioritize", "priority", or lists items
- **Method**: Workflow engine analysis + Santiago Core explanation
- **Example**: "Which of these tasks should we do first: A, B, or C?"

### Research Questions
- **Pattern**: Requires external information or investigation
- **Method**: Generate research questionnaire
- **Example**: "What are the latest trends in our industry?"

## Integration with Santiago-PM

### Cargo Manifests (Features)
Question answering can generate feature specifications:

```markdown
## Feature: Intelligent Question Answering

### Scenario: Team member asks complex question
Given a team member has a complex product question
When they ask the question through Santiago
Then they receive a reasoned answer with confidence score
And optionally a questionnaire for additional research
```

### Ships Logs (Issues)
Questions about issues generate structured problem analysis:

```markdown
## Issue: Question Answering Integration

**Status**: ✅ RESOLVED
**Priority**: HIGH

**Description**: Integrate question answering with Santiago Core reasoning

**Analysis**: Used neurosymbolic reasoning for prioritization decisions
**Solution**: Created QuestionAnsweringMCPService with domain routing
```

### Voyage Trials (Experiments)
Question answering capabilities are tested through experiments:

```json
{
  "experiment": "question_answering_accuracy",
  "hypothesis": "Santiago can answer PM questions with >80% accuracy",
  "metrics": {
    "accuracy": 0.85,
    "confidence_calibration": 0.92,
    "questionnaire_generation": 0.78
  }
}
```

## Configuration

### Knowledge Domain Mapping

```python
# Default domain mappings
knowledge_domains = {
    "product_management": "product_management",
    "software_engineering": "software_engineering",
    "prioritization": "product_management",
    "requirements": "product_management",
    "architecture": "system_architecture"
}
```

### Confidence Thresholds

```python
# When to generate validation questionnaires
validation_threshold = 0.7

# When to escalate to research questions
research_threshold = 0.5
```

## Testing

Run the integration tests:

```bash
cd santiago-pm/tackle/question_answering
python test_integration.py
```

Test specific functionality:

```bash
# Test CLI interface
python question_answering_service.py "How should we prioritize features?"

# Generate questionnaire
python question_answering_service.py --generate-questionnaire "user research"
```

## Future Enhancements

### Planned Features

1. **Knowledge Graph Integration**
   - Query existing PM artifacts for context
   - Link questions to relevant documentation
   - Build question-answer knowledge base

2. **Multi-Agent Collaboration**
   - Route questions to specialized agents
   - Aggregate answers from multiple sources
   - Consensus building for complex topics

3. **Learning and Adaptation**
   - Track question-answer quality
   - Improve responses based on feedback
   - Learn from successful questionnaire outcomes

4. **Advanced Reasoning**
   - Temporal reasoning for project timelines
   - Causal reasoning for impact analysis
   - Probabilistic reasoning for risk assessment

### Integration Points

- **EXP-040**: MCP service integration ✅
- **EXP-038**: Santiago Core reasoning ✅
- **EXP-037**: Validation testing 🔄
- **Knowledge Graph**: Context-aware answers 📋
- **Multi-Agent**: Collaborative answering 📋

## Development Workflow

1. **Question Analysis**: Understand user intent and domain
2. **Strategy Selection**: Choose appropriate answering method
3. **Reasoning Execution**: Apply Santiago Core or workflow analysis
4. **Artifact Generation**: Create questionnaires or recommendations
5. **Response Formatting**: Structure answer with confidence and reasoning
6. **Feedback Collection**: Learn from answer quality and user feedback

## Success Metrics

- **Answer Accuracy**: >80% of answers meet user needs
- **Response Time**: <5 seconds for simple questions, <30 seconds for complex
- **Questionnaire Utility**: >70% of generated questionnaires yield valuable insights
- **User Satisfaction**: >85% positive feedback on answer quality
- **System Learning**: Continuous improvement in answer confidence calibration

---

**This system represents Santiago-PM's ability to provide intelligent, context-aware support to the development team, combining structured data collection with advanced neurosymbolic reasoning for comprehensive question answering capabilities.**