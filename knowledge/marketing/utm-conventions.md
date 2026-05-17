# UTM Conventions — Agency Standard

Versi: 1.0 (Update 11)
Last updated: 2026-05-17
Audience: BrandFlow agents — `@brandflow.analytics`, `@brandflow.social`, `@brandflow.copywriter`, `@brandflow.cmo`

---

## Why a Convention

UTMs (Urchin Tracking Module parameters) attach metadata to URLs so analytics can attribute clicks to a specific source/medium/campaign/piece. Without a convention:

- Every campaign invents its own format.
- Reports can't be aggregated across clients or campaigns.
- Custom-fit aliases ("ig", "instagram", "Insta", "IG-Story") fragment the data.
- Six months later nobody remembers what "promo23" means.

This file is the **agency-wide locked convention**. Enforced by `tools/utm_builder.py` validation. Custom formats are rejected.

---

## The Five Parameters

```
?utm_source=<source>&utm_medium=<medium>&utm_campaign=<campaign>&utm_content=<content>&utm_term=<term>
```

| Parameter | Purpose | Required |
|---|---|---|
| `utm_source` | Where the click originated (platform identifier) | Yes |
| `utm_medium` | Format / channel-type identifier | Yes |
| `utm_campaign` | Campaign identifier (clusters pieces together) | Yes |
| `utm_content` | Specific piece identifier (ties back to pipeline) | Yes (BrandFlow standard) |
| `utm_term` | Targeting term (paid only — audience slice / keyword) | Conditional (paid only) |

---

## utm_source — Allowed Values

Platform identifiers. Use lowercase, hyphenated, no spaces.

| Value | Use for |
|---|---|
| `instagram` | Any IG surface (feed, story, reels, bio) |
| `linkedin` | Any LinkedIn surface (feed, article, DM, profile) |
| `tiktok` | Any TikTok surface |
| `twitter` | Any X / Twitter surface (we keep `twitter` for cross-tool consistency; some teams use `x`) |
| `youtube` | Any YouTube surface (description, end-screen, card) |
| `pinterest` | Pinterest |
| `facebook` | Facebook (organic + Meta Ads sometimes — see medium for distinction) |
| `whatsapp` | WhatsApp DMs / Status |
| `telegram` | Telegram channels / DMs |
| `email` | Any email send |
| `newsletter` | Specific newsletter surface (if distinguished from transactional email) |
| `direct` | Manual direct share (not platform-attributable) |
| `qr` | QR code (offline / event surfaces) |
| `referral-<partner-slug>` | Specific referral partner with slug |
| `podcast-<podcast-slug>` | Specific podcast appearance |

Add new sources only via CMO approval; update this list when added.

---

## utm_medium — Allowed Values

Format / channel-type. Distinguishes "what kind of placement" within a source.

| Value | Use for |
|---|---|
| `organic-post` | Standard organic feed/wall post |
| `organic-reel` | Reel / Short-form video (organic) |
| `organic-story` | Story / Status-format |
| `organic-thread` | Multi-tweet / multi-post thread |
| `bio-link` | Link in bio / Linktree-equivalent |
| `dm` | Sent via DM |
| `paid-feed` | Paid feed placement (Meta/LinkedIn/X ads) |
| `paid-story` | Paid story / vertical placement |
| `paid-reel` | Paid Reel / Short-form video ad |
| `paid-search` | SEM (Google Ads, Bing Ads) |
| `paid-display` | Display ad networks |
| `paid-influencer` | Paid influencer placement |
| `email-body` | Link in email body |
| `email-cta` | Primary CTA in email |
| `email-footer` | Footer link in email |
| `referral` | Generic referral (with utm_source = `referral-<partner>`) |
| `event` | Live event / talk / conference |
| `print` | Offline print (with utm_source = `qr`) |

---

## utm_campaign — Format

```
<client-slug>__<campaign-slug>__<YYYY-MM>
```

- `client-slug`: the client's slug (e.g. `acme`, `kopi-x`, `agency-self`).
- `campaign-slug`: short campaign name, lowercase, hyphenated (e.g. `summer-launch`, `q2-webinar-series`).
- `YYYY-MM`: month the campaign goes live.
- Separator: double underscore (`__`).

Examples:

```
acme__summer-launch__2026-05
kopi-x__loyalty-program__2026-06
agency-self__lead-magnet-q2__2026-04
```

Why double underscore: lets you split the campaign string back into the three components programmatically. Single underscore would conflict with hyphens-in-slugs.

For evergreen campaigns: use the **start month** (`YYYY-MM`) — don't keep updating the date.

---

## utm_content — Format

The piece identifier. Format:

```
<piece-id>
```

Where `<piece-id>` is the content-pipeline ID (e.g. `BF-acme-0142`).

This ties the click directly back to the pipeline JSONL row. Per-piece performance attribution is then automatic — the analytics report joins clicks to piece metadata via this field.

For ads with multiple creative variants on the same piece (A/B):

```
<piece-id>__<variant>
```

Examples:

```
BF-acme-0142
BF-acme-0142__hookA
BF-acme-0142__hookB
```

---

## utm_term — Format (Paid Only)

Used only on paid campaigns. Audience-slice or keyword identifier.

For paid social (audience targeting):

```
<audience-slice-slug>
```

Examples:

```
b2b-founders-id
remarketing-7day
lookalike-1pct-customer
```

For paid search (keyword targeting):

```
<keyword-slug>
```

Examples:

```
cold-email-templates-b2b
agency-jakarta
```

Don't use for organic. Empty `utm_term` is fine on organic; the field is conditional.

---

## Format Rules (Hard)

- All lowercase.
- All ASCII (no emojis, no Unicode).
- Hyphens for word separation within a slug.
- Underscores only in the agency-defined separators (`__` in campaign, `__` between piece-id and variant).
- No spaces.
- No special characters: `+`, `&`, `?`, `#`, `=`, `/`, `%`, etc.
- All values URL-encoded by the builder (never manually).
- Maximum 100 chars per parameter (most analytics platforms cap longer values).

`tools/utm_builder.py` validates all of the above and rejects non-compliant input.

---

## Building a UTM URL — Example

Inputs:
- Destination: `https://acme.com/landing-summer`
- Source: `instagram`
- Medium: `organic-post`
- Campaign client: `acme`, campaign-slug: `summer-launch`, month: `2026-05`
- Content (piece-id): `BF-acme-0142`
- Term: (none, organic)

Output:
```
https://acme.com/landing-summer?utm_source=instagram&utm_medium=organic-post&utm_campaign=acme__summer-launch__2026-05&utm_content=BF-acme-0142
```

Use `tools/utm_builder.py` rather than hand-construction. The builder also short-URLs the result if a short-domain is configured.

---

## Convention vs Native Tracking Differences

UTMs work for any analytics platform that accepts query parameters (GA4, Plausible, Fathom, etc.). For platforms with native tracking that bypasses UTMs:

- **Meta Ads Manager**: native click tracking via Meta Pixel; UTMs are still propagated to landing pages and visible in GA4.
- **LinkedIn Ads**: native conversion tracking + UTMs both work.
- **TikTok Ads**: native pixel + UTMs propagate.

Always set UTMs even when native tracking exists. Native tracking dies if the pixel is blocked / cookie-rejected; UTMs remain in the URL.

---

## Handling Special Cases

### Client share (link the client themselves shares)

If a client manually shares a piece's link, treat as `utm_source=direct&utm_medium=referral`. Don't try to attribute it to the campaign source — the client may share to anywhere.

### Cross-channel campaign with one landing page

Each channel gets its own UTM combo on the same destination URL. Reports then split traffic by source/medium even though landing page is shared.

### Long-lived evergreen content

Rebuild UTMs periodically if you want time-binning, OR use a stable "evergreen" campaign string:

```
<client>__evergreen-<topic>__YYYY-MM (start)
```

The month-suffix locks at start; don't update.

### Influencer campaign

```
utm_source=referral-<influencer-slug>
utm_medium=paid-influencer  (paid)  OR  organic  (gifted)
utm_campaign=<client>__<campaign>__YYYY-MM
utm_content=BF-<client>-<piece-id>
utm_term=<placement-context>  (e.g. story / reel / post)
```

### QR code (offline → online)

```
utm_source=qr
utm_medium=event  OR  print
utm_campaign=<client>__<campaign>__YYYY-MM
utm_content=<placement-id>  (e.g. booth-front / poster-elevator-3)
```

---

## Reporting Implications

The convention enables joinable, sliceable reports:

- **By source × medium**: which platforms drive most traffic / conversions per client.
- **By campaign**: campaign-level ROI rollup.
- **By piece-id**: which specific pieces deliver the campaign's KPI (joined back to pipeline metadata).
- **By month**: year-over-year and quarter-over-quarter comparison.
- **By client**: normalized cross-client benchmarking (anonymized).

Without convention, none of this works without per-campaign data wrangling.

---

## Anti-Patterns

- **Custom format per campaign.** Defeats the point of the convention.
- **Forgetting `utm_content`.** Loses the piece-level attribution.
- **Mixing case** ("Instagram" / "instagram" / "INSTAGRAM"). GA4 treats them as different. Always lowercase.
- **Spaces or special characters not encoded.** Breaks links in some clients.
- **Same `utm_campaign` for unrelated efforts.** Pollutes the campaign rollup.
- **Free-form `utm_term`.** Use slug discipline; analytics platforms group by exact match.
- **Tracking organic-share clicks under ads attribution.** Distinct sources; don't blur.
- **No UTM at all because "we have native tracking."** Native tracking is supplementary, not replacement.

---

## Reference

- `companies/brandflow/skills/automation/SKILL.md` — Senior Patterns §8 UTM convention enforcement.
- `tools/utm_builder.py` (Update 11) — convention-validating UTM builder.
- `companies/brandflow/skills/analytics/SKILL.md` — analytics consumes UTM-tagged data.
- This convention follows established UTM tracking standards (Google Analytics canonical). Content paraphrased for licensing compliance.
