const term = document.getElementById("terminal");
const input = document.getElementById("cmd");
const statusBox = document.getElementById("status");

function print(text) {
  if (!text) return;
  const div = document.createElement("div");
  div.textContent = text;
  term.appendChild(div);
  term.scrollTop = term.scrollHeight;
}

input.addEventListener("keydown", e => {
  if (e.key === "Enter") {
    const cmd = input.value.trim();
    if (!cmd) return;

    print("$ " + cmd);
    input.value = "";

    if (cmd === "clear" || cmd === "cls") {
      term.innerHTML = "";
      return;
    }

    fetch("/exec", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({cmd})
    })
    .then(r => r.text())
    .then(out => {
      out = out.replace(/\x1B\[[0-9;]*[A-Za-z]/g, "");
      print(out);
    });
  }
});

function updateStatus() {
  fetch("/status")
    .then(r => r.json())
    .then(data => {
      statusBox.textContent = JSON.stringify(data, null, 2);
    });
}

setInterval(updateStatus, 4000);
updateStatus();
