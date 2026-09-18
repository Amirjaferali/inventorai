# SERIOUS-RELEASE-PRE-RELEASE-TRANCHE-01, Slice A — production container image.
#
# Gate provenance: OD-INFRA-1 (RENDER) / OD-INFRA-2 (FRANKFURT) recorded in
# INFRA-G1-R1; INFRA-G1-R2 owns the serving posture (`gunicorn.conf.py`);
# INFRA-G1-P1 owns the provisioning specification. This file adds ONLY the
# container packaging those records require and changes no application logic.
#
# Purpose: express the governed production runtime as one inspectable artifact —
# the repository-pinned Python, the pinned Python dependencies, and the
# OS-level libraries that Direct Output PDF needs and that `requirements.txt`
# records as "OS packages, not pip packages".
#
# Input contract: the repository working tree; the platform-supplied `PORT`
# (read by `gunicorn.conf.py`, never here).
# Output contract: an image whose default command is the governed single-worker
# Gunicorn start command.
#
# Prohibited (binding): embedding any secret, credential or token; embedding a
# database path or creating a database inside the image; declaring a VOLUME
# (which would invite an ephemeral in-container database); more than one worker
# or thread; preloading the application; invoking Flask's development server.
#
# Why the runtime configuration is NOT here: `INVENTORAI_ENV`,
# `INVENTORAI_SECRET_KEY` and `INVENTORAI_DB_PATH` are supplied by the platform
# environment/secret facility at run time. The image therefore contains no
# environment-specific value, which is also what keeps it provider-neutral: the
# same image runs anywhere a single container with a persistent volume runs.

FROM python:3.11-slim-bookworm

# The repository pins 3.11 in `.python-version`; the base tag above must track
# it. `tests/test_infra_render_production_serving.py` — the existing owner of the
# production serving posture — asserts that agreement, so the two cannot drift
# silently and no second test family is introduced for this image.

# --- OS-level rendering stack (Direct Output PDF) -----------------------------
# WeasyPrint renders through Pango + HarfBuzz + Fontconfig, none of which pip
# can install. `fonts-dejavu-core` provides "DejaVu Sans" — the single family
# `web/templates/pdf_base.html` selects for BOTH the Latin and the Arabic
# deliverable, and the only font in the image that covers Arabic.
# `libharfbuzz-subset0` is included deliberately: WeasyPrint 70 emits
# "HarfBuzz-Subset will be required by future versions" without it, and font
# subsetting is what keeps the rendered deliverable small.
# --no-install-recommends keeps the image to the proven set; the apt lists are
# removed in the same layer so they are not carried in the image.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libharfbuzz0b \
        libharfbuzz-subset0 \
        libfontconfig1 \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencies are copied and installed before the application source so that an
# application-only change does not re-resolve the pinned dependency set.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fail fast and unbuffered: a crash or a log line must reach the platform log
# stream immediately, and `.pyc` files are not wanted in a read-only image layer.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# The governed start command, identical to the one `gunicorn.conf.py` declares.
# Every serving invariant (workers=1, threads=1, preload_app=False, reload=False,
# bind 0.0.0.0:$PORT) lives in that config file and is NOT duplicated here, so
# there is exactly one place where the single-writer posture can be changed.
CMD ["gunicorn", "-c", "gunicorn.conf.py", "web.app:app"]
