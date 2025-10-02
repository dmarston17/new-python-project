// DOM elements we interact with
const itemsDiv = document.getElementById('items');
const keyInput = document.getElementById('key');
const valueInput = document.getElementById('value');
const createBtn = document.getElementById('create');

// Open a WebSocket connection to receive real-time updates from the server.
// The URL uses the current origin (host+port) so it works in local dev.
const ws = new WebSocket(`ws://${location.host}/ws`);
ws.onmessage = (e) => {
  const msg = e.data;
  try {
    // Expect JSON messages like {action: 'created'|'updated'|'deleted', key, value?}
    const obj = JSON.parse(msg);
    if (obj.action === 'created' || obj.action === 'updated') {
      // Update or insert a single item in the DOM without re-fetching everything
      upsertDOM(obj.key, obj.value);
    } else if (obj.action === 'deleted') {
      removeFromDOM(obj.key);
    }
  } catch (err) {
    // If message isn't JSON, just log it (debugging / echo fallback)
    console.log('ws (raw):', msg);
  }
};

// Fetch current items from the server and render them.
async function refresh() {
  const res = await fetch('/items');
  const data = await res.json();
  itemsDiv.innerHTML = '';
  for (const [k, v] of Object.entries(data)) {
    const el = document.createElement('div');
    el.className = 'item';
    el.innerHTML = `<strong>${k}</strong>: <span>${v}</span> <button data-key="${k}" class="del">Delete</button>`;
    itemsDiv.appendChild(el);
    // Clicking the item (not the delete button) loads it into the form.
    el.addEventListener('click', (e) => {
      if (e.target.classList.contains('del')) return;
      keyInput.value = k;
      valueInput.value = v;
      setFormModeEdit(k);
    });
  }
  // Wire up delete buttons after rendering. This is a simple approach; in
  // larger apps you'd use a framework or better event delegation.
  document.querySelectorAll('.del').forEach(btn => btn.addEventListener('click', async (e) => {
    const key = e.target.dataset.key;
    await fetch(`/items/${encodeURIComponent(key)}`, { method: 'DELETE' });
    refresh();
  }));
}

function upsertDOM(key, value) {
  // If element exists, update value; otherwise append new entry
  const existing = [...document.querySelectorAll('.item')].find(el => el.querySelector('strong').textContent === key);
  if (existing) {
    existing.querySelector('span').textContent = value;
    return;
  }
  const el = document.createElement('div');
  el.className = 'item';
  el.innerHTML = `<strong>${key}</strong>: <span>${value}</span> <button data-key="${key}" class="del">Delete</button>`;
  itemsDiv.appendChild(el);
  el.querySelector('.del').addEventListener('click', async (e) => {
    const key = e.target.dataset.key;
    await fetch(`/items/${encodeURIComponent(key)}`, { method: 'DELETE' });
    removeFromDOM(key);
  });
  el.addEventListener('click', (e) => {
    if (e.target.classList.contains('del')) return;
    keyInput.value = key;
    valueInput.value = value;
    setFormModeEdit(key);
  });
}

function removeFromDOM(key) {
  const existing = [...document.querySelectorAll('.item')].find(el => el.querySelector('strong').textContent === key);
  if (existing) existing.remove();
}

// Create / Update action wired to the form button. Simple UX: if the key
// currently exists we send PUT /items/{key} to update it; otherwise we POST
// to create it. Clicking an item in the list loads it into the form.
let editingKey = null;
function setFormModeCreate() {
  editingKey = null;
  createBtn.textContent = 'Create';
}
function setFormModeEdit(key) {
  editingKey = key;
  createBtn.textContent = 'Save';
}

createBtn.addEventListener('click', async () => {
  const key = keyInput.value.trim();
  const value = valueInput.value.trim();
  if (!key) return; // require a key

  if (editingKey && editingKey === key) {
    // Update existing key
    await fetch(`/items/${encodeURIComponent(key)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ value })
    });
  } else {
    // Create new (or upsert) via POST
    await fetch(`/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key, value })
    });
  }

  keyInput.value = '';
  valueInput.value = '';
  setFormModeCreate();
});

// Initial render
refresh();

// Tip: open the browser console to see WebSocket logs and troubleshoot.
