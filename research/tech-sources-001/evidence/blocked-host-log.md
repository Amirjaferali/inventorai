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
