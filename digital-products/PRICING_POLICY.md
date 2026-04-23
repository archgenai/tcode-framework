# Digital Products — Pricing Policy

The tiering philosophy for every product in this portfolio.

---

## Goals

1. **Signal quality through price.** No $2 or $4 products — those read as
   unmaintained side projects. Floor: $19 one-time or $3/mo.
2. **Anchor high, convert at Pro.** Ladder is structured so the "Pro" tier feels
   like the obvious choice next to a premium Ultimate.
3. **Minimise bookkeeping.** Merchant-of-record handles tax, chargebacks, refunds.
4. **Preserve upgrade pressure without adware.** Free tier is usable but clearly
   capped; no fake scarcity, no nag pop-ups, no timed-out flashing banners.

---

## Standard Tier Ladder

Every digital product should map into this shape, even if the names or limits differ.

| Tier | Model | Typical price range | Role |
|---|---|---|---|
| **Free** | Forever free, capped | $0 | Trial + word-of-mouth lever |
| **Lite** | One-time purchase | $19 – $49 | Entry for subscription-averse buyers |
| **Pro** | Monthly or annual sub | $9 – $19/mo, $79 – $149/yr | The main offer |
| **Ultimate** | Premium sub + optional lifetime | $19 – $39/mo, $199 – $249/yr, $299 – $499 lifetime | Agencies, teams, anchor |

Products may skip Lite if every user benefits from ongoing updates. Products may
skip Ultimate if there's no team/API/agency segment to serve. Free is never skipped.

---

## Free Tier Rules

- Always usable end-to-end for one task (no "pay to export" at the final step).
- Hard caps enforced in the engine layer, not trusted to UI state.
- Watermark or duration cap is acceptable. Fake "upgrade required" walls that
  mock the paid experience are not.

## Lite Tier Rules

- One-time purchase. Includes 12 months of minor updates.
- Major upgrades may be paid (typically 50% of new price for existing Lite owners).
- Locked to a small number of devices (1–3), validated by merchant-of-record license key.

## Pro Tier Rules

- Ongoing value: preset updates, new features, platform specs kept current.
- 3 devices by default.
- Annual discount ≥ 30% vs monthly × 12.

## Ultimate Tier Rules

- Adds agency/team features: multiple seats, API access, scheduled exports,
  white-label, priority support.
- Optional "lifetime" price at 2–3× annual — caps LTV but captures users who
  refuse subs; use sparingly.
- Includes bundled access to future products in the portfolio (TFS Shrinks
  Ultimate customer gets future TFS digital products free or at a discount).

---

## Merchant-of-Record Defaults

Preferred: **Lemon Squeezy** (merchant of record, license keys built in, low
integration overhead). Fees ~5% + $0.50 per transaction.

Acceptable alternatives:
- **Paddle** — similar to LS, slightly more polish for B2B.
- **Gumroad** — simpler still, higher fee (~10%), best for products < $50.
- **Stripe direct** — only when revenue > $10k/mo and tax complexity is managed
  via a separate service (Stripe Tax, TaxJar). Never the default.

---

## Refund Policy

- **14-day no-questions refund** via merchant-of-record self-serve portal.
- On refund: license key revoked, app downgrades to Free on next online check.
- No manual exceptions — discipline > short-term revenue.

---

## Anti-Adware Rules

- No email capture walls before the free tier works.
- No "upgrade" pop-ups during active work.
- Upgrade prompts allowed: on first-run, in a settings/about panel, and after a
  clear user action that hits a paid feature (shown once, then remembered).
- No dark patterns in cancellation — cancel must take ≤ 2 clicks from the MoR portal.
