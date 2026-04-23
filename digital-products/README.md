# Digital Products Portfolio

Workspace-level portfolio for small, paid, repeatable digital products built under
the TFS brand and (later) other TCode-hosted brands.

This folder is **shared portfolio standards only** — individual products live in
`../projects/<product-name>/` following TCode's project convention.

---

## Portfolio Goals

1. Ship small, sharply-scoped digital products that each solve one pain point.
2. Reuse one SDLC contract, one security baseline, one release policy across every product.
3. Favour low-bookkeeping commercial models (merchant-of-record billing, no custom license servers).
4. Launch fast, iterate on revenue, skip premature platform coverage.

## Framework Files

| File | Purpose |
|---|---|
| [`FRAMEWORK.md`](FRAMEWORK.md) | Portfolio SDLC — extends workspace `../FRAMEWORK.md` with product-specific rules |
| [`SECURITY.md`](SECURITY.md) | Security baseline for distributed consumer software |
| [`RELEASE_POLICY.md`](RELEASE_POLICY.md) | Signing, notarization, checksums, rollback |
| [`PRICING_POLICY.md`](PRICING_POLICY.md) | Tiering philosophy, merchant-of-record choice, anti-adware rules |

## Products in this portfolio

| Product | Status | Location |
|---|---|---|
| TFS Shrinks | Kickoff | `../projects/tfs-shrinks/` |

> Add new products here as they are scaffolded. Each product entry should link back
> to its `PRODUCT_BRIEF.md`.

---

## How to add a new product

1. Scaffold under `../projects/<product-name>/` following TCode project layout.
2. Add `PRODUCT_BRIEF.md` that references this folder's `FRAMEWORK.md`.
3. Register in `../devops/config.yaml` and in workspace `memory/MEMORY.md`.
4. Register here in the Products table above.
