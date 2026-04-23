# Digital Products — Security Baseline

Applies to every product in `../projects/` that belongs to this portfolio.
Extends workspace `../FRAMEWORK.md` security rules with distribution-level concerns.

---

## Core Principles

- **Local means local.** If a product advertises offline/local processing, that
  promise must be testable and verifiable by a user with a network sniffer.
- **No silent uploads.** Zero media bytes, filenames, thumbnails, or media-derived
  hashes leave the device without explicit, disclosed opt-in.
- **No silent telemetry.** Analytics are opt-in, anonymous, and documented in the
  product's `docs/privacy.md`. Never collect user file paths or content.
- **Secrets never touch the binary.** No API keys, tokens, or signing keys
  embedded in distributed builds. License keys are user-visible strings validated
  against the merchant-of-record API.

---

## Distribution Trust

| Channel | Required |
|---|---|
| Web app | HTTPS, valid certificate, COOP/COEP headers for WASM, SRI for third-party scripts |
| Windows desktop | Code signing (EV or standard), SmartScreen-aware rollout plan |
| macOS desktop | Apple Developer ID + notarization + stapling before public release |
| Linux desktop | GPG-signed tarball + checksums |
| iOS app | App Store review, privacy nutrition labels accurate, no unapproved third-party SDKs |
| Android app | Play Console review, signed APK/AAB, Data Safety form accurate |

Checksums (SHA-256) published for every downloadable artifact.

## Signing Cost Reality

Signing costs money. For early-stage products where revenue < $500/mo:

| Platform | Acceptable early stance |
|---|---|
| Web | Vercel/Cloudflare free TLS — no cost |
| Windows | Ship unsigned with documented SmartScreen workaround; upgrade to signed cert when revenue justifies ($80–$300/yr) |
| macOS | Ship unsigned with `xattr -d com.apple.quarantine` instructions; upgrade to Developer ID ($99/yr) when revenue justifies |
| Android | Play Store cert is free (one-time $25 developer fee); sign from day one |
| iOS | Apple Developer $99/yr required — defer until revenue exists or v1 is web-only |

Document any unsigned distribution in `docs/troubleshooting.md` with clear user
instructions for the OS-level warning.

---

## Dependency Hygiene

- Dependency scanning (e.g. `npm audit`, Dependabot) runs in CI on every PR.
- License scanning on every release candidate — no GPL or viral licenses in
  production builds without explicit review.
- SBOM (CycloneDX or SPDX) generated per release and stored with release artifacts.

---

## Input Handling

- Sanitise filenames aggressively before passing to subprocess engines (FFmpeg, etc).
  Never use shell interpolation with user-provided strings.
- Treat user files as sensitive: temp work in an isolated scratch directory, clean
  on success, failure, cancel, and tab-close.
- Fail loud and safe: refuse to process files that can't be parsed; never assume
  container integrity.

---

## Crash & Log Policy

- Crash logs must redact absolute file paths (keep only basenames).
- Before a crash log can be shared with support, the user sees exactly what is
  included and consents.
- No media content, no user filenames leave the device in logs.

---

## Vulnerability Disclosure

Each product ships a `SECURITY.md` in its repo with:
- How to report (email or form)
- Expected acknowledgement time (7 days)
- Safe-harbour language for good-faith researchers
