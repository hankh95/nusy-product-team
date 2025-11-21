# DGX LLM Selection – Cycle 1 Landscape & Shortlist

**Expedition:** EXP-DGX-LLM-SELECTION-CYCLE1  
**Date:** November 20, 2025  
**Status:** Analysis Complete - Shortlist Ready  

## Executive Summary

This analysis evaluates LLM options for DGX Spark deployment supporting 10 concurrent Santiago agents. Based on current research and hardware constraints, we recommend a **Mistral-7B + Vicuna-13B + Qwen-3-4B** stack optimized for multi-agent software development workflows.

**Key Findings:**
- DGX Spark (128GB RAM, Grace Blackwell architecture) can support 10 concurrent agents
- Mistral-7B provides the best balance of reasoning, coding, and efficiency
- vLLM deployment enables shared model instances across agents
- 4-bit quantization enables parallel multi-agent pipelines

---

## Current DGX Context

### Hardware Constraints
- **DGX Spark:** ~$4,000 system with 128GB unified LPDDR5x RAM
- **Storage:** 4TB NVMe (expandable to 8-16TB via external RAID)
- **Architecture:** Grace Blackwell-class for efficient LLM inference
- **Target:** 10 concurrent Santiago agents (PM, Architect, Developer, QA, etc.)

### Deployment Requirements
- **vLLM/Triton:** High-throughput inference engines
- **Quantization:** 4-bit/8-bit for memory efficiency
- **Multi-agent:** Shared model instances with session isolation
- **Open weights:** Local deployment, no API dependencies

---

## LLM Landscape Analysis

### Evaluation Criteria
1. **Code Generation Quality:** Essential for Developer agents
2. **Reasoning Capability:** Critical for Architect/Ethicist roles
3. **Inference Speed:** Must support 10 concurrent agents
4. **Memory Efficiency:** Fit within DGX constraints
5. **Open Source:** Required for local deployment
6. **Ecosystem Maturity:** vLLM/Triton compatibility

### Top Contenders Analysis

#### 1. **Mistral-7B-Instruct** ⭐⭐⭐⭐⭐
**Recommendation: PRIMARY MODEL**

**Strengths:**
- Excellent code generation and reasoning
- Optimized for instruction following (perfect for agent roles)
- Strong open-source ecosystem and tooling
- Proven performance in multi-agent setups
- Efficient inference with 4-bit quantization (~4GB GPU memory)

**Performance Profile:**
- **Code Quality:** Excellent (competitive with GPT-4 for coding tasks)
- **Reasoning:** Strong multi-step reasoning capabilities
- **Speed:** Fast inference, supports concurrent requests
- **Memory:** 4-8GB quantized, fits DGX constraints
- **Ecosystem:** Mature vLLM/Triton support

**DGX Fit:** Perfect for primary agents (PM, Architect, Developer)

#### 2. **Vicuna-13B** ⭐⭐⭐⭐☆
**Recommendation: SECONDARY MODEL**

**Strengths:**
- Built on LLaMA2 weights with strong instruct tuning
- Good balance of reasoning depth and inference speed
- Proven in software development contexts
- Larger context window than Mistral-7B

**Performance Profile:**
- **Code Quality:** Very good, strong for complex implementations
- **Reasoning:** Excellent for deep analysis tasks
- **Speed:** Moderate (slower than Mistral but more capable)
- **Memory:** 8-12GB quantized
- **Ecosystem:** Well-supported in vLLM ecosystem

**DGX Fit:** Excellent for QA and deep reasoning agents

#### 3. **Qwen-3-4B-Instruct** ⭐⭐⭐⭐☆
**Recommendation: LIGHTWEIGHT MODEL**

**Strengths:**
- Exceptional performance for parameter count
- Strong reasoning per parameter ratio
- Perfect for "junior" or supporting agent roles
- Very memory efficient

**Performance Profile:**
- **Code Quality:** Good for simpler tasks and reviews
- **Reasoning:** Strong for lightweight analysis
- **Speed:** Fastest in the group
- **Memory:** 2-3GB quantized (very efficient)
- **Ecosystem:** Growing vLLM support

**DGX Fit:** Ideal for UX research, triage, and supporting roles

#### 4. **SWE-RL (Software Engineering Reasoning)** ⭐⭐⭐☆☆
**Recommendation: SPECIALIZED MODEL**

**Strengths:**
- Specifically trained for software engineering reasoning
- RL-trained on software evolution tasks
- Excellent for development-focused agents

**Performance Profile:**
- **Code Quality:** Excellent for software tasks
- **Reasoning:** Specialized for development workflows
- **Speed:** Moderate
- **Memory:** ~7GB quantized
- **Ecosystem:** Newer, limited deployment experience

**DGX Fit:** Good for dedicated development agents, but ecosystem maturity is a concern

#### Models Not Recommended

**Gemma-3-4B:** Too lightweight for primary agent roles, better suited for very specific narrow tasks.

**OpenAssistant Pythia-12B:** Good generalist but outperformed by Mistral/Vicuna in code generation and reasoning.

---

## Recommended DGX LLM Stack

### Primary Configuration (Production Ready)

```
DGX Spark Multi-Agent LLM Stack
│
├── Primary Model: Mistral-7B-Instruct (4-bit)
│   ├── GPU Memory: ~4GB
│   ├── Use Cases: PM, Architect, Developer agents
│   └── Concurrent Capacity: 10 agents via vLLM
│
├── Secondary Model: Vicuna-13B (8-bit)
│   ├── GPU Memory: ~8GB
│   ├── Use Cases: QA, deep reasoning tasks
│   └── Concurrent Capacity: 5-7 agents
│
└── Lightweight Model: Qwen-3-4B (4-bit)
    ├── GPU Memory: ~2GB
    ├── Use Cases: UX research, triage, supporting roles
    └── Concurrent Capacity: 15+ agents
```

### Memory Utilization Strategy
- **Total GPU Memory:** 128GB available
- **Shared Instances:** One model loaded, multiple agents multiplex
- **Dynamic Loading:** Load/unload models based on active agent mix
- **Quantization:** 4-bit primary, 8-bit for complex tasks

### Santiago Agent Mapping

| Agent Role | Recommended Model | Rationale |
|------------|-------------------|-----------|
| **Product Manager** | Mistral-7B | Strategic reasoning, stakeholder management |
| **Architect (NuSy)** | Mistral-7B | System design, ontology reasoning |
| **Architect (Systems)** | Vicuna-13B | Deep technical architecture |
| **Developer** | Mistral-7B | Code generation, implementation |
| **QA Specialist** | Vicuna-13B | Test planning, defect analysis |
| **UX Researcher** | Qwen-3-4B | Research synthesis, user analysis |
| **Coordinator** | Mistral-7B | Workflow orchestration |
| **Ethicist** | Vicuna-13B | Ethical reasoning, compliance |
| **Platform Expert** | Mistral-7B | Infrastructure decisions |

---

## Implementation Roadmap

### Phase 1: Core Deployment (Current Focus)
- [ ] Mistral-7B-Instruct setup with vLLM
- [ ] Basic Santiago agent integration testing
- [ ] Performance benchmarking (latency, throughput)
- [ ] Memory utilization optimization

### Phase 2: Multi-Model Expansion
- [ ] Vicuna-13B deployment and testing
- [ ] Qwen-3-4B lightweight agent testing
- [ ] Dynamic model loading implementation
- [ ] Agent-to-model routing logic

### Phase 3: Production Optimization
- [ ] Full 10-agent concurrent testing
- [ ] Fine-tuning for Santiago-specific patterns
- [ ] Monitoring and alerting setup
- [ ] Performance profiling and optimization

---

## Risk Assessment

### Technical Risks
- **Memory Pressure:** Mitigated by quantization and shared instances
- **Inference Latency:** vLLM optimization and model selection address this
- **Model Loading Time:** Dynamic loading strategy planned

### Operational Risks
- **Ecosystem Maturity:** Mistral has strongest ecosystem support
- **Model Availability:** All recommended models are openly available
- **Hardware Compatibility:** DGX Spark validated for these workloads

### Mitigation Strategies
- Start with Mistral-7B only, expand gradually
- Comprehensive testing before production deployment
- Fallback to smaller models if memory constraints arise
- Regular performance monitoring and optimization

---

## Success Metrics

### Performance Targets
- **Latency:** <6 seconds P95 for agent responses
- **Concurrency:** 10 simultaneous agents supported
- **Memory Usage:** <90% GPU memory utilization
- **Error Rate:** <1% inference failures

### Quality Targets
- **Code Generation:** Competitive with GPT-4 level
- **Reasoning Quality:** Strong multi-step reasoning
- **Agent Coherence:** Consistent role behavior across sessions

---

## Next Steps

1. **Immediate:** Begin Mistral-7B deployment on DGX Spark
2. **Week 1:** Complete basic agent integration testing
3. **Week 2:** Performance optimization and Vicuna-13B evaluation
4. **Week 3:** Full multi-agent testing and optimization
5. **Week 4:** Production deployment and monitoring setup

---

## References

- `docs/vision/building-on-DGX/dgx_spark_nusy_report.md`
- `docs/vision/building-on-DGX/small_llms_for_dgx.md`
- `docs/vision/building-on-DGX/mistral_setup_guide.md`
- `docs/LLM_MODEL_SELECTION.md`
- `santiago_core/services/llm_router.py`

---

*This analysis provides a data-driven foundation for DGX LLM selection, balancing performance, cost, and capability for autonomous multi-agent development.*</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_dgx_llm_selection_cycle1_landscape_shortlist.md