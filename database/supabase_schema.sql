-- ============================================================
-- Database Schema — Phase 1
-- ============================================================
-- Principles:
--   1. workflow_state is server-owned — never client-writable
--   2. RLS enforces idea isolation at DB layer
--   3. event_log is append-only — no updates, no deletes
--   4. Locked/archived ideas reject all field modifications
--   5. Five tables only — no Phase 2 tables
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- ENUMS
-- ============================================================

CREATE TYPE workflow_state AS ENUM (
  'IDLE',
  'INPUT_RECEIVED',
  'COMPLETENESS_CHECK',
  'DOMAIN_ANALYSIS',
  'GATE_EVALUATION',
  'REPORT_GENERATED',
  'ARCHIVED',
  'ERROR'
);

CREATE TYPE gate_outcome AS ENUM (
  'PASS',
  'WARN',
  'BLOCK'
);

CREATE TYPE event_type AS ENUM (
  'STATE_TRANSITION',
  'AI_CALL_START',
  'AI_CALL_SUCCESS',
  'AI_CALL_SCHEMA_FAILURE',
  'AI_CALL_FINAL_FAILURE',
  'GATE_DECISION',
  'COMPLETENESS_CHECK',
  'USER_ACTION',
  'ERROR'
);

CREATE TYPE analysis_domain AS ENUM (
  'IOT_ELECTRONICS'
);

-- ============================================================
-- TABLE 1: ideas
-- ============================================================

CREATE TABLE ideas (
  id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id                 UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  workflow_state          workflow_state NOT NULL DEFAULT 'IDLE',
  state_updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),

  domain                  analysis_domain NOT NULL DEFAULT 'IOT_ELECTRONICS',

  field_idea              TEXT,
  field_problem           TEXT,
  field_solution          TEXT,
  field_beneficiary       TEXT,
  field_domain_context    TEXT,
  input_hash              TEXT,
  input_locked_at         TIMESTAMPTZ,

  completeness_score      INTEGER CHECK (completeness_score BETWEEN 0 AND 100),
  completeness_warnings   JSONB,
  completeness_checked_at TIMESTAMPTZ,

  ai_model_version        TEXT,
  prompt_version          TEXT,
  ai_output_schema_version TEXT,
  ai_output               JSONB,
  ai_raw_response         TEXT,
  ai_called_at            TIMESTAMPTZ,

  gate_outcome            gate_outcome,
  gate_rule_version       TEXT,
  gate_rationale_ids      TEXT[],
  gate_evaluated_at       TIMESTAMPTZ,

  report_text             TEXT,
  report_generated_at     TIMESTAMPTZ,

  -- Draft persistence — pre-submission only, never triggers FSM
  -- Cleared when idea transitions to INPUT_RECEIVED
  draft_fields            JSONB,
  draft_updated_at        TIMESTAMPTZ,

  is_locked               BOOLEAN NOT NULL DEFAULT false,
  archived_at             TIMESTAMPTZ,

  last_error_code         TEXT,
  last_error_at           TIMESTAMPTZ,
  last_error_context      JSONB,

  created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_ideas_user_id    ON ideas(user_id);
CREATE INDEX idx_ideas_state      ON ideas(workflow_state);
CREATE INDEX idx_ideas_created_at ON ideas(created_at DESC);

-- ============================================================
-- TABLE 2: event_log
-- Append-only. No updates. No deletes. Ever.
-- ============================================================

CREATE TABLE event_log (
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  idea_id               UUID REFERENCES ideas(id) ON DELETE RESTRICT,
  user_id               UUID REFERENCES auth.users(id) ON DELETE RESTRICT,

  event_type            event_type NOT NULL,
  workflow_state        workflow_state NOT NULL,

  ai_model_version      TEXT,
  prompt_version        TEXT,
  input_hash            TEXT,
  output_schema_version TEXT,

  gate_outcome          gate_outcome,
  gate_rule_version     TEXT,
  gate_input_payload    JSONB,
  rationale_ids         TEXT[],

  duration_ms           INTEGER,
  error_code            TEXT,
  error_context         JSONB,
  context               JSONB,

  created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE RULE event_log_no_update AS ON UPDATE TO event_log DO INSTEAD NOTHING;
CREATE RULE event_log_no_delete AS ON DELETE TO event_log DO INSTEAD NOTHING;

CREATE INDEX idx_event_log_idea_id    ON event_log(idea_id);
CREATE INDEX idx_event_log_user_id    ON event_log(user_id);
CREATE INDEX idx_event_log_type       ON event_log(event_type);
CREATE INDEX idx_event_log_created_at ON event_log(created_at DESC);

-- ============================================================
-- TABLE 3: prompt_versions
-- ============================================================

CREATE TABLE prompt_versions (
  id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  version_string              TEXT NOT NULL UNIQUE,
  domain                      analysis_domain NOT NULL,
  model_version               TEXT NOT NULL,

  benchmark_schema_compliance NUMERIC(5,2),
  benchmark_gate_agreement    NUMERIC(5,2),
  benchmark_test_count        INTEGER,
  benchmark_run_at            TIMESTAMPTZ,
  benchmark_approved_by       TEXT,

  is_active                   BOOLEAN NOT NULL DEFAULT false,
  deployed_at                 TIMESTAMPTZ,
  deprecated_at               TIMESTAMPTZ,

  system_prompt_text          TEXT NOT NULL,
  output_schema               JSONB NOT NULL,

  created_at                  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX idx_prompt_versions_one_active
  ON prompt_versions(domain)
  WHERE is_active = true;

-- ============================================================
-- TABLE 4: gate_rule_versions
-- ============================================================

CREATE TABLE gate_rule_versions (
  id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  version_string TEXT NOT NULL UNIQUE,
  domain         analysis_domain NOT NULL,

  rules_yaml     TEXT NOT NULL,
  rules_hash     TEXT NOT NULL,

  reviewed_by    TEXT,
  approved_at    TIMESTAMPTZ,

  is_active      BOOLEAN NOT NULL DEFAULT false,
  deployed_at    TIMESTAMPTZ,
  deprecated_at  TIMESTAMPTZ,

  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX idx_gate_rules_one_active
  ON gate_rule_versions(domain)
  WHERE is_active = true;

-- ============================================================
-- TABLE 5: benchmark_runs
-- Governance/evidence only. Not part of user workflow runtime.
-- ============================================================

CREATE TABLE benchmark_runs (
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  prompt_version        TEXT NOT NULL,
  gate_rule_version     TEXT NOT NULL,
  model_version         TEXT NOT NULL,
  domain                analysis_domain NOT NULL,

  total_cases           INTEGER NOT NULL,
  schema_pass_count     INTEGER NOT NULL,
  gate_agree_count      INTEGER NOT NULL,
  schema_compliance_pct NUMERIC(5,2) NOT NULL,
  gate_agreement_pct    NUMERIC(5,2) NOT NULL,

  schema_threshold      NUMERIC(5,2) NOT NULL DEFAULT 90.00,
  gate_threshold        NUMERIC(5,2) NOT NULL DEFAULT 85.00,

  passed                BOOLEAN NOT NULL,
  reviewed_by           TEXT,
  notes                 TEXT,

  run_at                TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================

ALTER TABLE ideas              ENABLE ROW LEVEL SECURITY;
ALTER TABLE event_log          ENABLE ROW LEVEL SECURITY;
ALTER TABLE prompt_versions    ENABLE ROW LEVEL SECURITY;
ALTER TABLE gate_rule_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE benchmark_runs     ENABLE ROW LEVEL SECURITY;

-- -------------------------------------------------------
-- ideas: granular policies
-- Client may SELECT and INSERT their own ideas.
-- Client may NOT UPDATE directly — all writes go through
-- server-side service_role endpoints only.
-- -------------------------------------------------------

-- Client can read their own ideas (via view only — see below)
CREATE POLICY ideas_select ON ideas
  FOR SELECT
  USING (auth.uid() = user_id);

-- Client can insert new ideas (only user_id = their own)
CREATE POLICY ideas_insert ON ideas
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Client cannot UPDATE ideas table directly — ever.
-- All state transitions and field writes go through service_role.
-- No UPDATE policy = UPDATE is denied for authenticated role.

-- Client cannot DELETE ideas.
-- No DELETE policy = DELETE is denied for authenticated role.

-- -------------------------------------------------------
-- event_log: read own events only — no client inserts
-- -------------------------------------------------------
CREATE POLICY event_log_read_own ON event_log
  FOR SELECT
  USING (auth.uid() = user_id);

-- -------------------------------------------------------
-- prompt_versions: read only for authenticated users
-- -------------------------------------------------------
CREATE POLICY prompt_versions_read ON prompt_versions
  FOR SELECT
  USING (auth.role() = 'authenticated');

-- -------------------------------------------------------
-- gate_rule_versions: read only for authenticated users
-- -------------------------------------------------------
CREATE POLICY gate_rules_read ON gate_rule_versions
  FOR SELECT
  USING (auth.role() = 'authenticated');

-- -------------------------------------------------------
-- benchmark_runs: no client access — governance only
-- -------------------------------------------------------
CREATE POLICY benchmark_no_client_access ON benchmark_runs
  FOR ALL
  USING (false);

-- ============================================================
-- TRIGGERS
-- ============================================================

CREATE OR REPLACE FUNCTION fn_update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ideas_updated_at
  BEFORE UPDATE ON ideas
  FOR EACH ROW
  EXECUTE FUNCTION fn_update_updated_at();

-- Prevent workflow_state changes from any role except service_role.
-- All FSM transitions must go through server-side endpoints using service_role key.
-- authenticated role (client) cannot change workflow_state under any circumstance.
CREATE OR REPLACE FUNCTION fn_block_client_state_change()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.workflow_state IS DISTINCT FROM OLD.workflow_state THEN
    IF current_setting('role') != 'service_role' AND
       current_setting('request.jwt.claims', true)::jsonb->>'role' != 'service_role'
    THEN
      RAISE EXCEPTION 'state_change_forbidden: workflow_state can only be changed by server-side service_role';
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trg_ideas_state_protection
  BEFORE UPDATE ON ideas
  FOR EACH ROW
  EXECUTE FUNCTION fn_block_client_state_change();

-- Prevent gate fields from being changed by client
CREATE OR REPLACE FUNCTION fn_block_client_gate_write()
RETURNS TRIGGER AS $$
BEGIN
  IF (NEW.gate_outcome        IS DISTINCT FROM OLD.gate_outcome OR
      NEW.gate_rule_version   IS DISTINCT FROM OLD.gate_rule_version OR
      NEW.gate_rationale_ids  IS DISTINCT FROM OLD.gate_rationale_ids OR
      NEW.ai_output           IS DISTINCT FROM OLD.ai_output OR
      NEW.ai_raw_response     IS DISTINCT FROM OLD.ai_raw_response OR
      NEW.ai_model_version    IS DISTINCT FROM OLD.ai_model_version OR
      NEW.prompt_version      IS DISTINCT FROM OLD.prompt_version OR
      NEW.report_text         IS DISTINCT FROM OLD.report_text)
  THEN
    IF current_setting('role') != 'service_role' AND
       current_setting('request.jwt.claims', true)::jsonb->>'role' != 'service_role'
    THEN
      RAISE EXCEPTION 'server_field_forbidden: AI and gate fields can only be written by server-side service_role';
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER trg_ideas_server_fields
  BEFORE UPDATE ON ideas
  FOR EACH ROW
  EXECUTE FUNCTION fn_block_client_gate_write();

CREATE OR REPLACE FUNCTION fn_block_locked_idea()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.is_locked = true THEN
    RAISE EXCEPTION 'idea_locked: This idea is archived and cannot be modified';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ideas_lock
  BEFORE UPDATE ON ideas
  FOR EACH ROW
  EXECUTE FUNCTION fn_block_locked_idea();

CREATE OR REPLACE FUNCTION fn_block_input_modification()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.input_locked_at IS NOT NULL THEN
    IF NEW.field_idea           IS DISTINCT FROM OLD.field_idea OR
       NEW.field_problem        IS DISTINCT FROM OLD.field_problem OR
       NEW.field_solution       IS DISTINCT FROM OLD.field_solution OR
       NEW.field_beneficiary    IS DISTINCT FROM OLD.field_beneficiary OR
       NEW.field_domain_context IS DISTINCT FROM OLD.field_domain_context
    THEN
      RAISE EXCEPTION 'input_locked: Input fields cannot be changed after analysis begins';
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ideas_input_lock
  BEFORE UPDATE ON ideas
  FOR EACH ROW
  EXECUTE FUNCTION fn_block_input_modification();

CREATE OR REPLACE FUNCTION fn_block_gate_modification()
RETURNS TRIGGER AS $$
BEGIN
  IF OLD.gate_outcome IS NOT NULL AND
     NEW.gate_outcome IS DISTINCT FROM OLD.gate_outcome THEN
    RAISE EXCEPTION 'gate_locked: Gate outcome cannot be changed after evaluation';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_ideas_gate_lock
  BEFORE UPDATE ON ideas
  FOR EACH ROW
  EXECUTE FUNCTION fn_block_gate_modification();

-- ============================================================
-- CLIENT VIEW
-- This is the ONLY read path for client-facing queries.
-- Clients must query ideas_client_view — never the ideas table directly.
-- Hides: ai_raw_response, all internal audit fields, server-only columns.
-- RLS on underlying ideas table still applies through this view.
-- ============================================================

CREATE VIEW ideas_client_view WITH (security_invoker = true) AS
SELECT
  id,
  user_id,
  workflow_state,
  state_updated_at,
  domain,
  field_idea,
  field_problem,
  field_solution,
  field_beneficiary,
  field_domain_context,
  completeness_score,
  completeness_warnings,
  gate_outcome,
  gate_rationale_ids,
  report_text,
  report_generated_at,
  is_locked,
  archived_at,
  last_error_code,
  created_at
FROM ideas;

-- ============================================================
-- COMMENTS
-- ============================================================

COMMENT ON TABLE ideas IS
  'Core idea records. workflow_state is server-owned — never written by client.';
COMMENT ON TABLE event_log IS
  'Append-only audit log. No updates or deletes permitted.';
COMMENT ON TABLE prompt_versions IS
  'Registry of prompt versions. Enables AI call reproducibility and rollback.';
COMMENT ON TABLE gate_rule_versions IS
  'Registry of gate rule versions. Enables gate decision replay and audit.';
COMMENT ON TABLE benchmark_runs IS
  'Governance/evidence only. Not part of user workflow runtime.';
COMMENT ON COLUMN ideas.workflow_state IS
  'FSM state. Written by server only. Client reads via ideas_client_view.';
COMMENT ON COLUMN ideas.is_locked IS
  'True when ARCHIVED. All modifications blocked by trigger.';
COMMENT ON COLUMN ideas.ai_raw_response IS
  'Raw AI response preserved for audit even when schema validation fails.';
COMMENT ON COLUMN event_log.gate_input_payload IS
  'Full JSON passed to gate rule engine — enables gate decision replay.';
