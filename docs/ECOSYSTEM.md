# AaCT-E Ecosystem Guide

## Where This Repo Sits

```
┌─────────────────────────────────────────────────────────────┐
│                     GCAT / BCAT  ECOSYSTEM                   │
├─────────────────────────────────────────────────────────────┤
│  THEORY LAYER                                                │
│  ├─ GCAT-BCAT-Engine          Formal proofs, metrics        │
│  ├─ GCAT-BCAT-Engine/Publisher Paper publishing pipeline     │
│  └─ Gemstone_IV               Rigel geometry & benchmarks     │
├─────────────────────────────────────────────────────────────┤
│  DEMONSTRATION LAYER                                         │
│  └─ AaCT-E/demo  ◄── YOU ARE HERE                          │
│      Minimal, runnable, verifiable procurement evidence       │
├─────────────────────────────────────────────────────────────┤
│  OPERATIONAL LAYER                                           │
│  ├─ StegVerse-Labs/StegDB     Entity sandbox & monitoring    │
│  ├─ StegVerse-Labs/SDK        User-facing validation         │
│  └─ StegVerse-Labs/Site       Public presence & docs         │
└─────────────────────────────────────────────────────────────┘
```

## Integration Points

### Upstream: GCAT-BCAT-Engine/Publisher
- Theory papers feed into procurement narratives
- Publisher repo manages submission tracking, social media, release timing
- AaCT-E demo provides the "run it yourself" evidence for those papers

### Downstream: StegDB
- `stegdb_hooks/emit_status.py` runs after every CI verification
- Emits structured health reports to `last_status.json`
- StegDB ingests these to track ecosystem-wide repo health

### Sibling: StegVerse-Labs/SDK
- SDK is user-facing; AaCT-E is reviewer-facing
- Both validate the same core concepts through different interfaces

## Release Strategy

| Stage | Trigger | Action |
|-------|---------|--------|
| Alpha | Now | Repo private, CI running, traces verified |
| Beta | Pre-submission | Flip to public, org profile live, citation indexed |
| Release | SBIR/FAA submission | Tag v0.1.0, archive traces, link from proposal |

## Monitoring

- **CI**: Daily scheduled runs across Python 3.10–3.13
- **StegDB**: Ingests `last_status.json` after each run
- **Publisher**: Tracks which papers reference this demo

## Contact & Contribution

- Issues: [github.com/AaCT-E/demo/issues](https://github.com/AaCT-E/demo/issues)
- Discussions: [github.com/GCAT-BCAT-Engine](https://github.com/GCAT-BCAT-Engine)
