# TECH-SOURCES-001 — blocked host log

Append-only. Never bypassed.

| Date | Host | Result | Affected source | Alternative used |
|---|---|---|---|---|
| 2026-10-27 | research.fs.usda.gov | egress proxy CONNECT 403 (connect_rejected) | FPL-GTR-190 Treesearch records; FPL Research Note FPL-0210 (Orosz 1970), Treesearch 5840 | None authorized; SOURCE ACCESS BLOCKED |
| 2026-10-27 | www.fpl.fs.usda.gov | egress proxy CONNECT 403 | FPL-RN-0210 legacy PDF path | None |
| 2026-10-27 | www.standards.doe.gov | connection failed (no response) | DOE-HDBK-1011 official standards page | OSTI record 7112241 (same handbook, OSTI-distributed file) |
| 2026-10-27 | www.fs.usda.gov, www.fs.fed.us, www.govinfo.gov, www.nal.usda.gov, handle.nal.usda.gov, digital.library.unt.edu, archive.org | no response (connection failed) | Alternative hosts for the Wood Handbook / FPL notes | None reachable |
| 2026-10-27 | www.ibiblio.org | egress proxy CONNECT 403 | Kuphaldt, *Lessons in Electric Circuits* Vol. IV (Digital) and its licence appendix | None |
| 2026-10-27 | www.nxp.com | egress proxy CONNECT 403 | NXP / Freescale AN2434, AN2433 | None |
| 2026-10-27 | www.nrc.gov | egress proxy CONNECT 403 | NRC ML063530382 "The Programmable Logic Controller and Its…" (Q-07) | None |
| 2026-10-27 | ntrs.nasa.gov (single download) | 120 s client timeout on a 1.9 MB file; succeeded on retry with a longer timeout | NASA/TM-2009-215751 | Same host, retried once |
| 2026-10-27 (run 5) | www.openbookproject.net, catalog/babel.hathitrust.org, www.biodiversitylibrary.org, core.ac.uk, scholarsarchive.library.oregonstate.edu, docs.lib.purdue.edu, minds.wisconsin.edu, ww1.microchip.com, www.ti.com, www.analog.com, www.st.com, adamswebsearch2.nrc.gov, apps.dtic.mil, discover.dtic.mil, www.fpl.fs.fed.us, zenodo.org, onlinepubs.trb.org, www.cdc.gov, stacks.cdc.gov, www.usda.gov, agris.fao.org | egress proxy policy denial (CONNECT 403 / no connection); not retried | Alternative official / university / publisher hosts for Q-01, Q-05, Q-07 | Reachable only: ntrs.nasa.gov, osti.gov, nvlpubs.nist.gov, nist.gov, energy.gov, github.com |
| 2026-10-27 (run 6) | www.ibiblio.org (after the Owner's allowlist change) | curl error 60 "self-signed certificate in certificate chain": the host now presents its own public chain (InCommon Intermediate CA - OVG2C → emSign Root TLS CA - G1 → emSign Root CA - G1), and no trust store in this environment (proxy bundle, system store, certifi) contains the emSign root. Access had passed at 12:07 UTC the same day (proxy port 42773); fails after the session restart (proxy port 40435). Verification NOT disabled; no root added. | *Lessons in Electric Circuits* Vol. IV ch. 3 "Logic Gates" (DIGI_3.html), Appendix 3 "CC BY License" (DIGI_A3.html), Appendix 1 (DIGI_A1.html) | Q-05 remains UNVERIFIED |
| 2026-10-27 (run 7) | its.ntia.gov | egress proxy CONNECT 403 (connect_rejected) | NTIA Report 84-165 (Frazier, *Handbook of Radio Wave Propagation Loss*) and NTIA TN 89-2 (*Spectrum Management Technical Handbook*) — free-space / far-field definitions for Q-13 | None reachable |
| 2026-10-27 (run 8, ~13:55 UTC) | www.ibiblio.org | re-test: same emSign certificate chain, still untrusted here (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-27 (run 8) | stac.astrogeology.usgs.gov | egress proxy CONNECT 403 | USGS Astrogeology glossary (IFOV / pixel-scale definitions) for Q-15 | None |
| 2026-10-27 (run 9) | www.ibiblio.org | re-test: still no connection (curl 000; certificate trust issue as before) | Q-05 / Q-07 sources | None |
| 2026-10-27 (run 9) | www.faa.gov | no response (curl 000); proxy record not checked | FAA AC 27-1B (tethered-hover thrust statement) for Q-17 | NASA Ames papers (SRC-024, SRC-025) |
| 2026-10-28 (run 11) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-28 (run 11) | transition.fcc.gov, www.fcc.gov | CONNECT 403 (proxy policy), not retried | FCC OET Bulletin 65 (far-field inverse-square statement) for Q-13 | NBS TN 12 and TN 101 Vol. 2 (SRC-037, SRC-038) |
| 2026-10-28 (run 12) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-28 (run 13) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-28 (run 14) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-28 (run 14) | www.publications.usace.army.mil | CONNECT 403 (proxy policy), not retried | USACE EM 1110-2-2610 (2025): rod-side reduced working area; smaller rod-end volume (Q-20 residual) | None reachable on clean rights |
| 2026-10-28 (run 14) | apps.dtic.mil | CONNECT 403 (proxy policy), not retried | DTIC AD1027548 hydraulic handbook (Flow = Velocity × Area) for Q-20 | None reachable on clean rights |
| 2026-10-28 (run 15) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-29 (run 16) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-29 (run 16) | www.fpl.fs.usda.gov | CONNECT 403 (proxy policy), not retried | FPL RP-264 (centre-span deflection measured relative to the supports) for R-03 | research.fs.usda.gov reachable, but its candidate (SRC-049) failed the rights test |
| 2026-10-29 (run 17) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-29 (run 18) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-30 (run 19) | www.ibiblio.org | re-test: still no connection (curl 000) | Q-05 / Q-07 sources | None |
| 2026-10-30 (run 19) | ncc.navfac.navy.mil | CONNECT 403 (proxy policy), not retried | Navy MCM student guide (double-acting cylinder: less retract force, faster retraction) for R-10 | None |
| 2026-10-30 (run 19) | www.nrs.fs.usda.gov | CONNECT 403 (proxy policy), not retried | USDA RP NC-73 (cylinder sizing and flow) for R-10 | None |
| 2026-10-30 (run 19) | nvlpubs.nist.gov (NIST.TN.1951.pdf only) | HTTP 404 for the DOI target; host otherwise reachable | NIST TN 1951 (path loss in industrial sites) for R-08 | None |
