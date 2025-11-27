import './style.css';
import {
  saveEntry,
  loadEntries,
  deleteEntry,
  getSummary,
  getUsers,
  saveUser,
  updateUser,
  deleteUser,
  getPeriods,
  updatePeriod,
  getPayments,
  savePayment,
  getPaymentStatus,
  getPeriodUserHours
} from './logic.js';

// --- Elements ---
const entryForm = document.getElementById('entry-form');
const entriesBody = document.getElementById('entries-body');
const summaryContainer = document.getElementById('summary-container');
const dateInput = document.getElementById('date');
const userSelect = document.getElementById('user-select');
const quickAddUserBtn = document.getElementById('quick-add-user-btn');

// User Management Elements
const userForm = document.getElementById('user-form');
const userNameInput = document.getElementById('user-name');
const userRoleInput = document.getElementById('user-role');
const userActiveInput = document.getElementById('user-active');
const userSubmitBtn = document.getElementById('user-submit-btn');
const userCancelBtn = document.getElementById('user-cancel-btn');
const usersList = document.getElementById('users-list');

// Track edit mode
let editingUserId = null;

// Period Management Elements
const periodsBody = document.getElementById('periods-body');

// Payment Tracking Elements
const paymentPeriodSelect = document.getElementById('payment-period-select');
const paymentsBody = document.getElementById('payments-body');

// Navigation Elements
const navBtns = document.querySelectorAll('.nav-btn');
const viewSections = document.querySelectorAll('.view-section');

// --- Initialization ---
dateInput.valueAsDate = new Date();
renderAll();

// --- Navigation ---
navBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    // Update buttons
    navBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Update views
    const targetId = btn.dataset.target;
    viewSections.forEach(section => {
      section.classList.remove('active');
      if (section.id === targetId) {
        section.classList.add('active');
      }
    });
  });
});

// --- Rendering ---
function renderAll() {
  renderEntries();
  renderSummary();
  renderUsers();
  renderPeriods();
  updateUserSelect();
  renderPaymentPeriodSelect();
  renderPayments();
}

function updateUserSelect() {
  const users = getUsers().filter(u => u.active); // Only show active users
  const currentVal = userSelect.value;

  userSelect.innerHTML = '<option value="">Select User...</option>' +
    users.map(u => `<option value="${u.id}">${u.name}</option>`).join('');

  if (currentVal && users.find(u => u.id === currentVal)) {
    userSelect.value = currentVal;
  }
}

function renderEntries() {
  const entries = loadEntries().sort((a, b) => new Date(b.date) - new Date(a.date));
  const users = getUsers();

  if (entries.length === 0) {
    entriesBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color: var(--text-secondary);">No entries found.</td></tr>';
    return;
  }

  entriesBody.innerHTML = entries.map(entry => {
    const user = users.find(u => u.id === entry.userId);
    const userName = user ? user.name : '<span style="color:var(--danger)">Unknown</span>';

    return `
    <tr>
      <td>${entry.date}</td>
      <td>${userName}</td>
      <td><small style="color: var(--text-secondary);">${entry.period ? entry.period.label.split(':')[0] : 'N/A'}</small></td>
      <td>${entry.startTime} - ${entry.endTime}</td>
      <td>${entry.duration} hrs</td>
      <td>
        <button class="btn-delete" data-id="${entry.id}" title="Delete">
          &times;
        </button>
      </td>
    </tr>
  `}).join('');

  // Attach delete listeners
  document.querySelectorAll('#entries-body .btn-delete').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = e.target.dataset.id;
      deleteEntry(id);
      renderAll();
    });
  });
}

function renderSummary() {
  const summary = getSummary();

  if (summary.length === 0) {
    summaryContainer.innerHTML = '<p style="color: var(--text-secondary); text-align: center;">No data yet.</p>';
    return;
  }

  summaryContainer.innerHTML = `<ul class="summary-list">
    ${summary.map(item => `
      <li class="summary-item">
        <span class="period-label">${item.label}</span>
        <span class="total-hours">${item.totalHours.toFixed(2)} hrs</span>
      </li>
    `).join('')}
  </ul>`;
}

function renderUsers() {
  const users = getUsers();

  if (users.length === 0) {
    usersList.innerHTML = '<tr><td colspan="4" style="text-align:center; color: var(--text-secondary);">No users added.</td></tr>';
    return;
  }

  usersList.innerHTML = users.map(user => {
    const statusBadge = user.active
      ? '<span style="color: var(--accent); font-weight: 500;">● Active</span>'
      : '<span style="color: var(--text-secondary);">○ Inactive</span>';

    return `
      <tr>
        <td>${user.name}</td>
        <td>${user.role}</td>
        <td>${statusBadge}</td>
        <td>
          <button class="btn-edit user-edit-btn" data-id="${user.id}" title="Edit">✎</button>
          <button class="btn-delete user-delete-btn" data-id="${user.id}" title="Delete">&times;</button>
        </td>
      </tr>
    `;
  }).join('');

  // Attach edit listeners
  document.querySelectorAll('.user-edit-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const userId = e.target.dataset.id;
      startEditUser(userId);
    });
  });

  // Attach delete listeners
  document.querySelectorAll('.user-delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (confirm('Are you sure you want to delete this user?')) {
        deleteUser(e.target.dataset.id);
        renderAll();
      }
    });
  });
}

function startEditUser(userId) {
  const users = getUsers();
  const user = users.find(u => u.id === userId);
  if (!user) return;

  editingUserId = userId;
  userNameInput.value = user.name;
  userRoleInput.value = user.role;
  userActiveInput.checked = user.active;
  userSubmitBtn.textContent = 'Update User';
  userCancelBtn.style.display = 'block';
  userNameInput.focus();
}

function cancelEditUser() {
  editingUserId = null;
  userForm.reset();
  userActiveInput.checked = true;
  userSubmitBtn.textContent = 'Add User';
  userCancelBtn.style.display = 'none';
}

function renderPeriods() {
  const periods = getPeriods();

  periodsBody.innerHTML = periods.map(period => `
    <tr>
      <td>${period.label.split(':')[0]}</td>
      <td><input type="date" class="period-date-input" data-id="${period.id}" data-type="start" value="${period.startDate}"></td>
      <td><input type="date" class="period-date-input" data-id="${period.id}" data-type="end" value="${period.endDate}"></td>
      <td>
        <button class="btn-primary period-save-btn" data-id="${period.id}" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Save</button>
      </td>
    </tr>
  `).join('');

  document.querySelectorAll('.period-save-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = e.target.dataset.id;
      const row = e.target.closest('tr');
      const start = row.querySelector(`input[data-type="start"]`).value;
      const end = row.querySelector(`input[data-type="end"]`).value;

      updatePeriod(id, start, end);
      alert('Period updated!');
      renderAll();
    });
  });
}

function renderPaymentPeriodSelect() {
  const periods = getPeriods();
  const currentVal = paymentPeriodSelect.value;

  // Sort periods descending (newest first)
  const sortedPeriods = [...periods].sort((a, b) => new Date(b.startDate) - new Date(a.startDate));

  paymentPeriodSelect.innerHTML = sortedPeriods.map(p =>
    `<option value="${p.id}">${p.label}</option>`
  ).join('');

  if (currentVal && periods.find(p => p.id === currentVal)) {
    paymentPeriodSelect.value = currentVal;
  } else if (sortedPeriods.length > 0 && !currentVal) {
    // Default to latest period if nothing selected
    paymentPeriodSelect.value = sortedPeriods[0].id;
  }
}

function renderPayments() {
  const periodId = paymentPeriodSelect.value;
  if (!periodId) return;

  const users = getUsers().filter(u => u.active); // Only show active users

  paymentsBody.innerHTML = users.map(user => {
    const totalHours = getPeriodUserHours(periodId, user.id);
    const payment = getPaymentStatus(periodId, user.id);
    const status = payment ? payment.status : 'Unpaid';
    const notes = payment ? payment.notes : '';

    const statusColor = status === 'Paid' ? 'var(--accent)' : 'var(--text-secondary)';

    return `
      <tr>
        <td>${user.name}</td>
        <td>${user.role}</td>
        <td>${totalHours.toFixed(2)} hrs</td>
        <td>
          <select class="payment-status-select" data-userid="${user.id}" style="padding: 0.25rem; width: auto; color: ${statusColor}; font-weight: 500;">
            <option value="Unpaid" ${status === 'Unpaid' ? 'selected' : ''}>Unpaid</option>
            <option value="Paid" ${status === 'Paid' ? 'selected' : ''}>Paid</option>
          </select>
        </td>
        <td>
          <input type="text" class="payment-notes-input" data-userid="${user.id}" value="${notes}" placeholder="Check # / Notes" style="padding: 0.25rem; font-size: 0.9rem;">
        </td>
        <td>
          <button class="btn-primary payment-save-btn" data-userid="${user.id}" style="padding: 0.25rem 0.5rem; font-size: 0.8rem;">Save</button>
        </td>
      </tr>
    `;
  }).join('');

  // Attach listeners
  document.querySelectorAll('.payment-save-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const userId = e.target.dataset.userid;
      const row = e.target.closest('tr');
      const status = row.querySelector('.payment-status-select').value;
      const notes = row.querySelector('.payment-notes-input').value;

      savePayment(periodId, userId, status, notes);

      // Visual feedback
      const originalText = e.target.textContent;
      e.target.textContent = 'Saved!';
      setTimeout(() => {
        e.target.textContent = originalText;
      }, 1000);

      // Update status color
      const select = row.querySelector('.payment-status-select');
      select.style.color = status === 'Paid' ? 'var(--accent)' : 'var(--text-secondary)';
    });
  });

  // Auto-update color on change
  document.querySelectorAll('.payment-status-select').forEach(select => {
    select.addEventListener('change', (e) => {
      e.target.style.color = e.target.value === 'Paid' ? 'var(--accent)' : 'var(--text-secondary)';
    });
  });
}

// --- Event Listeners ---

// Add Entry
entryForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const userId = userSelect.value;
  const date = document.getElementById('date').value;
  const startTime = document.getElementById('start-time').value;
  const endTime = document.getElementById('end-time').value;

  if (!userId) {
    alert('Please select a user.');
    return;
  }
  if (!date || !startTime || !endTime) return;

  if (startTime >= endTime) {
    alert('End time must be after start time.');
    return;
  }

  const entry = {
    userId,
    date,
    startTime,
    endTime
  };

  saveEntry(entry);
  renderAll();

  // Reset form but keep user selected
  const currentUser = userSelect.value;
  entryForm.reset();
  userSelect.value = currentUser;
  dateInput.valueAsDate = new Date();
});

// Add/Update User
userForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const name = userNameInput.value.trim();
  const role = userRoleInput.value;
  const active = userActiveInput.checked;

  if (name && role) {
    if (editingUserId) {
      // Update existing user
      updateUser(editingUserId, { name, role, active });
      cancelEditUser();
    } else {
      // Add new user
      saveUser(name, role, active);
      userForm.reset();
      userActiveInput.checked = true;
    }
    renderAll();
  }
});

// Cancel Edit
userCancelBtn.addEventListener('click', () => {
  cancelEditUser();
});

// Quick Add User
quickAddUserBtn.addEventListener('click', () => {
  const name = prompt('Enter new user name:');
  if (name && name.trim()) {
    const role = prompt('Select role (Employee/Contractor/Manager/Admin):', 'Employee');
    const validRoles = ['Employee', 'Contractor', 'Manager', 'Admin'];
    const selectedRole = validRoles.includes(role) ? role : 'Employee';

    const newUser = saveUser(name.trim(), selectedRole, true);
    renderAll();
    userSelect.value = newUser.id; // Select the new user
  }
});
