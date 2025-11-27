export const STORAGE_KEY = 'time_entry_app_data';
export const USERS_KEY = 'time_entry_users';
export const PERIODS_KEY = 'time_entry_periods';
export const PAYMENTS_KEY = 'time_entry_payments';

// --- Helpers ---
export function calculateDuration(startTime, endTime) {
    if (!startTime || !endTime) return 0;

    const [startH, startM] = startTime.split(':').map(Number);
    const [endH, endM] = endTime.split(':').map(Number);

    const startMinutes = startH * 60 + startM;
    const endMinutes = endH * 60 + endM;

    let diff = endMinutes - startMinutes;
    if (diff < 0) diff += 24 * 60;

    return Number((diff / 60).toFixed(2));
}

// --- Users ---
export function getUsers() {
    const data = localStorage.getItem(USERS_KEY);
    const users = data ? JSON.parse(data) : [];

    // Ensure backward compatibility - add default role and active status if missing
    return users.map(user => ({
        ...user,
        role: user.role || 'Employee',
        active: user.active !== undefined ? user.active : true
    }));
}

export function saveUser(name, role = 'Employee', active = true) {
    const users = getUsers();
    const newUser = {
        id: Date.now().toString(),
        name,
        role,
        active
    };
    users.push(newUser);
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
    return newUser;
}

export function updateUser(id, userData) {
    const users = getUsers();
    const index = users.findIndex(u => u.id === id);
    if (index !== -1) {
        users[index] = {
            ...users[index],
            ...userData,
            id // Preserve the original ID
        };
        localStorage.setItem(USERS_KEY, JSON.stringify(users));
        return users[index];
    }
    return null;
}

export function deleteUser(id) {
    let users = getUsers();
    users = users.filter(u => u.id !== id);
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

// --- Periods ---
export function getPeriods() {
    const data = localStorage.getItem(PERIODS_KEY);
    if (data) return JSON.parse(data);

    // Generate defaults if none exist
    const defaults = generateDefaultPeriods(new Date().getFullYear());
    savePeriods(defaults);
    return defaults;
}

export function savePeriods(periods) {
    localStorage.setItem(PERIODS_KEY, JSON.stringify(periods));
}

export function updatePeriod(id, startDate, endDate) {
    const periods = getPeriods();
    const index = periods.findIndex(p => p.id === id);
    if (index !== -1) {
        periods[index].startDate = startDate;
        periods[index].endDate = endDate;
        // Update label
        const start = new Date(startDate);
        const end = new Date(endDate);
        const options = { month: 'short', day: 'numeric' };
        periods[index].label = `Period ${periods[index].periodNum}: ${start.toLocaleDateString('en-US', options)} - ${end.toLocaleDateString('en-US', options)}`;

        savePeriods(periods);
    }
}

function generateDefaultPeriods(year) {
    const periods = [];
    const startOfYear = new Date(year, 0, 1);
    let currentStart = new Date(startOfYear);

    for (let i = 1; i <= 26; i++) {
        const currentEnd = new Date(currentStart);
        currentEnd.setDate(currentStart.getDate() + 13);

        const options = { month: 'short', day: 'numeric' };
        const label = `Period ${i}: ${currentStart.toLocaleDateString('en-US', options)} - ${currentEnd.toLocaleDateString('en-US', options)}`;

        periods.push({
            id: `${year}-P${i}`,
            periodNum: i,
            year: year,
            startDate: currentStart.toISOString().split('T')[0],
            endDate: currentEnd.toISOString().split('T')[0],
            label: label
        });

        // Next period starts day after current end
        currentStart = new Date(currentEnd);
        currentStart.setDate(currentEnd.getDate() + 1);
    }
    return periods;
}

export function getPeriodForDate(dateStr) {
    const periods = getPeriods();
    const date = new Date(dateStr).toISOString().split('T')[0];

    return periods.find(p => date >= p.startDate && date <= p.endDate) || null;
}

// --- Payments ---
export function getPayments() {
    const data = localStorage.getItem(PAYMENTS_KEY);
    return data ? JSON.parse(data) : [];
}

export function savePayment(periodId, userId, status, notes) {
    const payments = getPayments();
    const index = payments.findIndex(p => p.periodId === periodId && p.userId === userId);

    const paymentData = {
        periodId,
        userId,
        status,
        notes,
        updatedAt: new Date().toISOString()
    };

    if (index !== -1) {
        payments[index] = { ...payments[index], ...paymentData };
    } else {
        payments.push(paymentData);
    }

    localStorage.setItem(PAYMENTS_KEY, JSON.stringify(payments));
    return paymentData;
}

export function getPaymentStatus(periodId, userId) {
    const payments = getPayments();
    return payments.find(p => p.periodId === periodId && p.userId === userId) || null;
}

export function getPeriodUserHours(periodId, userId) {
    const entries = loadEntries();
    const period = getPeriods().find(p => p.id === periodId);

    if (!period) return 0;

    return entries
        .filter(e => e.userId === userId && e.date >= period.startDate && e.date <= period.endDate)
        .reduce((total, e) => total + e.duration, 0);
}

// --- Entries ---
export function loadEntries() {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
}

export function saveEntry(entry) {
    const entries = loadEntries();
    const period = getPeriodForDate(entry.date);

    entries.push({
        id: Date.now().toString(),
        ...entry,
        duration: calculateDuration(entry.startTime, entry.endTime),
        period: period // Store full period object or just ID? Storing object for simplicity in display, but ID is better for ref. Let's store object snapshot for now as requirements are simple.
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
    return entries;
}

export function deleteEntry(id) {
    let entries = loadEntries();
    entries = entries.filter(e => e.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
    return entries;
}

export function getSummary() {
    const entries = loadEntries();
    const summary = {};

    entries.forEach(entry => {
        if (!entry.period) return; // Skip if no period found (shouldn't happen with valid dates)

        const pid = entry.period.id;
        if (!summary[pid]) {
            summary[pid] = {
                label: entry.period.label,
                totalHours: 0,
                year: entry.period.year,
                periodNum: entry.period.periodNum
            };
        }
        summary[pid].totalHours += entry.duration;
    });

    return Object.values(summary).sort((a, b) => {
        if (a.year !== b.year) return b.year - a.year;
        return b.periodNum - a.periodNum;
    });
}
