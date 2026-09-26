# Algorithms

## 1. Slot Availability Algorithm
**Input:** parking slot records.  
**Output:** visual list of AVAILABLE, OCCUPIED and RESERVED slots.

1. Retrieve all slots ordered by zone and slot code.
2. For each slot, read its status.
3. Map `AVAILABLE` to a green visual slot, `OCCUPIED` to red and `RESERVED` to amber.
4. Display the slot code so the operator can select an available location.
5. Count available and occupied slots for dashboard statistics.

**Complexity:** O(n) time and O(n) output space for n slots.

## 2. Vehicle Entry Algorithm
1. Read registration, owner, phone, vehicle type and selected slot.
2. Normalize registration to uppercase.
3. Check that the selected slot exists and has status `AVAILABLE`.
4. Find the vehicle in the vehicle table. Create it if it does not exist; otherwise update its details.
5. Check that the vehicle has no active parking session.
6. Create a new active parking session with the current timestamp.
7. Change the slot status from `AVAILABLE` to `OCCUPIED`.
8. Commit the transaction.
9. Display confirmation.

**Complexity:** O(log n) average for indexed registration/slot lookups; database dependent.

## 3. Parking Fee Algorithm
Let `m` be the total number of minutes parked.

- If `m <= 30`, fee = KSh 0.
- Else if `m <= 120`, fee = KSh 50.
- Else if `m <= 240`, fee = KSh 100.
- Else if `m <= 360`, fee = KSh 300.
- Else, fee = KSh 500.

**Complexity:** O(1) because the number of tariff bands is fixed.

## 4. Vehicle Exit Algorithm
1. Read the vehicle registration.
2. Search for its active parking session.
3. Record current time as exit time.
4. Compute elapsed minutes: `floor((exit - entry) / 60 seconds)`.
5. Apply the parking fee algorithm.
6. Record payment method and generate a receipt number.
7. Mark session `COMPLETED` and `PAID`.
8. Change the occupied slot to `AVAILABLE`.
9. Record payment in the payment table.
10. Display receipt and simulated `BARRIER OPEN` message.

**Complexity:** O(log n) average for indexed vehicle/session lookups.

## 5. Barrier Algorithm
1. Confirm the payment record was created successfully.
2. Confirm the session is marked `PAID`.
3. Signal `OPEN` to the simulated barrier.
4. Permit vehicle exit.
5. The associated slot is already returned to `AVAILABLE` as part of the transaction.

In a physical deployment, step 3 would call a GPIO/PLC/barrier-controller API. This student version simulates it in the web interface.
