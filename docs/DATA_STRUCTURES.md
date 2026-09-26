# Data Structures and Reasons for Use

| Data structure | Where used | Reason |
|---|---|---|
| List / array | Tariff bands and slot collections returned from DB | Simple ordered traversal and display. |
| Dictionary / JSON object | API fee response and receipt result | Key-value representation is natural for web communication. |
| Relational tables | Slots, vehicles, sessions, payments | Persistent structured storage with relationships and constraints. |
| Indexes (SQLite primary/unique keys) | IDs, registration, slot code, receipt | Fast lookup and uniqueness enforcement. |
| Queue concept | Future entry/exit vehicle processing | Useful if gates later receive many vehicles concurrently. |
| Stack concept | Could support undo/audit workflow | Useful for reversing the most recent administrative operation, although not required for normal parking flow. |

### Why a relational database?
The system has related entities: one vehicle can have many parking sessions; each session references one slot; each completed session can have one payment. SQLite provides foreign keys, constraints, transactions and SQL queries without requiring a separate database server.

### Data integrity
- Registration numbers are unique.
- Slot codes are unique.
- A session must reference an existing vehicle and slot.
- Slot status is restricted to AVAILABLE, OCCUPIED or RESERVED.
- Session/payment states are restricted to known values.
- Payment is unique per session.
