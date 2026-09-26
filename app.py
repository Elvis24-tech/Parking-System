from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'parking.db'
app = Flask(__name__)
app.secret_key = 'change-this-secret-key'
RATES = [
    (30, 0),
    (120, 50),
    (240, 100),
    (360, 300),
    (float('inf'), 500),
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_code TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'AVAILABLE' CHECK(status IN ('AVAILABLE','OCCUPIED','RESERVED')),
            zone TEXT NOT NULL DEFAULT 'A'
        );

        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration TEXT UNIQUE NOT NULL,
            vehicle_type TEXT NOT NULL DEFAULT 'Car',
            owner_name TEXT,
            phone TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS parking_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            entry_time TEXT NOT NULL,
            exit_time TEXT,
            duration_minutes INTEGER,
            amount INTEGER DEFAULT 0,
            payment_status TEXT NOT NULL DEFAULT 'UNPAID' CHECK(payment_status IN ('UNPAID','PAID')),
            session_status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK(session_status IN ('ACTIVE','COMPLETED')),
            FOREIGN KEY(vehicle_id) REFERENCES vehicles(id),
            FOREIGN KEY(slot_id) REFERENCES parking_slots(id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER UNIQUE NOT NULL,
            amount INTEGER NOT NULL,
            payment_method TEXT NOT NULL,
            paid_at TEXT NOT NULL,
            receipt_no TEXT UNIQUE NOT NULL,
            FOREIGN KEY(session_id) REFERENCES parking_sessions(id)
        );
    ''')
    count = conn.execute('SELECT COUNT(*) FROM parking_slots').fetchone()[0]
    if count == 0:
        slots = [(f'A-{i:02d}', 'A') for i in range(1, 21)] + [(f'B-{i:02d}', 'B') for i in range(1, 11)]
        conn.executemany('INSERT INTO parking_slots(slot_code, zone) VALUES (?, ?)', slots)
    conn.commit()
    conn.close()


def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def calculate_fee(minutes):
    """Return fee according to the supplied parking tariff."""
    for limit, fee in RATES:
        if minutes <= limit:
            return fee
    return 500


def calculate_duration(entry, exit_time):
    start = datetime.strptime(entry, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(exit_time, '%Y-%m-%d %H:%M:%S')
    return max(0, int((end - start).total_seconds() // 60))


def require_login():
    return session.get('logged_in') is True


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
def dashboard():
    if not require_login():
        return redirect(url_for('login'))
    conn = get_db()
    slots = conn.execute('SELECT * FROM parking_slots ORDER BY zone, slot_code').fetchall()
    active = conn.execute('''SELECT ps.*, v.registration, v.vehicle_type, s.slot_code
                            FROM parking_sessions ps JOIN vehicles v ON v.id=ps.vehicle_id
                            JOIN parking_slots s ON s.id=ps.slot_id
                            WHERE ps.session_status='ACTIVE' ORDER BY ps.entry_time DESC''').fetchall()
    totals = conn.execute('''SELECT
        COUNT(*) AS total,
        SUM(CASE WHEN status='AVAILABLE' THEN 1 ELSE 0 END) AS available,
        SUM(CASE WHEN status='OCCUPIED' THEN 1 ELSE 0 END) AS occupied,
        SUM(CASE WHEN status='RESERVED' THEN 1 ELSE 0 END) AS reserved
        FROM parking_slots''').fetchone()
    revenue = conn.execute("SELECT COALESCE(SUM(amount),0) FROM payments").fetchone()[0]
    conn.close()
    return render_template('dashboard.html', slots=slots, active=active, totals=totals, revenue=revenue)


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    if not require_login():
        return redirect(url_for('login'))
    conn = get_db()
    if request.method == 'POST':
        registration = request.form.get('registration', '').strip().upper()
        owner = request.form.get('owner_name', '').strip()
        phone = request.form.get('phone', '').strip()
        vehicle_type = request.form.get('vehicle_type', 'Car').strip()
        slot_id = request.form.get('slot_id')
        if not registration or not slot_id:
            flash('Registration number and parking slot are required.', 'danger')
        else:
            try:
                slot = conn.execute('SELECT * FROM parking_slots WHERE id=?', (slot_id,)).fetchone()
                if not slot or slot['status'] != 'AVAILABLE':
                    raise ValueError('Selected slot is no longer available.')
                existing = conn.execute('SELECT * FROM vehicles WHERE registration=?', (registration,)).fetchone()
                if existing:
                    vehicle_id = existing['id']
                    conn.execute('UPDATE vehicles SET owner_name=?, phone=?, vehicle_type=? WHERE id=?', (owner, phone, vehicle_type, vehicle_id))
                else:
                    cur = conn.execute('INSERT INTO vehicles(registration, vehicle_type, owner_name, phone) VALUES (?,?,?,?)', (registration, vehicle_type, owner, phone))
                    vehicle_id = cur.lastrowid
                active = conn.execute("SELECT id FROM parking_sessions WHERE vehicle_id=? AND session_status='ACTIVE'", (vehicle_id,)).fetchone()
                if active:
                    raise ValueError('This vehicle already has an active parking session.')
                conn.execute('INSERT INTO parking_sessions(vehicle_id, slot_id, entry_time) VALUES (?,?,?)', (vehicle_id, slot_id, now_str()))
                conn.execute("UPDATE parking_slots SET status='OCCUPIED' WHERE id=?", (slot_id,))
                conn.commit()
                flash(f'Vehicle {registration} admitted to {slot["slot_code"]}.', 'success')
                return redirect(url_for('dashboard'))
            except (sqlite3.IntegrityError, ValueError) as exc:
                conn.rollback()
                flash(str(exc), 'danger')
    slots = conn.execute("SELECT * FROM parking_slots WHERE status='AVAILABLE' ORDER BY zone, slot_code").fetchall()
    conn.close()
    return render_template('entry.html', slots=slots)

@app.route('/exit', methods=['GET', 'POST'])
def exit_vehicle():
    if not require_login():
        return redirect(url_for('login'))
    conn = get_db()
    result = None
    if request.method == 'POST':
        registration = request.form.get('registration', '').strip().upper()
        payment_method = request.form.get('payment_method', 'Cash')
        row = conn.execute('''SELECT ps.*, v.registration, s.slot_code, s.id AS slot_id
                              FROM parking_sessions ps JOIN vehicles v ON v.id=ps.vehicle_id
                              JOIN parking_slots s ON s.id=ps.slot_id
                              WHERE v.registration=? AND ps.session_status='ACTIVE' ''', (registration,)).fetchone()
        if not row:
            flash('No active parking session found for that registration.', 'danger')
        else:
            exit_time = now_str()
            minutes = calculate_duration(row['entry_time'], exit_time)
            amount = calculate_fee(minutes)
            receipt = f'RCP-{datetime.now().strftime("%Y%m%d%H%M%S")}-{row["id"]}'
            conn.execute('''UPDATE parking_sessions SET exit_time=?, duration_minutes=?, amount=?, payment_status='PAID', session_status='COMPLETED' WHERE id=?''', (exit_time, minutes, amount, row['id']))
            conn.execute("UPDATE parking_slots SET status='AVAILABLE' WHERE id=?", (row['slot_id'],))
            conn.execute('INSERT INTO payments(session_id, amount, payment_method, paid_at, receipt_no) VALUES (?,?,?,?,?)', (row['id'], amount, payment_method, exit_time, receipt))
            conn.commit()
            result = {'registration': registration, 'slot_code': row['slot_code'], 'entry_time': row['entry_time'], 'exit_time': exit_time, 'minutes': minutes, 'amount': amount, 'receipt': receipt, 'payment_method': payment_method}
            flash('Payment recorded. Barrier OPEN — vehicle may exit.', 'success')
    active = conn.execute("SELECT v.registration, ps.entry_time, s.slot_code FROM parking_sessions ps JOIN vehicles v ON v.id=ps.vehicle_id JOIN parking_slots s ON s.id=ps.slot_id WHERE ps.session_status='ACTIVE' ORDER BY ps.entry_time").fetchall()
    conn.close()
    return render_template('exit.html', active=active, result=result)

@app.route('/history')
def history():
    if not require_login():
        return redirect(url_for('login'))
    conn = get_db()
    rows = conn.execute('''SELECT ps.*, v.registration, v.vehicle_type, s.slot_code, p.receipt_no, p.payment_method
                           FROM parking_sessions ps JOIN vehicles v ON v.id=ps.vehicle_id
                           JOIN parking_slots s ON s.id=ps.slot_id
                           LEFT JOIN payments p ON p.session_id=ps.id
                           ORDER BY ps.id DESC''').fetchall()
    conn.close()
    return render_template('history.html', rows=rows)

@app.route('/api/slots')
def api_slots():
    conn = get_db()
    rows = conn.execute('SELECT slot_code, status, zone FROM parking_slots ORDER BY zone, slot_code').fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/fee', methods=['POST'])
def api_fee():
    data = request.get_json(silent=True) or {}
    minutes = max(0, int(data.get('minutes', 0)))
    return jsonify({'minutes': minutes, 'amount': calculate_fee(minutes)})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
