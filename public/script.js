const form = document.getElementById('form');
const input = document.getElementById('input');
const messages = document.getElementById('messages');

function addMessage(text, who = 'bot'){
  const el = document.createElement('div');
  el.className = 'message ' + (who === 'user' ? 'user' : 'bot');
  el.textContent = text;
  messages.appendChild(el);
  messages.scrollTop = messages.scrollHeight;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';

  try {
    const res = await fetch('/api/mcp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tool: 'handle_message', input: { message: text } })
    });

    const data = await res.json();
    if (res.ok && data && data.result) {
      addMessage(data.result, 'bot');
    } else {
      addMessage('Error: ' + (data?.error || JSON.stringify(data)), 'bot');
    }
  } catch (err) {
    addMessage('Network error: ' + err.message, 'bot');
  }
});

// Welcome message
addMessage('Welcome! Try commands: list, summarize, add:Title|YYYY-MM-DD|Desc, delete:Title');