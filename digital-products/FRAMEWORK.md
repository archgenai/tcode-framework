# Digital Products Framework
# Portfolio-level SDLC contract. Extends workspace `../FRAMEWORK.md`.
# Every product under `../projects/<name>/` that is part of the Digital Products
# portfolio MUST reference this file in its PRODUCT_BRIEF.md.

---

## Inheritance

This framework extends the workspace-level `../FRAMEWORK.md`. Workspace rules apply in
full. This file only records rules that are specific to *paid, distributed, consumer-facing*
digital products.

| Rule source | Covers |
|---|---|
| `../FRAMEWORK.md` | Code quality, testing, memory system, DevOps, commit format |
| This file | Productisation, distribution, pricing, release trust, user adoption, support |

---

## Product Factory Principles

Every digital product in this portfolio must obey these non-negotiable rules.

| Principle | Non-negotiable rule |
|---|---|
| Small, sharp problem | One pain point, one sentence. No "platform" nonsense. |
| Offline-first when possible | Local processing is the default. Never force uploads for jobs that can run on-device. |
| Paid utility, not adware | No dark patterns, no fake scarcity, no pop-ups. |
| Predictable outputs | User picks a target; tool explains the tradeoff in human terms. |
| Platform discipline | Every shipped platform (web, desktop, iOS, Android) is treated intentionally — no accidental ports. |
| Docs as product surface | Help, FAQ, troubleshooting ship on day one. |
| Release trust | Signed binaries (when native), checksums, reproducible release notes. |

---

## Commercial Model Rules

1. **Merchant of record preferred.** Use Lemon Squeezy, Paddle, or Gumroad for
   subscriptions and one-time buys. Do NOT build a custom license server or
   subscription billing pipeline unless revenue exceeds $10k/mo and the MoR fee
   is demonstrably the bottleneck.
2. **Hybrid tiers allowed.** A product may offer both one-time ("Lite") and
   subscription ("Pro", "Ultimate") tiers if the subscription delivers recurring
   value (ongoing preset updates, cloud features, team seats, API access).
3. **Free tier must be usable.** Enough to prove the product works. Never a
   crippled trial that shows only screenshots. Always watermark or cap duration
   to preserve upgrade pressure.
4. **Pricing floors.** No product is priced below $19 one-time or $3/mo. Cheap
   pricing signals cheap quality; premium positioning is the default.
5. **No subscription for pure local utility.** If a product has zero ongoing
   cloud value, do not add a subscription tier just to recur revenue.
6. **Refund policy is public.** 14-day no-questions refund, self-service via
   the MoR dashboard.

See [`PRICING_POLICY.md`](PRICING_POLICY.md) for the full tiering philosophy.

---

## User Adoption Standards

- **Time-to-value**: first successful outcome in one session, without reading docs.
- **Explainability**: user understands *why* the tool did what it did.
- **Determinism**: same input + same preset → same output, reproducibly.
- **Low-regret purchase**: trial or free tier, clear refund, no bait pricing.
- **Supportability**: FAQ, troubleshooting, known-limits doc live on day one.

---

## Required Product Documents

Every digital product in this portfolio carries these documents under its project
folder (in addition to TCode-standard `APP_SPEC.md`, `STACK.md`, `REQUIREMENTS.md`):

| File | Purpose |
|---|---|
| `PRODUCT_BRIEF.md` | Problem, value prop, positioning, target users, pricing |
| `README.md` | Human-facing intro — what it is, who it's for, how to use |
| `CHANGELOG.md` | Release history, semver |
| `docs/user-guide.md` | Normal-mode walkthrough |
| `docs/troubleshooting.md` | Common errors and fixes |
| `docs/privacy.md` | What is and is not collected |
| `docs/release-checklist.md` | Pre-ship gate list (see `../RELEASE_POLICY.md`) |

---

## Test Gates

Workspace-level test rules apply (`../FRAMEWORK.md`). Digital products add:

| Layer | Must pass before release |
|---|---|
| Unit | Preset mapping, validation, file naming |
| Integration | Real engine runs on sample assets |
| Golden media | Before/after reference outputs on a curated test corpus |
| UX smoke | Open app, run core flow, cancel, retry — on every target platform |
| Security | Input fuzzing (filenames, paths), temp-file cleanup, no hidden uploads |
| Release | Installer integrity, signing, checksum, clean-room install test |

Media test corpus: short clip, long clip, vertical phone video, high-motion,
screencast, low-light, multiple audio tracks, odd rotation metadata, huge file,
broken/corrupt file.

---

## Repository Layout (portfolio-level)

```
digital-products/                     ← this folder
├── FRAMEWORK.md
├── SECURITY.md
├── RELEASE_POLICY.md
├── PRICING_POLICY.md
└── README.md

projects/<product-name>/              ← individual products (TCode convention)
├── CLAUDE.md                         ← project adapter
├── APP_SPEC.md                       ← input form
├── PRODUCT_BRIEF.md                  ← product-level brief (this framework)
├── REQUIREMENTS.md                   ← phased feature plan
├── STACK.md                          ← live tech ledger
├── README.md
├── CHANGELOG.md
├── docs/
├── src/
├── tests/
└── memory/
```

---

## References

Portfolio framework seeded from:
- TCode workspace `../FRAMEWORK.md`
- `Project_Kickoffs/Digital_Products/digital_products_kickoff_video_compressor.pdf` (2026-04-17)
- `Project_Kickoffs/Digital_Products/TFS_SHRINKS_v2_addendum.md` (2026-04-18)
