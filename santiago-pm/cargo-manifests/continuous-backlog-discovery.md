# Feature: Continuous Backlog Discovery & Grooming

```yaml
---
artifact_type: cargo-manifest
feature_id: F-029
feature_name: continuous-backlog-discovery
priority: 0.93 (CRITICAL)
status: discovery
created: 2025-11-17
created_by: Hank (via conversation)
source: Discussion about Santiago-PM scanning for new work
related_features:
  - F-027 (Personal Log Feature - source of discoveries)
  - F-028 (Workflow Test Data System - testing this workflow)
  - F-026 (Lean-Kanban Backlog Management - where items go)
kerievsky_principles:
  - "Experiment & Learn Rapidly" (discover → validate → prioritize)
  - "Deliver Value Continuously" (always know what's next)
---
```

---

## Feature Overview

**Problem**: Product managers need to continuously scan multiple sources for new work:
- **Personal logs** (human and agent) - feature hints, pain points, discoveries
- **Ships logs** (team issues) - coordination needs, blockers
- **Research logs** - findings that suggest capabilities
- **Cargo manifests** (features) - dependencies, related work
- **Code/artifacts** - TODOs, FIXMEs, comments suggesting improvements
- **Knowledge graph** - patterns, gaps, opportunities
- **Git history** - what's changing, velocity, bottlenecks

**Human Pattern** (Traditional):
- Scan sources manually (spreadsheets, docs, Slack, tickets)
- Backlog grooming once per week (scheduled ceremony)
- PM reviews 1-2 times per day (when they remember)
- Items get lost, delayed, or duplicated

**Santiago-PM Pattern** (Continuous):
- Automated scanning (every N minutes or triggered by events)
- Semantic extraction (detect work items from unstructured sources)
- Continuous grooming (always up-to-date)
- Intelligent clustering (find duplicates, related items)
- Priority calculation (using neurosymbolic backlog algorithm)

**Key Insight**: Santiago-PM can scan more frequently than humans because:
1. No context switching cost (agents don't get tired)
2. Semantic understanding (extract from unstructured text)
3. Graph awareness (see relationships humans miss)
4. Pattern recognition (detect anomalies, trends)

**Value Proposition**:
- **Never miss work**: Scan all sources continuously
- **Reduce duplicates**: Detect similar items automatically
- **Better prioritization**: Always know what's most valuable
- **Faster response**: New items identified within minutes, not days
- **Learning**: Track discovery patterns (where do good ideas come from?)

---

## User Stories

### Story 1: Continuous Source Scanning (MVP)

**As Santiago-PM**
**I want to scan multiple sources for new work items continuously**
**So that I never miss valuable work and the backlog stays current**

**Given** I have access to multiple work sources:
```yaml
sources:
  - type: personal_logs
    location: santiago-pm/personal-logs/
    scan_frequency: every_10_minutes
    patterns:
      - "NEW FEATURE"
      - "need to"
      - "should build"
      - "discovered"
      - "pain point"
  
  - type: ships_logs
    location: santiago-pm/ships-logs/
    scan_frequency: every_5_minutes
    patterns:
      - "[x]" (completed items may suggest follow-up)
      - "blocked"
      - "need help"
      - "coordination issue"
  
  - type: cargo_manifests
    location: santiago-pm/cargo-manifests/
    scan_frequency: on_change (git hook)
    patterns:
      - "future enhancements"
      - "dependencies"
      - "related features"
  
  - type: code_artifacts
    location: src/
    scan_frequency: on_commit (git hook)
    patterns:
      - "TODO:"
      - "FIXME:"
      - "HACK:"
      - "# NOTE:"
  
  - type: research_logs
    location: ocean-research/
    scan_frequency: every_30_minutes
    patterns:
      - "finding"
      - "suggests"
      - "could enable"
```

**When** I run continuous scanning:

**Scan Loop (Every 10 Minutes)**:
```python
def continuous_backlog_scan():
    """
    Santiago-PM's continuous scanning loop.
    
    Runs periodically to discover new work items.
    """
    while True:
        # Get sources that need scanning (based on frequency)
        sources_to_scan = get_sources_ready_for_scan()
        
        for source in sources_to_scan:
            # Extract potential work items
            discoveries = scan_source(source)
            
            for discovery in discoveries:
                # Semantic classification: What type of work is this?
                work_type = classify_work_item(discovery)
                
                # Check if already exists (avoid duplicates)
                if not is_duplicate(discovery):
                    # Create backlog item
                    backlog_item = create_backlog_item(
                        title=discovery.title,
                        type=work_type,
                        source=discovery.source,
                        discovered_at=datetime.now(),
                        priority=calculate_initial_priority(discovery)
                    )
                    
                    # Add to appropriate backlog
                    add_to_backlog(backlog_item, work_type)
                    
                    # Log discovery for learning
                    log_discovery(discovery, backlog_item)
        
        # Wait before next scan
        sleep(calculate_next_scan_interval())
```

**Example Discovery from Personal Log**:
```yaml
# Input: Personal log mentions
content: |
  "Need to build conversational questionnaire interface.
   Current markdown forms are fine but chat-based would be more natural."

# Output: Backlog item created
backlog_item:
  id: BI-042
  title: "Build conversational questionnaire interface"
  type: feature
  source:
    artifact: santiago-pm/personal-logs/humans/2025-11-17-hank-workflow-test-data-feature.md
    line: 234
    context: "User mentioned as future enhancement"
  discovered_at: 2025-11-17T13:15:00Z
  discovered_by: santiago-pm-continuous-scan
  priority: 0.70 (HIGH - user explicitly requested)
  status: new
  tags: [ux, questionnaire, enhancement]
  semantic_links:
    - related_to: santiago-pm/tackle/questionnaires/
    - mentioned_in: personal-log:2025-11-17-hank
```

**Then** I should have:
- All sources scanned within their frequency windows
- New work items extracted and classified
- Duplicates detected and merged
- Backlog always up-to-date
- Discovery patterns tracked

**Acceptance Criteria**:
- [ ] Scan 5+ source types (personal logs, ships logs, code, research, manifests)
- [ ] Each source has configurable scan frequency
- [ ] Semantic extraction detects work items from unstructured text
- [ ] Classification: feature, bug, task, research, debt, coordination
- [ ] Duplicate detection: 95% accuracy (don't create duplicates)
- [ ] Scan latency: < 30 seconds per source
- [ ] Discovery logging: track where good ideas come from
- [ ] Event-triggered scans: git commit, file change, new log entry

---

### Story 2: Semantic Work Item Extraction (Journeyman)

**As Santiago-PM**
**I want to extract work items from unstructured text semantically**
**So that I understand context, not just keyword matches**

**Given** a personal log entry with implicit work mention:
```markdown
# Session Notes

The workflow test data system is going to be crucial. But I'm worried about
performance - if we're loading full KG history every query, it'll be slow.
Maybe we should explore vector DB or Redis for caching? This could be a
separate optimization feature once we have the basic implementation working.

Also noticed that when multiple agents work on the same file, we need better
concurrency control. The current approach might have race conditions.
```

**When** Santiago-PM applies semantic extraction:

**Step 1: Entity Recognition**
```python
entities = extract_entities(log_entry)
# → ["workflow test data system", "KG history", "vector DB", "Redis",
#    "caching", "optimization", "agents", "concurrency control", "race conditions"]
```

**Step 2: Context Analysis**
```python
contexts = analyze_context(entities, log_entry)
# → {
#     "vector DB": {
#         "intent": "explore",
#         "reasoning": "performance concern (slow queries)",
#         "timing": "after basic implementation",
#         "type": "optimization"
#     },
#     "concurrency control": {
#         "intent": "need",
#         "reasoning": "race conditions in multi-agent work",
#         "timing": "now (current approach has issues)",
#         "type": "bug_fix"
#     }
# }
```

**Step 3: Work Item Generation**
```python
work_items = generate_work_items(contexts)
# → [
#     BacklogItem(
#         title="Optimize KG queries with vector DB/Redis caching",
#         type="enhancement",
#         priority=0.60,  # Medium (future optimization)
#         timing="after F-028 basic implementation",
#         reasoning="Performance concern: full KG history slow"
#     ),
#     BacklogItem(
#         title="Fix concurrency control race conditions in multi-agent file access",
#         type="bug",
#         priority=0.85,  # High (current issue)
#         timing="now",
#         reasoning="Current approach has race conditions"
#     )
# ]
```

**Then** Santiago-PM should create:
- 2 backlog items (not just keyword matches)
- Correct types (enhancement vs bug)
- Accurate priorities (future vs now)
- Full context (reasoning, timing, relationships)
- Semantic links (both relate to F-028)

**Acceptance Criteria**:
- [ ] NER (Named Entity Recognition) for domain concepts
- [ ] Intent classification: explore, need, should, consider, worried
- [ ] Timing detection: now, after X, future, someday
- [ ] Reasoning extraction: why is this needed?
- [ ] Relationship detection: relates to F-028, blocks F-030
- [ ] Type classification: feature, bug, task, research, debt
- [ ] Priority hints: "crucial", "worried", "might", "could"
- [ ] Context preservation: full sentence/paragraph saved

---

### Story 3: Intelligent Duplicate Detection (Journeyman)

**As Santiago-PM**
**I want to detect duplicate or highly similar work items**
**So that I don't create redundant backlog items**

**Given** an existing backlog with items:
```yaml
backlog:
  - id: BI-042
    title: "Build conversational questionnaire interface"
    description: "Chat-based questionnaire flow instead of markdown forms"
    source: personal-log:2025-11-17-hank
    created: 2025-11-17T10:00:00Z
  
  - id: BI-055
    title: "Add vector DB for performance optimization"
    description: "Use Redis or vector DB to cache KG queries for speed"
    source: personal-log:2025-11-17-hank
    created: 2025-11-17T12:00:00Z
```

**When** Santiago-PM discovers new potential work:
```yaml
new_discoveries:
  - title: "Conversational UI for questionnaires"
    description: "Make questionnaires chat-based for better UX"
    source: ships-log:issue-234
  
  - title: "Performance: Cache KG with Redis"
    description: "Slow queries need caching layer"
    source: cargo-manifest:F-028-future-enhancements
```

**Then** Santiago-PM should detect duplicates:

**Duplicate Detection Algorithm**:
```python
def is_duplicate(new_item, existing_backlog):
    """
    Multi-factor duplicate detection.
    
    Factors:
    - Semantic similarity (embeddings)
    - Title similarity (fuzzy matching)
    - Description overlap (TF-IDF)
    - Related entities (same concepts mentioned)
    - Source similarity (same person/log)
    """
    for existing_item in existing_backlog:
        # Calculate semantic similarity
        semantic_sim = cosine_similarity(
            embed(new_item.description),
            embed(existing_item.description)
        )
        
        # Calculate title similarity (fuzzy)
        title_sim = fuzz.ratio(
            new_item.title.lower(),
            existing_item.title.lower()
        ) / 100.0
        
        # Check entity overlap
        new_entities = extract_entities(new_item.description)
        existing_entities = extract_entities(existing_item.description)
        entity_overlap = len(new_entities & existing_entities) / len(new_entities | existing_entities)
        
        # Combined similarity score
        similarity = (
            semantic_sim * 0.5 +
            title_sim * 0.3 +
            entity_overlap * 0.2
        )
        
        if similarity > DUPLICATE_THRESHOLD:  # 0.75
            return {
                "is_duplicate": True,
                "matches": existing_item,
                "similarity": similarity,
                "action": "merge" if similarity > 0.85 else "link_as_related"
            }
    
    return {"is_duplicate": False}
```

**Action taken**:
```yaml
# Discovery 1: High similarity to BI-042 (0.92)
action: merge
result:
  - Update BI-042 with additional context from ships-log
  - Add cross-reference: "Also mentioned in ships-log:issue-234"
  - Update priority if new source adds urgency

# Discovery 2: Medium similarity to BI-055 (0.78)
action: link_as_related
result:
  - Keep both items separate (different emphasis)
  - Add semantic link: BI-XXX related_to BI-055
  - Note: "Similar to BI-055 but focuses on Redis specifically"
```

**Acceptance Criteria**:
- [ ] Semantic similarity using embeddings (cosine similarity)
- [ ] Fuzzy title matching (handle typos, synonyms)
- [ ] Entity overlap detection (same concepts = likely duplicate)
- [ ] Threshold tuning: > 0.85 = merge, 0.70-0.85 = link, < 0.70 = separate
- [ ] Merge strategy: combine descriptions, preserve all sources
- [ ] Link strategy: create relationships (related_to, similar_to)
- [ ] Human review: flag uncertain cases (similarity 0.70-0.75)

---

### Story 4: Discovery Pattern Learning (Master)

**As Santiago-PM**
**I want to learn which sources produce the most valuable work items**
**So that I can optimize scanning priorities and predict where innovation happens**

**Given** 3 months of discovery history:
```yaml
discovery_log:
  - source: personal_logs/humans/
    discoveries: 47 items
    value_delivered:
      - BI-042: completed, high value (user satisfaction +30%)
      - BI-055: in-progress, promising
      - BI-023: completed, medium value
    hit_rate: 68% (items completed / items created)
    avg_priority: 0.72
    avg_time_to_start: 3 days
  
  - source: personal_logs/agents/
    discoveries: 31 items
    value_delivered:
      - BI-011: completed, low value
      - BI-028: abandoned (not needed)
    hit_rate: 42%
    avg_priority: 0.55
    avg_time_to_start: 12 days
  
  - source: code_comments/
    discoveries: 89 items (mostly TODOs)
    value_delivered:
      - Many small fixes, few major features
    hit_rate: 34%
    avg_priority: 0.45
    avg_time_to_start: 45 days
  
  - source: ships_logs/
    discoveries: 22 items
    value_delivered:
      - BI-033: completed, critical (unblocked team)
      - BI-041: completed, high value
    hit_rate: 82%
    avg_priority: 0.85
    avg_time_to_start: 1 day
```

**When** Santiago-PM analyzes patterns:

**Pattern 1: Source Quality**
```python
source_quality = analyze_source_quality(discovery_log)
# → {
#     "ships_logs": {
#         "quality": "excellent",
#         "reasoning": "82% hit rate, high priority, fast action",
#         "pattern": "Coordination issues → immediate valuable work"
#     },
#     "personal_logs/humans": {
#         "quality": "very_good",
#         "reasoning": "68% hit rate, high priority, quick action",
#         "pattern": "User insights → high-value features"
#     },
#     "code_comments": {
#         "quality": "fair",
#         "reasoning": "34% hit rate, low priority, slow action",
#         "pattern": "Technical debt → low-priority cleanup"
#     }
# }
```

**Pattern 2: Optimal Scanning**
```python
optimize_scan_frequencies(source_quality)
# → {
#     "ships_logs": "every 5 minutes" (high value, urgent),
#     "personal_logs/humans": "every 10 minutes" (high value),
#     "personal_logs/agents": "every 30 minutes" (medium value),
#     "code_comments": "every 2 hours" (low value, not urgent)
# }
```

**Pattern 3: Predictive Insights**
```python
predict_innovation_sources()
# → {
#     "most_likely_next_breakthrough": "personal_logs/humans",
#     "confidence": 0.78,
#     "reasoning": "47 discoveries in 3 months, 3 high-value features shipped",
#     "recommendation": "Pay extra attention to Hank's personal logs"
# }
```

**Then** Santiago-PM should:
- Adjust scan frequencies based on source quality
- Prioritize high-value sources (ships logs, human personal logs)
- Reduce frequency for low-value sources (code comments)
- Predict where next innovations will come from
- Report insights to team: "Most valuable work comes from coordination issues and user reflections"

**Acceptance Criteria**:
- [ ] Track discovery→completion funnel for each source
- [ ] Calculate hit rate: items completed / items discovered
- [ ] Measure value delivered: user satisfaction, velocity increase
- [ ] Optimize scan frequencies dynamically (not static config)
- [ ] Predict innovation sources (where will next breakthrough come from?)
- [ ] Generate insights for humans: "Your personal logs are our #1 source of innovation"
- [ ] Continuous learning: patterns evolve as team changes

---

### Story 5: Backlog Grooming Automation (Master)

**As Santiago-PM**
**I want to automate continuous backlog grooming**
**So that the backlog is always organized, prioritized, and ready for work**

**Human Pattern** (Traditional weekly grooming):
```yaml
weekly_ceremony:
  frequency: once per week (Friday 2pm)
  duration: 2 hours
  activities:
    - Review new items (30 min)
    - Estimate effort (30 min)
    - Prioritize (45 min)
    - Remove stale items (15 min)
  problems:
    - Stale by mid-week (items added Monday not groomed until Friday)
    - Batch processing (all 50 items at once, fatigue)
    - Context loss (forgot why item was created)
```

**Santiago-PM Pattern** (Continuous grooming):
```yaml
continuous_grooming:
  frequency: every 30 minutes
  duration: 2-5 minutes per cycle
  activities:
    - Review items added since last cycle (1-5 items)
    - Calculate priority (neurosymbolic algorithm)
    - Detect stale items (not touched in 30 days)
    - Cluster related items (find themes)
    - Suggest refactoring (split large items)
  benefits:
    - Always current (items groomed within 30 min of creation)
    - Small batches (1-5 items per cycle, no fatigue)
    - Fresh context (just created, reasoning still clear)
```

**Grooming Workflow**:
```python
def continuous_grooming_cycle():
    """
    Run every 30 minutes to keep backlog healthy.
    """
    # 1. Get items added since last cycle
    new_items = get_items_since_last_grooming()
    
    for item in new_items:
        # 2. Calculate priority (neurosymbolic)
        priority = calculate_priority(item)
        item.priority = priority.score
        item.priority_reasoning = priority.reasoning
        
        # 3. Estimate effort (if not already estimated)
        if not item.effort_estimate:
            estimate = estimate_effort(item)
            item.effort_estimate = estimate.points
            item.effort_reasoning = estimate.reasoning
        
        # 4. Detect relationships
        related = find_related_items(item)
        for rel in related:
            create_link(item, rel, relationship_type="related_to")
        
        # 5. Suggest clustering
        theme = detect_theme(item)
        if theme:
            add_to_cluster(item, theme)
    
    # 6. Detect stale items
    stale_items = get_stale_items(days=30)
    for item in stale_items:
        action = decide_stale_action(item)
        if action == "archive":
            archive_item(item, reason="No activity in 30 days")
        elif action == "escalate":
            create_task("Review stale item", item_id=item.id)
    
    # 7. Detect bloat (too many items)
    if len(backlog) > MAX_ITEMS:
        suggest_backlog_cleanup()
    
    # 8. Generate grooming report
    report = generate_grooming_report(
        new_items_groomed=len(new_items),
        stale_items_found=len(stale_items),
        clusters_updated=True,
        next_cycle=datetime.now() + timedelta(minutes=30)
    )
    
    log_grooming_cycle(report)
```

**Grooming Report Example**:
```yaml
grooming_cycle_report:
  timestamp: 2025-11-17T14:30:00Z
  duration: 3.2 minutes
  
  new_items_groomed: 4
  items:
    - BI-067:
        title: "Fix race condition in multi-agent file access"
        priority: 0.85 (HIGH)
        reasoning: "Critical bug, affects current feature (F-028)"
        effort: 3 points
        related_to: [F-028, BI-042]
        cluster: "concurrency-control"
    
    - BI-068:
        title: "Research Temporal.io workflow testing patterns"
        priority: 0.65 (MEDIUM)
        reasoning: "Research task, informs F-028 design"
        effort: 2 points
        related_to: [F-028]
        cluster: "workflow-testing"
  
  stale_items_archived: 2
  items:
    - BI-012: "Add dark mode to UI" (no activity 45 days, low priority)
    - BI-019: "Investigate GraphQL" (no activity 60 days, exploration)
  
  clusters_updated:
    - "workflow-testing": 7 items (+2 today)
    - "concurrency-control": 3 items (+1 today)
    - "performance-optimization": 5 items (unchanged)
  
  backlog_health:
    total_items: 42
    high_priority: 8
    medium_priority: 19
    low_priority: 15
    avg_age: 12 days
    stale_items: 0 (all archived)
    health_score: 0.87 (excellent)
  
  next_cycle: 2025-11-17T15:00:00Z
```

**Acceptance Criteria**:
- [ ] Continuous grooming: run every 30 minutes
- [ ] Small batches: groom 1-5 items per cycle (no fatigue)
- [ ] Priority calculation: neurosymbolic algorithm with reasoning
- [ ] Effort estimation: use historical data + complexity analysis
- [ ] Relationship detection: find related items automatically
- [ ] Clustering: group by theme (concurrency, testing, performance)
- [ ] Stale detection: archive items with no activity in 30 days
- [ ] Health monitoring: track backlog size, age, priority distribution
- [ ] Human review: escalate uncertain cases (close similarity, complex dependencies)
- [ ] Grooming reports: summary after each cycle (humans can review)

---

## Technical Design

### Scanning Architecture

```python
# Core scanning system
class ContinuousBacklogScanner:
    """
    Continuously scan sources for new work items.
    
    Architecture:
    - Event-driven (git hooks, file watchers)
    - Periodic (cron-like scheduler)
    - Priority-based (scan high-value sources more often)
    """
    
    def __init__(self, sources: List[Source], kg: KnowledgeGraph):
        self.sources = sources
        self.kg = kg
        self.discovery_log = []
        self.last_scan = {}
    
    async def start_continuous_scan(self):
        """Main scanning loop."""
        while True:
            sources_ready = self.get_sources_ready_for_scan()
            
            for source in sources_ready:
                try:
                    discoveries = await self.scan_source(source)
                    await self.process_discoveries(discoveries)
                except Exception as e:
                    log_error(f"Scan failed for {source.name}: {e}")
            
            await asyncio.sleep(self.calculate_next_interval())
    
    async def scan_source(self, source: Source) -> List[Discovery]:
        """Scan a single source for work items."""
        # Get new content since last scan
        new_content = source.get_new_content(since=self.last_scan.get(source.name))
        
        # Extract potential work items
        discoveries = []
        for content in new_content:
            # Semantic extraction
            items = self.extract_work_items(content, source.patterns)
            
            for item in items:
                discovery = Discovery(
                    title=item.title,
                    description=item.description,
                    source=source.name,
                    source_location=content.path,
                    discovered_at=datetime.now(),
                    context=item.context,
                    entities=item.entities,
                    intent=item.intent
                )
                discoveries.append(discovery)
        
        self.last_scan[source.name] = datetime.now()
        return discoveries
    
    def extract_work_items(self, content: str, patterns: List[str]) -> List[WorkItem]:
        """
        Extract work items from unstructured text.
        
        Uses:
        - Pattern matching (keywords, regex)
        - NER (Named Entity Recognition)
        - Intent classification
        - Context analysis
        """
        items = []
        
        # Pattern matching
        for pattern in patterns:
            matches = find_pattern_matches(content, pattern)
            for match in matches:
                # Get context window
                context = get_context_window(content, match, window_size=200)
                
                # NER
                entities = extract_named_entities(context)
                
                # Intent classification
                intent = classify_intent(context)
                
                # Generate work item
                item = WorkItem(
                    title=generate_title(context),
                    description=context,
                    entities=entities,
                    intent=intent,
                    confidence=calculate_confidence(match, context)
                )
                
                if item.confidence > CONFIDENCE_THRESHOLD:
                    items.append(item)
        
        return items
```

### Duplicate Detection

```python
class DuplicateDetector:
    """
    Detect duplicate or similar work items.
    
    Multi-factor similarity:
    - Semantic similarity (embeddings)
    - Title similarity (fuzzy matching)
    - Entity overlap
    - Source similarity
    """
    
    def __init__(self, embedding_model, existing_backlog):
        self.embedding_model = embedding_model
        self.backlog = existing_backlog
        self.similarity_threshold = 0.75
        self.merge_threshold = 0.85
    
    def is_duplicate(self, new_item: Discovery) -> DuplicateResult:
        """Check if new item is duplicate of existing."""
        best_match = None
        best_similarity = 0.0
        
        for existing_item in self.backlog:
            similarity = self.calculate_similarity(new_item, existing_item)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = existing_item
        
        if best_similarity > self.merge_threshold:
            return DuplicateResult(
                is_duplicate=True,
                action="merge",
                match=best_match,
                similarity=best_similarity
            )
        elif best_similarity > self.similarity_threshold:
            return DuplicateResult(
                is_duplicate=True,
                action="link_as_related",
                match=best_match,
                similarity=best_similarity
            )
        else:
            return DuplicateResult(is_duplicate=False)
    
    def calculate_similarity(self, item1: Discovery, item2: BacklogItem) -> float:
        """Multi-factor similarity calculation."""
        # Semantic similarity (embeddings)
        emb1 = self.embedding_model.encode(item1.description)
        emb2 = self.embedding_model.encode(item2.description)
        semantic_sim = cosine_similarity(emb1, emb2)
        
        # Title similarity (fuzzy matching)
        from fuzzywuzzy import fuzz
        title_sim = fuzz.ratio(item1.title, item2.title) / 100.0
        
        # Entity overlap
        entities1 = set(item1.entities)
        entities2 = set(extract_entities(item2.description))
        if entities1 or entities2:
            entity_overlap = len(entities1 & entities2) / len(entities1 | entities2)
        else:
            entity_overlap = 0.0
        
        # Combined similarity
        similarity = (
            semantic_sim * 0.5 +
            title_sim * 0.3 +
            entity_overlap * 0.2
        )
        
        return similarity
```

### Grooming Automation

```python
class ContinuousBacklogGroomer:
    """
    Automate continuous backlog grooming.
    
    Runs every 30 minutes:
    - Prioritize new items
    - Estimate effort
    - Detect relationships
    - Archive stale items
    - Cluster by theme
    """
    
    def __init__(self, backlog, kg, prioritizer):
        self.backlog = backlog
        self.kg = kg
        self.prioritizer = prioritizer  # Neurosymbolic prioritization (F-026)
        self.grooming_interval = timedelta(minutes=30)
        self.stale_threshold = timedelta(days=30)
    
    async def run_grooming_cycle(self):
        """Single grooming cycle."""
        report = GroomingReport(timestamp=datetime.now())
        
        # 1. Get new items since last grooming
        new_items = self.backlog.get_items_since(self.last_grooming_time)
        
        for item in new_items:
            # 2. Calculate priority
            priority_result = await self.prioritizer.calculate_priority(item)
            item.priority = priority_result.score
            item.priority_reasoning = priority_result.reasoning
            
            # 3. Estimate effort
            if not item.effort_estimate:
                effort = await self.estimate_effort(item)
                item.effort_estimate = effort.points
                item.effort_reasoning = effort.reasoning
            
            # 4. Find relationships
            related = await self.find_related_items(item)
            for rel in related:
                self.kg.create_relationship(item, rel, "related_to")
            
            # 5. Detect theme/cluster
            theme = await self.detect_theme(item)
            if theme:
                self.add_to_cluster(item, theme)
        
        report.new_items_groomed = len(new_items)
        
        # 6. Archive stale items
        stale_items = self.backlog.get_stale_items(self.stale_threshold)
        for item in stale_items:
            action = self.decide_stale_action(item)
            if action == "archive":
                self.backlog.archive(item, reason="No activity in 30 days")
                report.stale_items_archived.append(item)
        
        # 7. Calculate backlog health
        report.backlog_health = self.calculate_backlog_health()
        
        # 8. Log and return report
        self.last_grooming_time = datetime.now()
        return report
    
    async def estimate_effort(self, item: BacklogItem) -> EffortEstimate:
        """
        Estimate effort using historical data.
        
        Factors:
        - Complexity (lines of code likely needed)
        - Dependencies (number of related items)
        - Similar past items (how long did they take?)
        - Team velocity (current capacity)
        """
        # Find similar completed items
        similar_items = self.backlog.find_similar_completed(item)
        
        if similar_items:
            # Use historical data
            avg_effort = sum(i.actual_effort for i in similar_items) / len(similar_items)
            confidence = len(similar_items) / 10  # More examples = higher confidence
        else:
            # Fallback: complexity-based estimation
            complexity = self.analyze_complexity(item)
            avg_effort = complexity.estimated_points
            confidence = 0.5
        
        return EffortEstimate(
            points=avg_effort,
            confidence=min(confidence, 1.0),
            reasoning=f"Based on {len(similar_items)} similar items" if similar_items else "Complexity-based estimate"
        )
```

---

## Implementation Phases

### Phase 1: Basic Scanning (Week 1) - MVP

**Goal**: Scan 2 sources (personal logs, ships logs) and create backlog items

**Tasks**:
- [ ] Build source scanner (file watcher + periodic polling)
- [ ] Implement pattern matching (keywords, regex)
- [ ] Create backlog item from discovery
- [ ] Log discoveries (track source, timestamp, context)
- [ ] Scan personal logs every 10 minutes
- [ ] Scan ships logs every 5 minutes

**Deliverables**:
- `ContinuousBacklogScanner` class
- 2 source types supported (personal logs, ships logs)
- Discovery logging (CSV or database)
- Basic pattern matching

**Success Criteria**:
- Scan latency < 30 seconds
- Discover 80% of manually-identified work items
- Zero crashes during 24-hour test run

---

### Phase 2: Semantic Extraction + Duplicate Detection (Week 2)

**Goal**: Extract work items semantically and avoid duplicates

**Tasks**:
- [ ] Implement NER (Named Entity Recognition)
- [ ] Intent classification (need, should, explore, worry)
- [ ] Context window extraction
- [ ] Duplicate detection (semantic similarity)
- [ ] Merge/link strategies
- [ ] Add 2 more sources (cargo manifests, research logs)

**Deliverables**:
- `SemanticExtractor` class
- `DuplicateDetector` class
- 4 source types supported
- Duplicate merge/link logic

**Success Criteria**:
- 95% duplicate detection accuracy
- 70% semantic extraction precision (vs keyword matching)
- Merge decisions: 90% correct (human validation)

---

### Phase 3: Continuous Grooming + Learning (Week 3)

**Goal**: Automate grooming and learn discovery patterns

**Tasks**:
- [ ] Build continuous grooming cycle (every 30 min)
- [ ] Priority calculation integration (neurosymbolic algorithm from F-026)
- [ ] Effort estimation (historical data)
- [ ] Relationship detection (find related items)
- [ ] Stale item archival
- [ ] Discovery pattern analysis (which sources are most valuable?)
- [ ] Dynamic scan frequency adjustment

**Deliverables**:
- `ContinuousBacklogGroomer` class
- `DiscoveryPatternAnalyzer` class
- Grooming reports (after each cycle)
- Source quality metrics

**Success Criteria**:
- Grooming cycle < 5 minutes (for typical backlog size)
- Priority accuracy: 85% (matches human judgment)
- Source quality metrics tracked
- Scan frequencies optimized dynamically

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Discovery completeness | 90% | % of work items found vs manual review |
| Duplicate prevention | 95% | % of duplicates caught before creation |
| Scan latency | < 30s | Time to scan all sources |
| Grooming freshness | < 30 min | Time from creation to grooming |
| Source quality tracking | 100% | All sources have hit rate metrics |
| Backlog health | > 0.80 | Composite score (age, priority distribution, stale %) |
| Human time saved | 80% | Weekly grooming 2hr → 30 min review |

---

## Integration with Existing Features

### With F-027 (Personal Log Feature)
- **Connection**: Personal logs are primary source for discoveries
- **Integration**: Scanner reads personal-logs/ directory continuously
- **Pattern**: Mentions → Semantic extraction → Backlog items
- **Validation**: This feature validates personal log value (tracks hit rate)

### With F-026 (Lean-Kanban Backlog Management)
- **Connection**: Discovered items added to backlog
- **Integration**: Uses neurosymbolic prioritization algorithm
- **Pattern**: Discovery → Grooming → Prioritization → Assignment
- **Enhancement**: Continuous grooming complements manual grooming

### With F-028 (Workflow Test Data System)
- **Connection**: This workflow needs testing
- **Integration**: Create fixtures for scanning/grooming workflows
- **Pattern**: Simulated discoveries → Grooming → Validation
- **Test scenarios**: Multiple sources, duplicates, stale items

### With F-029 (Domain Knowledge Extraction)
- **Connection**: Knowledge mentions are work items too
- **Integration**: Scanner detects domain knowledge → Creates research tasks
- **Pattern**: Mention → Relevance assessment → Task creation
- **Synergy**: Both use semantic extraction pipeline

---

## Related Patterns

### Human Team Pattern (Weekly Grooming)
```yaml
traditional_grooming:
  frequency: weekly
  duration: 2 hours
  batch_size: 50-100 items
  problems:
    - Stale (items added Monday, groomed Friday)
    - Fatigue (too many items at once)
    - Context loss (why was this created?)
  cost: 2 hours × team size (4-8 people) = 8-16 person-hours/week
```

### Santiago-PM Pattern (Continuous Grooming)
```yaml
continuous_grooming:
  frequency: every 30 minutes
  duration: 2-5 minutes per cycle
  batch_size: 1-5 items
  benefits:
    - Fresh (groomed within 30 min of creation)
    - No fatigue (small batches)
    - Context preserved (just created)
  cost: 5 min × 48 cycles/day = 240 min/day = 4 hours/day (automated)
  human_review: 30 min/week (review reports only)
```

**ROI**: 8-16 person-hours/week → 30 min/week = **96% time savings**

---

## Future Enhancements

1. **Natural Language Queries**: "Show me all items related to performance"
2. **Predictive Backlog**: "Based on patterns, you'll need these items next quarter"
3. **Anomaly Detection**: "This item has unusual characteristics (very high effort + low priority)"
4. **Cross-Team Discovery**: Scan other teams' logs for coordination needs
5. **Voice Input**: "Santiago, add to backlog: investigate Redis for caching"
6. **Visual Timeline**: See discovery → grooming → work → completion flow

---

## Metadata

```yaml
cargo_manifest:
  feature_id: F-029
  feature_name: continuous-backlog-discovery
  priority: 0.93 (CRITICAL)
  estimated_effort: 3 weeks
  complexity: high
  risk_level: medium
  
  value_proposition: |
    - Never miss work: Continuous scanning of all sources
    - Better prioritization: Always know what's most valuable
    - Time savings: 96% reduction in grooming time (8-16hr → 30min/week)
    - Pattern learning: Discover where innovation comes from
    - Quality: 95% duplicate prevention, 90% discovery completeness
  
  key_insight: |
    Santiago-PM can scan more frequently than humans (no fatigue, context switching cost).
    Continuous grooming >> weekly ceremony (fresher context, smaller batches, no fatigue).
    Discovery pattern learning enables optimization (scan high-value sources more often).
  
  phases:
    - phase: 1
      name: basic_scanning
      duration: 1 week
      deliverables: Scanner, 2 sources, pattern matching
      critical: true
    
    - phase: 2
      name: semantic_extraction
      duration: 1 week
      deliverables: NER, duplicate detection, 4 sources
      critical: true
    
    - phase: 3
      name: continuous_grooming
      duration: 1 week
      deliverables: Grooming automation, pattern learning
      critical: false
  
  dependencies:
    - F-026: Neurosymbolic prioritization (for grooming)
    - F-027: Personal logs (primary source)
  
  enables:
    - F-028: Workflow testing (test this workflow)
    - Future: Predictive backlog (know what's needed next)
  
  discovered_via:
    conversation: "User described PM scanning pattern, weekly grooming ceremony"
    date: 2025-11-17
    context: "Discussing difference between human PM (weekly) and AI PM (continuous)"
```

---

**Meta**: This feature creates a continuous feedback loop:
- Personal logs → Discoveries → Backlog items → Work → Learning → Better prioritization
- The system learns where good ideas come from and optimizes scanning accordingly
- Continuous grooming eliminates weekly ceremony (Kerievsky: "Deliver Value Continuously")
- Discovery pattern learning enables meta-learning (learning about learning)

**Self-reference**: This cargo manifest itself was discovered from a conversation, demonstrating the very pattern it describes. If Santiago-PM scans this artifact, it should recognize: "This is F-029, it describes how I should scan for work. Meta!" 🚢
