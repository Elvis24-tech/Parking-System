# ParkSmart Kenya — Project Report

## 1. Introduction
ParkSmart Kenya is a web-based parking management system designed to automate vehicle entry, parking-space allocation, fee calculation and vehicle exit. It addresses the stated client requirement that drivers/operators should see available parking spaces before entry and that the system should automatically calculate the amount payable when a vehicle exits.

## 2. Objectives
- Provide a visual real-time parking slot map.
- Record vehicles and arrival times.
- Allocate only available slots.
- Calculate parking duration automatically.
- Apply the supplied Kenya Shilling tariff.
- Record payment and generate a receipt number.
- Simulate opening the exit barrier after payment.
- Maintain a dynamic database and historical records.

## 3. Proposed technology
- Python 3
- Flask web framework
- SQLite relational database
- HTML5/CSS3/JavaScript frontend
- Git/GitHub for version control and submission

## 4. Functional requirements
The system provides authentication, slot management, vehicle entry, parking-session management, exit/payment, barrier simulation, history and revenue information.

## 5. Non-functional considerations
- Responsive web interface.
- Transactional database updates.
- Input validation and constrained status values.
- Clear separation between presentation templates, application logic and database.
- Code comments and documentation.

## 6. Tariff implementation
The tariff supplied by the client is implemented exactly as follows:

| Duration | Fee |
|---|---:|
| Up to 30 minutes | KSh 0 |
| Up to 2 hours | KSh 50 |
| Up to 4 hours | KSh 100 |
| Up to 6 hours | KSh 300 |
| Over 6 hours | KSh 500 |

## 7. Testing scenarios
1. Login with correct credentials.
2. View 30 slots and identify available spaces.
3. Record a vehicle into an available slot.
4. Confirm the slot changes to OCCUPIED.
5. Try to select an occupied slot; the server rejects it.
6. Process an active vehicle exit.
7. Verify duration and fee calculation.
8. Verify payment and receipt creation.
9. Verify barrier-open confirmation.
10. Verify the slot returns to AVAILABLE and history is updated.

## 8. Limitations and future improvements
This student implementation simulates the physical barrier. A production system could integrate ANPR cameras, RFID tickets, M-Pesa Daraja payments, physical barrier controllers, sensors, role-based access control, HTTPS, cloud hosting, backups and audit logs.

## 9. Conclusion
The system translates the client terms of reference into modules, algorithms, data structures and a dynamic database. The web application provides an end-to-end parking workflow from availability and entry through automated billing and exit.
