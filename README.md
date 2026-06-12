# Branch merge notes

## Pulse jumps branch scope
- Contain only resources and logic related to pulse jumps.
- Keep `template.yaml` updated with jumps resources and handlers.
- Use the shared logger common layer.
- Include Lambda functions that populate pulse jumps into MongoDB.

### Jumps document format
- device_id
- previous pulse value
- current pulse value
- date/time in ISO UTC format without TZ

## Supabase sync updates
- `pulse_imitator_config.py` devices should match the DB `devices` table.
- Group IDs should match the DB `groups` table.
- Device/group relations should match patient/group relations from DB.
- `GROUPS` should stay synced with DB groups.

## Integration goal
- Merge `reduced-values-branch` and `pulse-jumps-branch` into `main` so experiments can run for both reduced values and pulse jumps.
