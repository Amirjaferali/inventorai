# T1-C′ Automated Study Dry Run 001 — mechanics evidence

**EVIDENCE ONLY.** This record is not execution authority. It alters no corpus, no product
behaviour and no governance state; it authorizes no human activity and claims no T1-C′
completion, usability, novice/expert performance, differentiation, trust, decision impact,
human value, commercial readiness or release readiness.

**HUMAN EXECUTION REMAINS NOT AUTHORIZED.**

## 1. Identity

- Repository: `Amirjaferali/inventorai`, branch `feature/atomic-json-session-persistence`.
- Run HEAD: `d3b76eff5859c4c1ab7890059e5629fdeefab4b4` (tree `22d110a2abc356064bab85963d48d1670735625d`);
  working tree clean.
- Corpus: `docs/validation/T1C_STANDARDIZED_STUDY_CORPUS_V1.md`, file SHA-256
  `25b35b2abec219dcc3132b650a5174904c4fbc2dab4620fc06d5b7bdfbb6b89b`, verified before use.
- Block SHA-256 verified before use: T1C-EE-01
  `2a01c8e6ddafca5a25cbf2f57e92c23db57e06411a84af7c78759ac07d817d15`; T1C-ME-01
  `c91a3487d509e2eceee659659dbdf4af463c372600ae7e8743e6bed49fcbc26b`.
- Executed 2026-09-23 22:11:26–22:11:44 UTC; Chromium 141.0.7390.37 (Playwright, headless).
- **Release-candidate boundary:** this is mechanics evidence at the HEAD above only. It is NOT the
  T1-C′ release-candidate rehearsal; the dry run must be repeated against the exact pinned actual
  release-candidate tip before any authorized human execution. The HEAD above is not a release
  candidate.

## 2. Seed construction rule applied (Owner decision)

For each case and language: take the intended language's `idea`, `context` and `known constraint`
lines from the frozen participant-text block, remove only the field labels
(`EN — idea: ` / `EN — context: ` / `EN — known constraint: ` or the `AR — …: ` equivalents),
preserve every remaining character, and join `idea + " " + context + " " + constraint` with single
ASCII spaces. No paraphrase, normalization, keyword addition, re-translation or spacing change. The
seed text is not reproduced here; each seed is identified by byte length and SHA-256.

| Case / language | Seed UTF-8 bytes | Seed SHA-256 |
|---|---|---|
| T1C-EE-01 / EN | 790 | `cc29037fa8379b6ae80880135482c59e9e4a5823da3c81f40b71fa4f2a525a25` |
| T1C-EE-01 / AR | 1126 | `6dc1f3c15b9065bb67ae9bf9193641346e364391d0ce9d35dabb92006a9a0fec` |
| T1C-ME-01 / EN | 745 | `ef848fd0e44611afb287db78c44da2f8e6f23420739936de57597a183659a18a` |
| T1C-ME-01 / AR | 1049 | `915f14181851e20cd037e8378bad5f06820ddafb4e418b20a955083234528952` |

## 3. Method

- Ephemeral runner in the session scratchpad; not committed; not a test; reads the corpus at the run
  HEAD and verifies the hashes above before use.
- Existing browser/E2E surface only: Playwright Chromium, the repository's single-thread werkzeug
  live-server pattern, real form submission, real CSRF, real JavaScript and `localStorage`.
  Routes: `/` → `/ui-language` (real switch button) → `/start` (real domain-choice radios and
  confirmation checkbox, never bypassed) → `/session/<sid>` → `/session/<sid>/deliverable` →
  `/session/<sid>/deliverable.pdf` (real form token, shared cookie jar) → `/session/<sid>/resume`
  (real button). No ILT-only or benchmark-only route. No account, email or export.
- Isolation: one fresh throwaway SQLite database and one fresh browser context per case; the
  database directory was deleted after each case (verified); browser contexts closed.
- Progression boundary: eight fixed synthetic mechanics-only answers per language, identical for both
  cases, written before any run and never adjusted to product outcomes; action `answered` each time;
  at most 8 submissions; the run was not driven toward the completion marker or eligibility.
- Cold reload: after the live phase the server was stopped, the in-process session store cleared and
  store handles closed, and a fresh server started against the same database; session and
  deliverable were then requested through normal routes, and writable resume was attempted through
  the real resume button.
- Process note (truthful): a first runner attempt failed on three cases because the runner's
  domain-choice locator matched the hidden `domain_choice` carrier on the confirmation page
  instead of the visible radio; that was a runner defect, not a product defect. The locator was
  corrected and the complete four-case run below was executed afresh. Seeds and answers were not
  changed. Snapshots of the aborted attempt were discarded.

## 4. Four-case results

| | EE / EN | EE / AR | ME / EN | ME / AR |
|---|---|---|---|---|
| UI language (`<html lang>`) | en | ar (dir rtl) | en | ar (dir rtl) |
| Classifier on seed | `SINGLE` → electronics_electrical | `NONE` | `NONE` | `NONE` |
| Admission path observed | confirm only (electronics_electrical) | choice [electronics_electrical, mechanical] → confirm electronics_electrical | choice [electronics_electrical, mechanical] → confirm mechanical | choice [electronics_electrical, mechanical] → confirm mechanical |
| Persisted domain / path | electronics_electrical / N | electronics_electrical / N | mechanical / N | mechanical / N |
| First question | "Explain in everyday words how you imagine the system would notice the problem and respond." (en, ltr) | «اشرح بكلمات يومية بسيطة كيف تتخيل أن النظام سيلاحظ المشكلة وكيف سيستجيب لها.» (ar, rtl) | "Describe the physical steps your mechanism takes to achieve its function." (en, ltr) | «صِف الخطوات المادية التي تقوم بها آليتك لتحقيق وظيفتها.» (ar, rtl) |
| Answer submissions / HTTP | 8 / all 302 | 8 / all 302 | 8 / all 302 | 8 / all 302 |
| Progression observed | MECHANISM_COMPLETENESS OPEN → PARTIAL, stayed PARTIAL | same | same | same |
| Final gap states | MC PARTIAL | MC PARTIAL | MC PARTIAL | MC PARTIAL |
| Maturity level | 1 | 1 | 1 | 1 |
| Completion marker reached | NO | NO | NO | NO |
| Final deliverable (live) | 200, `lang=en`, "Assessment Snapshot — In Progress" | 200, `lang=ar dir=rtl`, in-progress snapshot | 200, `lang=en`, in-progress snapshot | 200, `lang=ar dir=rtl`, in-progress snapshot |
| `deliverable_eligible` | false | false | false | false |
| Open gaps at end | MC PARTIAL | MC PARTIAL | MC PARTIAL | MC PARTIAL |
| Deliverable text blocks (AR-only / EN-only / mixed) | 0 / 100 / 0 | 44 / 23 / 31 | 0 / 100 / 0 | 44 / 23 / 31 |
| Live deliverable snapshot SHA-256 | `e0c594e5…7bccc` | `21b2ad5d…8ae01` | `134fb994…daa4ba` | `399881b7…645eb` |
| PDF | 200, application/pdf, 30985 B, `%PDF-` | 200, application/pdf, 50289 B, `%PDF-` | 200, application/pdf, 30935 B, `%PDF-` | 200, application/pdf, 50470 B, `%PDF-` |
| Cold reload: session | 200; read-only (no answer form); resume button present | same | same | same |
| Cold reload: deliverable | 200; in-progress snapshot; read-only reconstruction notice | same (Arabic notice) | same | same (Arabic notice) |
| Writable resume | POST 302; answer form present; domain restored | same | same | same |
| Server errors / exceptions | none | none | none | none |
| Throwaway DB deleted | yes | yes | yes | yes |

Full snapshot hashes: EE/EN live `e0c594e53444f23b7d8013a35efedba618bc46c41a4d1b5f3f3c8f2987f7bccc`,
cold `ea21cf011d90fcfa5be7a2f94ecdaded8a34beaacd04a611ff430c04a93832f5`; EE/AR live
`21b2ad5d78d868b86d369b9a56252591f0a480a7d861348c811f00ff3d08ae01`, cold
`7181fdd061b487c1a0662d2c2bb7598df35a000ea253fdaecee9cdbf109711ca`; ME/EN live
`134fb9949b69a22319d75992cbdbebef5586adb74dee0e228a6c9c20bbdaa4ba`, cold
`5522bd01f05eb2f683f9e6e14ab19177865329cc03d52fe0729ce9e83300dc3e`; ME/AR live
`399881b7fdc180c586c51abad94f59e87ac58ad9ef1fb17c3fb0582b69b645eb`, cold
`5bcf4b9012ecffa96453d5fa9696977d3df189807d46006acff895a0d3f2d179`. Live and cold snapshots differ
only by the read-only reconstruction notice and the generation timestamp; the assessment content is
identical. Snapshot files were retained only in the ephemeral run directory.

## 5. Per-case mechanics classification

| Case | Classification |
|---|---|
| T1C-EE-01 / EN | **DRY-RUN MECHANICS PASS** |
| T1C-EE-01 / AR | **DRY-RUN MECHANICS PASS** |
| T1C-ME-01 / EN | **DRY-RUN MECHANICS PASS** |
| T1C-ME-01 / AR | **DRY-RUN MECHANICS PASS** |

Classification rests only on browser admission, POST/progression mechanics, durable cold reload,
writable resume, final snapshot rendering and PDF generation. It does not rest on maturity, gap
closure, the completion marker, answer quality or `deliverable_eligible`.

## 6. Descriptive EN/AR and admission observations (not defects, not requirements)

1. Admission paths differ: EE/EN resolves directly and needs confirmation only; EE/AR, ME/EN and
   ME/AR resolve `NONE` and take the governed domain-choice → confirmation path. The English cases
   therefore have different admission conditions and must not be compared as if identical.
2. Arabic sessions serve Arabic questions with `lang="ar" dir="rtl"`, Arabic chrome, an Arabic
   read-only reconstruction notice and an Arabic exhausted-questions prompt.
3. The Arabic deliverable is mixed-language by accepted rule: generated substantive content stays
   English (44 Arabic-only / 23 English-only / 31 mixed text blocks in both Arabic cases). The
   English deliverable is English throughout.
4. With the fixed generic answers, all four journeys stayed at MECHANISM_COMPLETENESS PARTIAL,
   maturity 1, in-progress snapshot; after eight submissions the product served its
   exhausted-questions prompt naming the honest exits. No EN/AR progression divergence appeared
   in this run (identical gap trajectories); this is not evidence against the recorded
   divergence in `DEFERRED_OBLIGATIONS_REGISTER.md` row "EN↔AR SUBSTANTIVE-ASSESSMENT OUTCOME
   DIVERGENCE", which concerns substantive answers.
5. The cold-loaded session is read-only until the real resume button is used; resume restored the
   confirmed domain and a writable answer form in every case.

## 7. Overall result

**DRY RUN 001: ALL FOUR CASES DRY-RUN MECHANICS PASS at HEAD `d3b76eff…`.** No material product
defect was found. Nothing here advances T1-C′, Stage 11 human execution, consent/custody
readiness or release status; the mechanics dry run must be repeated on the exact pinned
release-candidate tip before any authorized human round.
