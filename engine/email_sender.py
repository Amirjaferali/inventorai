"""P5-1 — Account & Credential Foundation: narrow EmailSender boundary.

A minimal provider boundary so a future production adapter (P5-2+/ops) can drop
in without touching call sites. P5-1 ships ONLY a development sink. The interface
is deliberately tiny (verification / recovery / email-change transactional
messages) — it is NOT output/marketing/notification delivery, has no queue, no
retry worker, and no bulk sending, and it adds NO runtime dependency.

The raw verification token appears ONLY inside a captured/sink message body — it
is never written to the application logs.
"""


class EmailNotConfigured(Exception):
    """Raised when an email is requested and no sender can actually deliver it.

    This exists so a caller FAILS CLOSED AT POINT OF USE rather than reporting a
    delivery that cannot happen. It carries no address, token or message body.
    """


class EmailSender:
    """Abstract boundary. Subclasses implement ``send``.

    ``can_deliver`` states whether this sender is capable of delivering at all.
    It is a capability declaration, not a promise that any individual send will
    succeed: a configured provider can still fail per-message. A future
    production adapter inherits ``True`` and needs no change here.
    """

    can_deliver = True

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


class UnconfiguredEmailSender(EmailSender):
    """The PRODUCTION sender used until a transactional-email provider is
    selected and configured.

    It exists so production can never silently fall back to
    ``DevMemoryEmailSender``: an in-memory sink in production would accept every
    message, report success, and deliver nothing — the application would tell a
    user that verification instructions had been sent when nothing could send
    them. This sender refuses instead, so the caller fails closed and can answer
    truthfully.

    It captures nothing: no address, subject or body is stored or logged here,
    so a refused send leaks no recipient and no token anywhere.
    """

    can_deliver = False

    def send(self, to, subject, body):
        raise EmailNotConfigured(
            "no production email provider is configured")
