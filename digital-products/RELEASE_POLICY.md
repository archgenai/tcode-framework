# Digital Products — Release Policy

Applies to every product in this portfolio.

---

## Versioning

- **Semver** (`MAJOR.MINOR.PATCH`) for every product.
- Minor-version updates are free for all paying tiers during the stated support window.
- Major versions may be a paid upgrade for "Lite" (one-time) tier; always free for
  active subscribers.

---

## Release Channels

| Channel | Audience | Signing |
|---|---|---|
| `dev` | Internal only | Unsigned, local build |
| `beta` | Opted-in testers | Signed where supported, checksum published |
| `stable` | Public | Signed + notarized where supported, checksum + SBOM published |

---

## Pre-Release Checklist

Every product's `docs/release-checklist.md` must cover:

- [ ] All unit + integration + golden-media + security + UX tests pass
- [ ] Changelog updated with user-facing summary
- [ ] Version bumped in all manifests (package.json, Tauri, Capacitor iOS/Android, etc.)
- [ ] `docs/user-guide.md` screenshots regenerated if UI changed materially
- [ ] Privacy statement reviewed if any data-handling changed
- [ ] License-gate happy path tested end-to-end against live merchant-of-record sandbox
- [ ] License-gate revocation path tested (cancelled subscription → downgrade)
- [ ] Offline-grace path tested (disable network → app still works for grace window)
- [ ] Installer integrity verified on a clean VM (or equivalent sandbox)
- [ ] Checksums generated and published next to artifacts
- [ ] SBOM generated and attached to release
- [ ] Rollback artifact prepared (previous stable version retained for at least 90 days)

---

## Distribution

Products may ship on any combination of:

- **Direct download** from the product website (primary for margin)
- **Merchant-of-record storefront** (Lemon Squeezy / Paddle / Gumroad product page)
- **Microsoft Store** (Windows)
- **Mac App Store** (macOS)
- **Apple App Store** (iOS)
- **Google Play Store** (Android)
- **Setapp** (macOS subscription bundle — favourable for subscription tiers)
- **Indie directory listings** (AlternativeTo, Product Hunt, etc.)

Each product records its active channels in `STACK.md`.

---

## Rollback

- Every release tag has a matching rollback artifact stored for ≥ 90 days.
- Auto-update (when shipped) checks for a "last known good" pointer before applying.
- If a release is yanked, users on the bad version are notified via in-app banner
  on next launch.

---

## Commit & Tag Conventions

- **Conventional Commits** (workspace rule; see `../FRAMEWORK.md`).
- Release commits: `chore(release): <product> v<semver>`
- Release tag: `<product>-v<semver>` (e.g. `tfs-shrinks-v1.0.0`)

---

## Kill-Switch Discipline

No kill-switches that brick legitimate customers.
- License revocation applies only to confirmed stolen/refunded keys.
- Cancelled subscriptions downgrade to the free tier, never to a broken state.
- Offline users get a minimum 30-day grace before re-validation prompts.
