# GRC Tool Integration -> Evidence Collection Implementation Flow

This document converts your requirement into an implementation-ready flow for FastAPI/service-layer logic.

It is based on your payload contract and table structures, and it aligns with model names in `models.py` (for reference only): `Organizations`, `Tools`, `ToolIntegrations`, `ToolEvidence`, `EvidenceMasters`, `Evidence`, `EvidenceCollection`, `EvidenceMappeds`, `ControlEvidenceMaster`.


---

## 1) Input Contract

### Headers

- `domain_name`: example `nihar.sq1.security`

### Request body

```json
{
  "user_id": "019d00d4-4c50-7044-8d4a-ce71851c4b7a",
  "tool_id": "019d00d3-ec05-73de-86be-72a46a919871",
  "configuration_data": {
    "provider_key": "aws",
    "role_arn": ""
  }
}
```

---

## 2) High-Level Sequence

1. Resolve `organization_id` from `organizations.domain_name`.
2. Validate `tool_id` in `tools` table and identify tool.
3. Upsert integration config into `tool_integrations`.
4. Read tool-evidence mappings from `tool_evidence` for this `tool_id`.
5. For each mapped evidence master:
   - Collect data from tool/internal API endpoint.
   - Upsert row in `evidence` (`organization_id` + `tool_evidence_id` unique at app level).
   - Insert one or more `evidence_collection` rows.
   - Map generated `evidence.id` to controls via `evidence_mappeds` using `control_evidence_master`.

All write operations should run inside a DB transaction per request, except long-running API pulls which can be queued and then persisted in a follow-up transactional step.

---

## 3) Step-by-Step Data Flow

## Step 1: Resolve Organization from header

Query:

```sql
SELECT id
FROM organizations
WHERE domain_name = :domain_name
LIMIT 1;
```

Output:

- `organization_id` = primary key from `organizations.id`

If not found: return `404` (`organization not found for domain_name`).

---

## Step 2: Validate tool and build normalized working payload

Query:

```sql
SELECT id, name
FROM tools
WHERE id = :tool_id
LIMIT 1;
```

If not found: return `400/404` (`invalid tool_id`).

Normalized payload for internal processing:

```json
{
  "org_id": "<organization_id_from_step_1>",
  "user_id": "<request.user_id>",
  "tool_id": "<request.tool_id>",
  "configuration_data": { "...": "..." }
}
```

---

## Step 3: Save config into `tool_integrations`

Required values:

- `user_id` from request
- `organization_id` from Step 1
- `tool_id` from request
- `configuration_data` from request
- `is_active = true`

Required uniqueness rule:

- Pair (`organization_id`, `tool_id`) must always be unique in `tool_integrations`.

Create-only behavior (as requested):

- If (`organization_id`, `tool_id`) already exists, **do not update** existing row.
- Return message: **`integration already exists`**.

Pseudo SQL:

```sql
-- check existence first
SELECT id
FROM tool_integrations
WHERE organization_id = :organization_id
  AND tool_id = :tool_id;

-- if found: return without update
-- message: 'integration already exists'

-- if not found: insert
INSERT INTO tool_integrations (
  id, user_id, organization_id, tool_id, configuration_data, is_active, created_at, updated_at
)
VALUES (
  :uuid, :user_id, :organization_id, :tool_id, :configuration_data, true, NOW(), NOW()
);
```

---

## Step 4: Resolve evidence definitions for this tool

Fetch tool-evidence mappings:

```sql
SELECT te.id AS tool_evidence_id,
       te.tool_id,
       te.evidence_master_id,
       te.api_endpoint,
       em.name AS evidence_name,
       em.code AS evidence_master_code,
       em.required_fields
FROM tool_evidence te
JOIN evidence_masters em ON em.id = te.evidence_master_id
WHERE te.tool_id = :tool_id;
```

If no rows: return success with message `configuration stored; no evidence mapping found for tool`.

Required uniqueness rule:

- Pair (`tool_id`, `evidence_master_id`) must always be unique in `tool_evidence`.

---

## Step 5: Collect evidence per `tool_evidence` mapping

For each row from Step 4:

1. Use tool adapter (based on `tools.name` and/or `configuration_data.provider_key`) to call:
   - `te.api_endpoint` if present, else default endpoint map in code.
2. Normalize result to a serializable payload.
3. Persist into `evidence` + `evidence_collection`.

### 5A) Upsert into `evidence`

Rules from requirement:

- `organization_id` = resolved organization id
- `title` = `evidence_masters.name`
- `tool_evidence_id` = `tool_evidence.id`
- `code` = generated sequence format:
  - `E-0001` ... `E-9999`
  - after 9999: `E-10000`, `E-10001`, ...

App-level uniqueness requirement:

- Pair (`organization_id`, `tool_evidence_id`) must be unique (enforce in service logic; add DB unique index later if possible).

Pseudo logic:

- If evidence exists for (`organization_id`, `tool_evidence_id`): update metadata/status.
- Else create new evidence row with next code.

Code generation approach:

```text
1) Read highest numeric suffix from evidence.code where code starts with 'E-'
2) next_number = max + 1 (default 1)
3) if next_number <= 9999 => code = 'E-' + zero_pad_4(next_number)
4) else code = 'E-' + str(next_number)
```

Use row/table lock or DB sequence to avoid duplicate codes under concurrency.

### 5B) Insert into `evidence_collection`

Requirement:

- Multiple `evidence_collection` rows can belong to one `evidence.id`.

Insert at least one row per collection attempt:

- `organization_id`, `user_id`, `tool_id` (from incoming request)
- `evidence_id` (from 5A)
- `status` (`success` / `failed`)
- `detail` (raw/normalized API evidence payload)
- `error_message` when failed
- `started_at`, `completed_at`

---

## Step 6: Map evidence to controls through `control_evidence_master`

Fetch controls for each `evidence_master_id`:

```sql
SELECT control_id
FROM control_evidence_master
WHERE evidence_master_id = :evidence_master_id;
```

For each `control_id`, create mapping row in `evidence_mappeds`:

- `evidence_id` = created/upserted evidence id
- `evidenceable_type` = `App\\Models\\Control`
- `evidenceable_id` = `control_id`
- `mapped_by` = request `user_id`

Idempotency recommendation:

- Before insert, check existence by (`evidence_id`, `evidenceable_type`, `evidenceable_id`).

Pseudo SQL:

```sql
INSERT INTO evidence_mappeds (
  id, evidence_id, evidenceable_type, evidenceable_id, mapped_by, created_at, updated_at
)
VALUES (
  :uuid, :evidence_id, 'App\\Models\\Control', :control_id, :user_id, NOW(), NOW()
)
-- do nothing if already exists (handled via app check or unique index)
;
```

---

## 4) End-to-End Pseudocode

```text
function configure_tool_and_collect_evidence(headers, body):
    validate body.user_id, body.tool_id, body.configuration_data
    domain_name = headers["domain_name"]

    begin transaction
      org = find organization by domain_name
      if not org: rollback + 404

      tool = find tool by body.tool_id
      if not tool: rollback + 404

      existing_integration = find tool_integrations by (org.id, body.tool_id)
      if existing_integration:
          rollback + return message "integration already exists"

      insert tool_integrations with:
          user_id=body.user_id
          organization_id=org.id
          tool_id=body.tool_id
          configuration_data=body.configuration_data
          is_active=true

      mappings = get tool_evidence + evidence_masters for tool
    commit transaction

    for each mapping in mappings:
        started_at = now
        try:
            collected_payload = collect_from_tool_api(tool, mapping.api_endpoint, body.configuration_data)

            begin transaction
              evidence = upsert evidence by (org.id, mapping.tool_evidence_id)
                title = mapping.evidence_name
                code = generated E-XXXX if new

              insert evidence_collection(success, detail=collected_payload, timestamps...)

              control_ids = get control_evidence_master by mapping.evidence_master_id
              for each control_id:
                  upsert evidence_mappeds(
                     evidence_id=evidence.id,
                     evidenceable_type='App\\Models\\Control',
                     evidenceable_id=control_id,
                     mapped_by=body.user_id
                  )
            commit transaction

        except Exception as ex:
            begin transaction
              evidence = ensure evidence row exists for (org.id, mapping.tool_evidence_id)
              insert evidence_collection(failed, error_message=str(ex), timestamps...)
            commit transaction

    return summary
```

---

## 5) API Response Shape (recommended)

```json
{
  "organization_id": "019d00d4-4b28-73f8-ba85-39bbdd335503",
  "tool_id": "019d00d3-ec05-73de-86be-72a46a919871",
  "tool_name": "aws",
  "integration_saved": true,
  "evidence_processed": 5,
  "evidence_success": 4,
  "evidence_failed": 1,
  "items": [
    {
      "tool_evidence_id": "....",
      "evidence_master_id": "....",
      "evidence_id": "....",
      "status": "success"
    }
  ]
}
```

---

## 6) Validation and Error Handling Checklist

- Missing `domain_name` header -> `400`.
- Unknown `domain_name` -> `404`.
- Unknown `tool_id` -> `404`.
- Existing integration for (`organization_id`, `tool_id`) -> `409` with message `integration already exists`.
- Invalid `configuration_data` required fields per tool -> `422`.
- Tool API auth/permission failure -> save failed `evidence_collection` row with error.
- Do not fail whole request if one evidence mapping fails; process remaining mappings.

---

## 7) Concurrency + Idempotency Notes

- Protect evidence `code` generation with lock/sequence.
- Enforce one active integration config per (`organization_id`, `tool_id`) in app logic.
- Enforce unique mapping per (`tool_id`, `evidence_master_id`) in `tool_evidence` handling.
- Enforce uniqueness for evidence by (`organization_id`, `tool_evidence_id`) in app logic.
- Prevent duplicate control mappings by checking existing `evidence_mappeds`.

---

## 8) Optional DB Constraints to Add Later (recommended)

If migrations are allowed later, add:

1. Unique index on `tool_integrations (organization_id, tool_id)`.
2. Unique index on `tool_evidence (tool_id, evidence_master_id)`.
3. Unique index on `evidence (organization_id, tool_evidence_id)`.
4. Unique index on `evidence_mappeds (evidence_id, evidenceable_type, evidenceable_id)`.

These are not required for this flow document, but they reduce race-condition bugs.

