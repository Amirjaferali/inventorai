"""Explicit CURRENT-TRUTH contract regions for governance documents.

File: tests/current_truth_contract.py
Purpose: give the document truth-guards one durable, formatting-independent way
to find the part of a document that states CURRENT truth.

Why this exists. Earlier guards tried to tell current truth from history by
recognising particular Markdown shapes — a bullet starting `* **SUPERSEDED`, an
italicised quotation. That failed twice. A document may preserve a superseded
claim as a bullet, a blockquote, a table row, an italic aside or plain prose,
and any shape the guard did not anticipate let a correct-sounding past claim
satisfy a check about the present. Shape is not a contract.

The contract is an explicit delimiter pair:

    <!-- CURRENT-TRUTH:<NAME>:BEGIN -->
    …only statements that are true now…
    <!-- CURRENT-TRUTH:<NAME>:END -->

Guards assert facts ONLY inside the region. History may live anywhere outside
it, in any format, and is free to contradict what the region says — that is the
point of preserving it. The region is malformed, missing or duplicated, and the
guard fails rather than guessing.

This module is a helper, not a test module: it defines no test and is imported
by the guards that do.
"""


def _marker(name, side):
    return "<!-- CURRENT-TRUTH:%s:%s -->" % (name, side)


def region(text, name):
    """Return the CURRENT-TRUTH region `name` from `text`.

    Raises AssertionError — which is what a guard wants — when the region is
    missing, duplicated or malformed, so a document cannot quietly lose its
    contract and leave every downstream assertion vacuously satisfied.
    """
    begin, end = _marker(name, "BEGIN"), _marker(name, "END")
    n_begin, n_end = text.count(begin), text.count(end)

    assert n_begin, "missing CURRENT-TRUTH region %s: no %s" % (name, begin)
    assert n_end, "missing CURRENT-TRUTH region %s: no %s" % (name, end)
    assert n_begin == 1, (
        "duplicate CURRENT-TRUTH region %s: %d BEGIN markers — a second region "
        "makes 'current truth' ambiguous" % (name, n_begin))
    assert n_end == 1, (
        "duplicate CURRENT-TRUTH region %s: %d END markers" % (name, n_end))

    start = text.index(begin) + len(begin)
    stop = text.index(end)
    assert stop > start, (
        "malformed CURRENT-TRUTH region %s: END precedes BEGIN" % name)
    body = text[start:stop]
    assert body.strip(), "empty CURRENT-TRUTH region %s" % name
    return body


def outside(text, name):
    """Everything in `text` that is NOT inside the region — i.e. the history."""
    begin, end = _marker(name, "BEGIN"), _marker(name, "END")
    if begin not in text or end not in text:
        return text
    head = text[:text.index(begin)]
    tail = text[text.index(end) + len(end):]
    return head + "\n" + tail
