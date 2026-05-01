const API_URL = "";

// ── Elements Mapping ──
const els = {
    // Nav (Now Card Based)
    screens: document.querySelectorAll(".screen-container"),
    
    // Auth
    userEmail: document.getElementById("user-email"),
    connStatus: document.getElementById("connection-status"),
    
    // Sync
    btnConnect: document.getElementById("btn-drive-connect"),
    btnDisconnect: document.getElementById("btn-drive-disconnect"),
    btnSync: document.getElementById("btn-start-sync"),
    folderIdInput: document.getElementById("sync-folder-id"),
    progressArea: document.getElementById("sync-progress-container"),
    progressFill: document.getElementById("sync-progress-fill"),
    
    // Documents
    docsList: document.getElementById("documents-list"),
    
    // Chat
    chatInput: document.getElementById("chat-input"),
    btnSend: document.getElementById("btn-send-message"),
    chatMessages: document.getElementById("chat-messages"),
    recommendations: document.getElementById("recommendations-container"),
    
    // Settings
    btnThemeToggle: document.getElementById("btn-theme-toggle"),
    llmSelect: document.getElementById("setting-llm-provider"),
    btnPurge: document.getElementById("btn-purge-data"),
};

// ── State ──
let isDarkMode = true;
let currentUserId = null;

// ── Initialization ──
function init() {
    // Theme
    document.body.classList.add("dark-theme");

    // Theme Toggle
    els.btnThemeToggle.addEventListener("click", toggleTheme);

    // Initial Status Check
    checkStatus();
    
    // Sync Events
    els.btnConnect.addEventListener("click", () => window.location.href = `${API_URL}/auth/login`);
    if(els.btnDisconnect) els.btnDisconnect.addEventListener("click", handleDisconnect);
    els.btnSync.addEventListener("click", handleSync);
    
    // Chat Events
    els.btnSend.addEventListener("click", handleSendMessage);
    els.chatInput.addEventListener("keypress", (e) => e.key === "Enter" && handleSendMessage());
    
    // Settings Events
    els.btnPurge.addEventListener("click", handlePurge);
}

// ── Navigation ──
function scrollToSection(id) {
    const element = document.getElementById(id);
    if (!element) return;
    
    window.scrollTo({
        top: element.offsetTop - 100,
        behavior: 'smooth'
    });
    
    // Active glow animation
    els.screens.forEach(s => s.classList.remove('active-glow'));
    element.classList.add('active-glow');
}

// ── Theme Logic ──
function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle("dark-theme", isDarkMode);
    document.body.classList.toggle("light-theme", !isDarkMode);
    localStorage.setItem("theme", isDarkMode ? "dark" : "light");
}

// ── API Logic ──
async function checkStatus() {
    try {
        const res = await fetch(`${API_URL}/status`);
        if (!res.ok) throw new Error("Status check failed");
        const data = await res.json();

        // Update User Profile
        if (data.drive_connected) {
            const email = data.user_email || "Connected User";
            els.userEmail.textContent = email;
            els.userAvatarInitial.textContent = email.charAt(0).toUpperCase();
            els.connStatus.textContent = "Drive Connected";
            els.btnConnect.style.display = "none";
            els.btnDisconnect.style.display = "flex";
            els.btnSync.disabled = false;
        } else {
            els.userEmail.textContent = "Guest User";
            els.connStatus.textContent = "Not Connected";
            els.btnConnect.style.display = "flex";
            els.btnDisconnect.style.display = "none";
            els.btnSync.disabled = true;
        }

        // Update Sync Indicator
        if (data.faiss_index_exists) {
            els.syncDot.style.backgroundColor = "var(--secondary)";
            els.syncLabel.textContent = `${data.unique_documents} Files Ready`;
            renderDocuments(data.files || []);
            fetchRecommendations();
        } else {
            els.syncDot.style.backgroundColor = "var(--warning)";
            els.syncLabel.textContent = "No Data Indexed";
        }

    } catch (e) {
        console.error("Status check failed", e);
    }
}

async function handleSync() {
    const folderId = els.folderIdInput.value.trim();
    
    els.btnSync.disabled = true;
    els.progressArea.style.display = "block";
    els.progressFill.style.width = "20%";
    els.progressText.textContent = "Scanning folder...";

    try {
        const res = await fetch(`${API_URL}/sync-drive`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ folder_id: folderId })
        });
        const data = await res.json();

        if (res.ok) {
            els.progressFill.style.width = "100%";
            els.progressText.textContent = `Sync Complete: ${data.files_processed} files processed.`;
            logActivity(`Successfully synced ${data.files_processed} files.`);
            checkStatus();
        } else {
            throw new Error(data.detail || "Sync failed");
        }
    } catch (e) {
        els.progressFill.style.backgroundColor = "var(--danger)";
        els.progressText.textContent = `Error: ${e.message}`;
        logActivity(`Sync failed: ${e.message}`, "danger");
    } finally {
        els.btnSync.disabled = false;
    }
}

async function handleSendMessage() {
    const query = els.chatInput.value.trim();
    if (!query) return;

    appendMessage("user", query);
    els.chatInput.value = "";
    els.btnSend.disabled = true;

    const loadingId = "msg-" + Date.now();
    appendMessage("assistant", "Searching through documents...", [], loadingId);

    try {
        const res = await fetch(`${API_URL}/ask`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });
        const data = await res.json();

        const msgEl = document.getElementById(loadingId);
        if (res.ok) {
            const sourcesHtml = data.sources.map(s => `
                <a href="${s.link}" target="_blank" class="source-badge">
                    <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" style="margin-right:4px;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                    ${s.name}
                </a>
            `).join("");

            msgEl.innerHTML = `
                <div class="message-content">
                    ${data.answer}
                    ${data.sources.length ? `<div class="sources">${sourcesHtml}</div>` : ""}
                </div>
            `;
        } else {
            msgEl.innerHTML = `<div class="message-content danger-text">Error: ${data.detail}</div>`;
        }
    } catch (e) {
        document.getElementById(loadingId).innerHTML = `<div class="message-content danger-text">Network error occurred.</div>`;
    } finally {
        els.btnSend.disabled = false;
        els.chatInput.focus();
    }
}

async function fetchRecommendations() {
    try {
        const res = await fetch(`${API_URL}/recommend-questions`);
        if (!res.ok) return;
        const data = await res.json();
        
        if (data.questions && data.questions.length > 0) {
            els.recommendations.innerHTML = "";
            data.questions.forEach(q => {
                const pill = document.createElement("div");
                pill.className = "recommend-pill";
                pill.textContent = q;
                pill.onclick = () => {
                    els.chatInput.value = q;
                    handleSendMessage();
                };
                els.recommendations.appendChild(pill);
            });
            els.recommendations.style.display = "flex";
        }
    } catch (e) {}
}

async function handleDisconnect() {
    if (!confirm("Are you sure you want to disconnect Google Drive?")) return;
    const res = await fetch(`${API_URL}/disconnect`, { method: "POST" });
    if (res.ok) window.location.reload();
}

async function handlePurge() {
    if (!confirm("This will PERMANENTLY delete all indexed documents and history. Continue?")) return;
    const res = await fetch(`${API_URL}/clear-data`, { method: "POST" });
    if (res.ok) window.location.reload();
}

// ── UI Helpers ──
function appendMessage(role, text, sources = [], id = null) {
    const msg = document.createElement("div");
    msg.className = `message ${role}`;
    if (id) msg.id = id;
    
    msg.innerHTML = `<div class="message-content">${text}</div>`;
    els.chatMessages.appendChild(msg);
    els.chatMessages.scrollTop = els.chatMessages.scrollHeight;
}

function renderDocuments(files) {
    els.docsList.innerHTML = "";
    if (files.length === 0) {
        els.docsList.innerHTML = '<div class="empty-state">No documents found.</div>';
        return;
    }

    files.forEach(f => {
        const card = document.createElement("div");
        card.className = "doc-card";
        card.innerHTML = `
            <div class="doc-info">
                <h4>${f.name}</h4>
                <div class="doc-meta">ID: ${f.id.substring(0, 12)}...</div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:auto;">
                <span class="sync-indicator">
                    <span class="sync-dot" style="background-color:var(--secondary)"></span>
                    Indexed
                </span>
                <button onclick="handleDeleteDoc('${f.id}')" class="btn-icon" style="color:var(--danger)">
                    <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                </button>
            </div>
        `;
        els.docsList.appendChild(card);
    });
}

window.handleDeleteDoc = async function(id) {
    if (!confirm("Delete this document from knowledge base?")) return;
    const res = await fetch(`${API_URL}/delete-file?doc_id=${encodeURIComponent(id)}`, { method: "POST" });
    if (res.ok) checkStatus();
};

function logActivity(text, type = "info") {
    const entry = document.createElement("div");
    entry.style.padding = "8px 0";
    entry.style.fontSize = "0.85rem";
    entry.style.borderBottom = "1px solid var(--border)";
    entry.style.color = type === "danger" ? "var(--danger)" : "var(--text-main)";
    entry.textContent = `[${new Date().toLocaleTimeString()}] ${text}`;
    
    if (els.activityLog.querySelector(".empty-state")) {
        els.activityLog.innerHTML = "";
    }
    els.activityLog.prepend(entry);
}

// Launch
init();
