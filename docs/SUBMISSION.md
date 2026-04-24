# Submission Packaging Guide

> **How to prepare AaCT-E/demo for FAA/TSSC or SBIR submission.**

---

## Pre-Submission Checklist

### 1. Version Lock

```bash
git tag -a v0.2.0 -m "feat: access layer, submission packaging"
git push origin v0.2.0
```

**Why:** Reviewers must reference an immutable version, not a moving branch.

### 2. Verify CI Passes

Check GitHub Actions: `https://github.com/AaCT-E/demo/actions`

- All Python versions (3.10–3.13) must pass
- `verify_demo.py` must print `Verification PASSED`
- Traces must be uploaded as artifacts

### 3. Generate Release Assets

The release workflow (`.github/workflows/release.yml`) automatically creates:

| Asset | Description |
|-------|-------------|
| `aacte-demo-v0.2.0.zip` | Full repo snapshot |
| `traces-v0.2.0.zip` | Reproducible trace artifacts |
| `SHA256SUMS` | Cryptographic checksums |

**Manual verification:**
```bash
python -m access.cli --json > status.json
sha256sum outputs/*.json >> SHA256SUMS
```

### 4. Update Citation

Ensure `CITATION.cff` matches the tag:

```yaml
version: 0.2.0
date-released: 2026-04-24
```

### 5. Notify Publisher

The Publisher repo auto-ingests releases. Verify:

- `GCAT-BCAT-Engine/Publisher` has archived the traces
- Social media scheduler queued the release announcement
- Paper submissions reference `v0.2.0` in their methodology section

---

## Submission Package Contents

### For FAA/TSSC Review

Include in your proposal:

1. **Link:** `https://github.com/AaCT-E/demo/releases/tag/v0.2.0`
2. **Instructions:** `docs/ACCESS.md` (Path 1: Direct Clone)
3. **Evidence:** `traces-v0.2.0.zip` from the release page
4. **Checksum:** `SHA256SUMS` for integrity verification
5. **Citation:** `CITATION.cff` BibTeX block

### For SBIR Phase I

Include in your submission:

1. **Technical Merit:** Reference `DEMO_SPEC.md` for exact methodology
2. **Commercialization Path:** Reference `docs/PROCUREMENT.md`
3. **Reproducibility:** Include the one-line verification command:
   ```bash
   git clone --branch v0.2.0 https://github.com/AaCT-E/demo.git && cd demo && python verify_demo.py
   ```
4. **Phase II Roadmap:** Reference `CHANGELOG.md` for planned expansion

---

## Post-Submission Freeze

After submission:

- **Do NOT delete the tag.** Tags are permanent references.
- **Do NOT force-push to main.** History must remain intact.
- **Do NOT modify release assets.** If fixes are needed, create `v0.2.1`.

---

## Emergency Fixes

If a critical bug is found post-submission:

1. Create `v0.2.1` with the fix
2. Update `CHANGELOG.md` with the delta
3. Notify Publisher to update paper references
4. Submit errata to the reviewing agency

**Never modify an existing release.** Always version forward.

---

## Contact

For submission questions: open an issue at `github.com/AaCT-E/demo/issues`
For ecosystem coordination: contact `GCAT-BCAT-Engine/Publisher` maintainers
