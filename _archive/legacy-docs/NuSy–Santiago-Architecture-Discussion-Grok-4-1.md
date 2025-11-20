# NuSy Santiago Architecture Discussion - Grok 4.1 Integration

## 📚 Legal EPUB Sources for Medical Information Retrieval

### Primary Recommendations for Clinical-Grade Systems

#### 1. Local Library Services (Best for Modern Books)
- **Libby (OverDrive)**: Free app for iOS/Android/Windows/Mac. Borrow EPUBs instantly with library card. No waitlists for older titles. Send to Kindle supported.
- **Hoopla**: Library service with EPUBs, audiobooks, comics. No waitlists.

#### 2. Public Domain & Classics (Permanent Downloads)

| Site | Key Features | # of Free EPUBs | Notes |
|------|-------------|-----------------|-------|
| **Project Gutenberg** | Clean, proofread classics | 70,000+ | Pride and Prejudice, Sherlock Holmes |
| **Standard Ebooks** | Modern formatting of public domain | Thousands | Highly recommended for best reading experience |
| **Internet Archive / Open Library** | Millions of titles, controlled digital lending | Millions | Create account to borrow modern-ish titles |
| **ManyBooks** | Curated public domain + free indie | 50,000+ | Multiple formats, nice covers |
| **Smashwords** | Indie authors, permanently free/promotional | 100,000+ free | Great for romance, sci-fi, self-help |
| **Feedbooks** | Clean EPUBs of classics | Thousands | Simple and ad-free |

#### 3. Other Legal Sources
- **Amazon Kindle Store**: Filter by "Free" for classics + promotional modern books
- **Google Play Books**: Free section with classics and promos
- **Kobo Store**: Strong free classics section + frequent

## 🔌 API Interfaces for Programmatic Access

### Available APIs for EPUB Sources

| Source | Public/Programmatic API? | Details |
|--------|-------------------------|---------|
| **Project Gutenberg** | Yes (strong third-party support) | Gutendex – JSON REST API for search, filters, metadata, and direct EPUB links |
| **Standard Ebooks** | No API | Only bulk ZIP downloads for Patrons-circle donors |
| **Internet Archive / Open Library** | Yes (excellent) | Full-featured RESTful APIs for search, metadata, covers, and borrow/lend status |
| **Libby (OverDrive)** | Yes, but restricted | Developer portal with discovery, checkout, and metadata APIs. Requires partnership |
| **Hoopla** | Yes, but restricted | Partner/developer portal with catalog search, metadata, and availability APIs |
| **ManyBooks** | No | Manual browsing/download only |
| **Smashwords** | Limited (affiliate-focused) | Affiliate tools and data feeds, no modern public REST API |
| **Feedbooks** | No current API | OPDS feeds may work for some catalogs |

### Best Options for Programmatic EPUB Access (2025)
- **Gutendex** → For classics/public domain (70,000+ EPUBs). Simple, free, no key required
- **Open Library / Internet Archive APIs** → Broader coverage (millions of borrowable or downloadable EPUBs)

## 🏥 Clinical-Grade Medical Information Sources

### Gold-Standard Clinical Sources with Programmatic Access

| Source | Format | Programmatic Access | License / Safety | Notes |
|--------|--------|-------------------|------------------|-------|
| **NCBI Bookshelf / PubMed Books** | HTML + EPUB export | Full REST API (Entrez E-utilities) + bulk FTP | U.S. government work — public domain or CC-BY | 1,000+ open textbooks (Harrison's, GeneReviews, NCBI's own medical books) |
| **Open Textbook Library** | EPUB + PDF | Open API + OAI-PMH harvest + bulk ZIP | Almost all CC-BY or CC-BY-SA | 1,000+ university-level health sciences textbooks |
| **MedOne Education (Thieme)** | EPUB | Official OAuth2 API for institutions | Institutional license (auditable) | Full EPUB download + chapter-level access |
| **Directory of Open Access Books** | EPUB | OAI-PMH + REST API | All CC or open licenses | 80,000+ academic books, strong medicine section |
| **Internet Archive CDL** | EPUB/PDF | Open Library API + IA bulk API | Fair-use lending (1:1 owned:lent ratio) | Borrow Harrison's 21e, Guyton physiology, etc. for 14 days |
| **Europe PMC Bookshelf** | EPUB/XML | Full REST API + FTP | CC-BY or public domain | European open textbooks |

### Recommended Primary Stack for Santiago (2025)
1. **Primary**: NCBI Bookshelf (gold standard, public domain, versioned)
2. **Secondary**: Open Textbook Library + DOAB (CC-BY academic textbooks)
3. **Tertiary**: Institutional MedOne / AccessMedicine API (if licensed)
4. **Fallback**: Open Library / IA CDL (controlled digital lending)

### Python Starter for NCBI Bookshelf EPUB Retrieval
```python
import requests
import xml.etree.ElementTree as ET

def get_ncbi_book_epub(book_id: str):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=books&id={book_id}"
    r = requests.get(url)
    root = ET.fromstring(r.content)

    # Find EPUB download link
    for link in root.findall(".//BookDocument//Link"):
        if link.get("format") == "epub":
            return link.get("href")
    return None

# Example: GeneReviews (clinical gold standard)
epub_url = get_ncbi_book_epub("NBK222584")
print(epub_url)  # → direct .epub you can wget/curl
```

## 🤖 Grok 4.1 Access & Integration

### Current Tier Mapping for Grok 4.1

| Subscription Plan | Grok 4.1 Access? | How to Use | Context Window | Notes |
|------------------|------------------|------------|----------------|-------|
| **Free tier** | No | — | — | Grok 3 only |
| **SuperGrok (paid)** | Yes | Web UI + API (model name: grok-4.1) | 128k–256k | Highest priority & rate limits |
| **X Premium+** | Yes | Web/chat + API (same grok-4.1 endpoint) | Same | Same model as SuperGrok |
| **xAI API tier** | Yes | grok-4.1 or grok-4.1-128k | Up to 256k | Pay-as-you-go |

### Testing Grok 4.1 Access
```bash
curl https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer YOUR_XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4.1",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0
  }'
```

## 🧠 Grok Projects (Long Context Memory)

### Current Features (November 2025)

| Feature | Available Now? | Where it works | Details |
|---------|----------------|----------------|---------|
| **Persistent Project Memory** | Yes (beta) | console.grok.com → "Projects" tab | Create named projects with full conversation history + uploaded documents |
| **Shared between web chat and API** | Partial | Same backing store | Continue web threads via API using project_id parameter |
| **Direct API continuation** | Yes | Live in API | project_id in chat/completions endpoint |
| **Team sharing & permissions** | Yes | Invite by email | Full scrollback access with role-based permissions |
| **Cross-interface sync** | 90% | Web ↔ API ↔ Console | @mention or link projects from any interface |

### Setting Up a NuSy Project
1. Go to https://console.grok.com/projects
2. Click "New Project" → Name it "NuSy Santiago Core"
3. Upload initial files (architecture diagrams, medical corpus, etc.)
4. Set custom instructions for the project
5. Copy the project_id for API use

### API Usage with Projects
```python
import os
import xai

client = xai.Client(api_key=os.getenv("XAI_API_KEY"))

response = client.chat.completions.create(
    model="grok-4.1",
    project_id="proj_1a2b3c4d5e6f7g8h9i0j",  # Your shared NuSy project
    messages=[
        {"role": "system", "content": "Continue the Santiago clinical retrieval module design..."},
        {"role": "user", "content": "Add the new NCBI ingestion code we discussed"}
    ],
    temperature=0.0
)
```

## 🏗️ Multi-Layer Memory Architecture

### Memory Hierarchy for NuSy Team

| Layer | Name in xAI | Scope | Sharing | Persistence | API-accessible | Best for |
|-------|-------------|-------|---------|-------------|----------------|----------|
| **1** | Personal Memory | One user only | Private by default | Forever | Yes (auto-bound to API key) | Domain expert's private long-term memory |
| **2** | Project (Workspace) | Many users | Invite-by-email, role-based | Forever + versioned files | Yes → project_id | Shared team contexts |
| **3** | Organization Memory | Entire org/team | Inherited by all members | Forever, admin governed | Rolling out this month | Global medical knowledge base |
| **4** | Agent-Specific Memory | Per-agent thread | Private or attached to Project | Forever | Yes — agent_id + memory_stream_id | Each NuSy being's infinite scrollback |

### Implementation for NuSy
- **Shared backbone**: "NuSy Master Brain" (architecture, EPUB corpus, licensing)
- **Domain-specific sub-projects**: "NuSy Oncology Expert", "NuSy Pharmacology", etc.
- **Private memories**: Individual team members' long-running conversations

## 🔄 Cross-Interface Project Sharing

### How to Share Conversations Between Interfaces

| Interface | How to Attach/Share | Result |
|-----------|-------------------|--------|
| **This chat (x.com)** | Type `@ProjectName` or use menu → "Move conversation to..." | Thread becomes part of Project's permanent memory |
| **Web console** | Create Project, invite team members | Full scrollback visible to all invitees |
| **API calls** | Include `project_id` in requests | Model sees entire project history + files |

### Creating a Santiago Project
Simply say: *"Move this entire conversation into a new shared Project called 'Santiago'"*

This instantly:
- Creates the "Santiago" project
- Moves all conversation history into it
- Makes it accessible across all interfaces
- Enables team collaboration

## ⚡ Productivity Setup for xAI Developers & PMs

### Recommended Tools for Deep Architecture Work

| Goal | Tool/Setup | Why it's gold standard | Setup time |
|------|------------|----------------------|------------|
| **Infinite context canvas + real-time collab** | Cursor (cursor.sh) with xAI account | Full Grok 4.1 integration, native Projects/memory support | 5 minutes |
| **Voice-to-text architecture sessions** | Cursor + WhisperKit or MacWhisper Pro | Talk for an hour; transcribes + formats perfectly | Free-fast tier |
| **Diagram-as-code that stays in context** | Mermaid Live + Excalidraw in Cursor/Grok Projects | Grok 4.1 can edit diagrams live; all stay versioned | No extra tools |
| **Second brain synced with Grok** | Obsidian + obsidian-grok plugin | Every note can @mention Projects; Grok reads entire vault | Optional |
| **Fastest Grok 4.1 loop** | Grok web console full-screen + Raycast/Arc | Cmd-T → "grok" → instant access with full memory | Free |

### Morning Architecture Session Setup
- **Left monitor**: Cursor full-screen (whole codebase + Grok sidebar)
- **Right monitor**: Grok web console in dedicated Project
- **Voice input**: MacWhisper running (⌥-Space hotkey)
- **Diagrams**: Mermaid + Excalidraw tabs pinned
- **Quick access**: Raycast with custom Grok command

This setup enables hours of deep architectural work with zero friction, full context preservation, and seamless team collaboration.