# Use Cases and Modules

## Actors
- **Parking Operator/Admin:** records arrivals, processes exits, monitors occupancy and views history.
- **Driver:** sees availability, parks in an assigned slot and pays at exit.
- **Barrier Controller:** receives an open instruction after successful payment (simulated in this project).

## Modules

| Module | Main requirement | Key operations |
|---|---|---|
| Authentication | Secure operator access | Login/logout |
| Slot Management | Visual availability | Display, status updates |
| Vehicle Entry | Record arrival | Vehicle registration, slot assignment, timestamp |
| Parking Session | Track stay | Entry/exit timestamps, active/completed state |
| Fee & Payment | Automatic billing | Duration calculation, tariff selection, payment recording |
| Barrier Control | Allow exit | Payment confirmation and barrier-open simulation |
| History & Reporting | Management information | Search/view completed sessions and revenue |
| Dynamic Database | Persistent state | SQLite tables, relationships, constraints, transactions |

## Main use-case flow
1. Operator logs in.
2. Dashboard displays available/occupied slots.
3. Driver/vehicle arrives.
4. Operator selects an available slot and records entry.
5. System marks slot occupied and starts session timer from entry timestamp.
6. Vehicle returns to exit.
7. Operator selects registration.
8. System calculates elapsed minutes and fee.
9. Payment is recorded.
10. System marks slot available and displays barrier-open confirmation.
11. Receipt/session remains available in history.
