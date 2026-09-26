# Dynamic Database Design

## ER-style relationship

`VEHICLES (1) ---- (M) PARKING_SESSIONS (M) ---- (1) PARKING_SLOTS`

`PARKING_SESSIONS (1) ---- (0..1) PAYMENTS`

## Tables

### parking_slots
- id: INTEGER PK
- slot_code: TEXT UNIQUE
- status: AVAILABLE/OCCUPIED/RESERVED
- zone: TEXT

### vehicles
- id: INTEGER PK
- registration: TEXT UNIQUE
- vehicle_type: TEXT
- owner_name: TEXT
- phone: TEXT
- created_at: timestamp

### parking_sessions
- id: INTEGER PK
- vehicle_id: FK vehicles.id
- slot_id: FK parking_slots.id
- entry_time: timestamp
- exit_time: timestamp nullable
- duration_minutes: INTEGER nullable
- amount: INTEGER
- payment_status: UNPAID/PAID
- session_status: ACTIVE/COMPLETED

### payments
- id: INTEGER PK
- session_id: FK parking_sessions.id UNIQUE
- amount: INTEGER
- payment_method: TEXT
- paid_at: timestamp
- receipt_no: TEXT UNIQUE

## Dynamic behavior
At entry, the database changes the chosen slot to OCCUPIED and creates an active session. At exit, it stores duration and amount, creates a payment, completes the session and returns the slot to AVAILABLE. This makes the visual dashboard reflect the current state without manually editing slot records.
