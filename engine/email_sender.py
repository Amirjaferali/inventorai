"""P5-1 — Account & Credential Foundation: narrow EmailSender boundary.

A minimal provider boundary so a future production adapter (P5-2+/ops) can drop
in without touching call sites. P5-1 ships ONLY a development sink. The interface
is deliberately tiny (verification / recovery / email-change transactional
messages) — it is NOT output/marketing/notification delivery, has no queue, no
retry worker, and no bulk sending, and it adds NO runtime dependency.

The raw verification token appears ONLY inside a captured/sink message body — it
is never written to the application logs.
"""


class EmailSender:
    """Abstract boundary. Subclasses implement ``send``."""

    def send(self, to, subject, body):  # pragma: no cover - interface
        raise NotImplementedError


class DevMemoryEmailSender(EmailSender):
    """Development / test sink: captures messages in memory (never sends over a
    network, never writes to the application logs). Tests read ``.sent``; manual
    dev may inspect it. A production adapter is a SEPARATE, later concern."""

    def __init__(self):
        self.sent = []

    def send(self, to, subject, body):
        self.sent.append({"to": to, "subject": subject, "body": body})
        return True

    def last_for(self, to):
        for msg in reversed(self.sent):
            if msg["to"] == to:
                return msg
        return None

    def clear(self):
        self.sent.clear()
