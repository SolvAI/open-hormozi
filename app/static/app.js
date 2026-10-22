'use strict';

/* OpenHormozi local UI. Plain JS, no build step.
   Views: strategy list (#/), new strategy form (#/new), one strategy (#/job/:id), settings (#/settings). */

const view = document.getElementById('view');
const toastBox = document.getElementById('toasts');

const state = {
  settings: null,
  schema: null,
  jobs: null,
  statuses: new Map(),   // job id → last seen status, to toast transitions
  route: null,
  ui: { renaming: false, logOpen: false, log: '' },
};

const TIERS = [
  { prefix: 'U', title: 'Strategy' },
  { prefix: 'CH', title: 'Acquisition channels' },
  { prefix: 'FC', title: 'Funnel' },
  { prefix: 'BM', title: 'Sales and operations' },
  { prefix: 'MT', title: 'Proof and tools' },
];

const STATUS_LABEL = {
  queued: 'Queued',
  running: 'Generating',
  completed: 'Ready',
  partial: 'Ready, with gaps',
  failed: 'Stopped',
  cancelled: 'Cancelled',
  interrupted: 'Interrupted',
};

const DRAFT_KEY = 'openhormozi.draft';

// ─── Helpers ────────────────────────────────────────────────

function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function fmtMoney(usd) {
  return '$' + (usd || 0).toFixed(usd >= 100 ? 0 : 2);
}

function fmtDuration(seconds) {
  const s = Math.max(0, Math.round(seconds || 0));
  if (s < 60) return `${s} s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m} min`;
  return `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, '0')} min`;
}

function fmtDate(iso) {
  if (!iso) return '';
  return new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }).format(new Date(iso));
}

function fmtSize(bytes) {
  return bytes > 1e6 ? `${(bytes / 1e6).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1e3))} KB`;
}

function isActive(job) {
  return job.status === 'queued' || job.status === 'running';
}

function go(hash) {
  if (location.hash === hash) render();
  else location.hash = hash;
}

function loadDraft() {
  try { return JSON.parse(localStorage.getItem(DRAFT_KEY)) || null; } catch { return null; }
}

function saveDraft(draft) {
  try { localStorage.setItem(DRAFT_KEY, JSON.stringify(draft)); } catch { /* private mode */ }
}

function clearDraft() {
  try { localStorage.removeItem(DRAFT_KEY); } catch { /* private mode */ }
}

// ─── API ────────────────────────────────────────────────────

class ApiError extends Error {
  constructor(status, body) {
    super(body?.error?.title || body?.detail || `Request failed (${status})`);
    this.status = status;
    this.error = body?.error || null;
    this.detail = typeof body?.detail === 'string' ? body.detail : null;
    this.fields = body?.fields || null;
  }
}

async function api(method, path, body) {
  const opts = { method, headers: { 'X-OpenHormozi': '1' } };
  if (body !== undefined) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  }
  let res;
  try {
    res = await fetch(path, opts);
  } catch {
    throw new ApiError(0, { error: { title: 'The app is not responding', message: 'Check that the OpenHormozi window is still running, then reload this page.' } });
  }
  const text = await res.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  if (!res.ok) throw new ApiError(res.status, data && typeof data === 'object' ? data : { detail: data });
  return data;
}

// ─── Toasts ─────────────────────────────────────────────────

function toast({ kind = 'info', title, message = '', actions = [], sticky = false }) {
  const el = document.createElement('div');
  el.className = `toast toast-${kind}`;
  el.setAttribute('role', kind === 'error' ? 'alert' : 'status');
  el.innerHTML = `
    <strong>${esc(title)}</strong>
    <button class="toast-close" aria-label="Dismiss">×</button>
    ${message ? `<p>${esc(message)}</p>` : ''}
    ${actions.length ? `<div class="btn-row">${actions.map((a, i) => `<button class="btn ${i === 0 ? 'btn-primary' : 'btn-quiet'}" data-i="${i}">${esc(a.label)}</button>`).join('')}</div>` : ''}`;
  const close = () => el.remove();
  el.querySelector('.toast-close').onclick = close;
  el.querySelectorAll('[data-i]').forEach(b => {
    b.onclick = () => { actions[Number(b.dataset.i)].run(); close(); };
  });
  toastBox.appendChild(el);
  if (!sticky) setTimeout(close, 7000);
  while (toastBox.children.length > 4) toastBox.firstElementChild.remove();
}

// An error from the API ({code, title, message, action}) becomes a toast with
// the matching action button: open Settings, resume the run, or open a URL.
function errorActions(error, jobId) {
  if (!error?.action) return [];
  if (error.action === 'settings') return [{ label: error.action_label, run: () => go('#/settings') }];
  if (error.action === 'resume') return jobId ? [{ label: error.action_label, run: () => resumeJob(jobId) }] : [];
  if (/^https?:/.test(error.action)) return [{ label: error.action_label, run: () => window.open(error.action, '_blank', 'noopener') }];
  return [];
}

function showError(err, jobId) {
  const e = err.error || {};
  toast({
    kind: 'error',
    title: e.title || err.message,
    message: e.message || err.detail || '',
    actions: errorActions(e, jobId),
    sticky: true,
  });
}

// ─── Shared data ────────────────────────────────────────────

async function refreshSettings() {
  state.settings = await api('GET', '/api/settings');
  const chip = document.getElementById('keystate');
  chip.hidden = false;
  chip.classList.toggle('missing', !state.settings.has_api_key);
  chip.textContent = state.settings.has_api_key ? 'API key ready' : 'Add your API key';
}

async function getSchema() {
  if (!state.schema) state.schema = await api('GET', '/api/schema');
  return state.schema;
}

// Called by the poller: toast every status change seen since the last poll.
function noticeTransitions(jobs) {
  for (const job of jobs) {
    const before = state.statuses.get(job.id);
    state.statuses.set(job.id, job.status);
    if (!before || before === job.status) continue;
    const open = { label: 'Open', run: () => go(`#/job/${job.id}`) };
    if (job.status === 'completed') {
      toast({ kind: 'success', title: 'Strategy ready', message: `${job.name}: ${job.doc_done} documents generated.`, actions: [open] });
    } else if (job.status === 'partial') {
      toast({ kind: 'warn', title: 'Strategy ready, with gaps', message: job.error_detail || '', actions: [open, { label: 'Resume', run: () => resumeJob(job.id) }], sticky: true });
    } else if (job.status === 'failed') {
      const e = job.error || {};
      toast({ kind: 'error', title: e.title || 'Generation stopped', message: e.message || job.error_detail || '', actions: [...errorActions(e, job.id), open], sticky: true });
    } else if (job.status === 'cancelled') {
      toast({ kind: 'info', title: 'Generation cancelled', message: 'Finished documents are kept. Resume any time.' });
    } else if (job.status === 'running' && before === 'queued') {
      toast({ kind: 'info', title: 'Generation started', message: job.name });
    }
  }
}

// ─── Actions ────────────────────────────────────────────────

async function resumeJob(id) {
  try {
    await api('POST', `/api/jobs/${id}/resume`);
    toast({ kind: 'info', title: 'Resuming', message: 'Finished documents are kept; only the missing ones are generated.' });
    await poll();
  } catch (err) { showError(err, id); }
}

async function cancelJob(id) {
  try {
    await api('POST', `/api/jobs/${id}/cancel`);
    toast({ kind: 'info', title: 'Cancelling', message: 'The current document stops within a few seconds.' });
    await poll();
  } catch (err) { showError(err); }
}

async function deleteJob(id, name) {
  if (!window.confirm(`Delete "${name}" and all its documents from this computer?`)) return;
  try {
    await api('DELETE', `/api/jobs/${id}`);
    state.statuses.delete(id);
    toast({ kind: 'info', title: 'Strategy deleted' });
    go('#/');
  } catch (err) { showError(err); }
}

// ─── Strategy list ──────────────────────────────────────────

function progressOf(job) {
  if (!job.doc_total) return job.status === 'completed' ? 1 : 0;
  return job.doc_done / job.doc_total;
}

function jobProgressText(job) {
  if (job.status === 'queued') return 'Waiting to start';
  if (job.error && !isActive(job)) return `${job.doc_done} of ${job.doc_total || '?'} documents. ${job.error.title}.`;
  if (!job.doc_total) return job.status === 'running' ? 'Diagnosing the business' : 'No documents yet';
  return `${job.doc_done} of ${job.doc_total} documents`;
}

function renderList() {
  const jobs = state.jobs || [];
  const s = state.settings;

  if (!jobs.length) {
    view.innerHTML = `
      ${s && !s.has_api_key ? `
        <div class="setup-note">
          <div><strong>First, add your Anthropic API key.</strong><p>OpenHormozi runs on your own Anthropic account. Generation costs go to your key, nothing else is charged.</p></div>
          <a class="btn btn-primary" href="#/settings">Add API key</a>
        </div>` : ''}
      <section class="intro">
        <div>
          <h1>Your whole acquisition strategy from one form.</h1>
          <p class="lede">Answer questions about your business. OpenHormozi diagnoses your real bottleneck with Alex Hormozi's frameworks, then writes your offer, pricing, funnel, sales scripts, channel playbooks and launch roadmap. Everything is generated on this computer with your own Anthropic API key.</p>
          <div class="btn-row">
            <a class="btn btn-primary" href="#/new">Start a strategy</a>
            <a class="btn" href="#/new?example=1">Try the example answers</a>
          </div>
        </div>
        <div class="facts">
          <div class="fact"><div class="display">18 to 31</div><p>documents, picked for your business model and channels</p></div>
          <div class="fact"><div class="display">~40 min</div><p>per strategy, in the background. You can close this tab.</p></div>
          <div class="fact"><div class="display">$5 to $8</div><p>of Anthropic API credit with the default models</p></div>
        </div>
      </section>`;
    return;
  }

  view.innerHTML = `
    <div class="page-head">
      <div>
        <h1>Strategies</h1>
        <p class="muted">Generations run one at a time, in the order you start them.</p>
      </div>
      <a class="btn btn-primary" href="#/new">New strategy</a>
    </div>
    <div class="jobs">
      ${jobs.map(job => `
        <div class="job-row">
          <div>
            <a class="job-name" href="#/job/${job.id}">${esc(job.name)}</a>
            <div class="job-sub">Started ${esc(fmtDate(job.created_at))}</div>
          </div>
          <div>
            <span class="status status-${job.status}">${STATUS_LABEL[job.status] || job.status}</span>
            <div class="bar" aria-hidden="true"><i style="width:${Math.round(progressOf(job) * 100)}%"></i></div>
            <div class="small muted">${esc(job.status === 'running' && job.phase === 'documents' && job.current ? `${jobProgressText(job)}. Writing ${job.current}` : jobProgressText(job))}</div>
          </div>
          <div><span class="cell-label">Cost</span><span class="num">${fmtMoney(job.cost_usd)}</span></div>
          <div><span class="cell-label">Time</span><span class="num">${fmtDuration(job.elapsed_s)}</span></div>
          <div class="actions btn-row">
            ${job.has_zip ? `<a class="btn btn-quiet" href="/api/jobs/${job.id}/download">Download ZIP</a>` : ''}
            ${job.resumable ? `<button class="btn btn-quiet" data-resume="${job.id}">Resume</button>` : ''}
            ${isActive(job) ? `<button class="btn btn-quiet" data-cancel="${job.id}">Cancel</button>` : ''}
          </div>
        </div>`).join('')}
    </div>`;

  view.querySelectorAll('[data-resume]').forEach(b => { b.onclick = () => resumeJob(b.dataset.resume); });
  view.querySelectorAll('[data-cancel]').forEach(b => { b.onclick = () => cancelJob(b.dataset.cancel); });
}

// ─── Strategy page ──────────────────────────────────────────

function tierOf(id) {
  return TIERS.find(t => t.prefix !== 'U' && id.startsWith(t.prefix))?.prefix || 'U';
}

function fileLabel(file) {
  const n = file.name.toLowerCase();
  if (n.includes('_diagram')) return 'Diagram';
  if (n.includes('_chart')) return 'Chart';
  if (n.includes('_render')) return 'Timeline';
  return { pdf: 'PDF', html: 'Web page', png: 'Image', xlsx: 'Spreadsheet' }[file.kind] || file.kind.toUpperCase();
}

function filesFor(job, docId) {
  if (!docId) return [];
  const prefix = docId.toLowerCase() + '_';
  return (job.files || []).filter(f => f.name.toLowerCase().startsWith(prefix));
}

function docRow(job, doc) {
  const files = doc.status === 'done' || doc.status === 'failed' ? filesFor(job, doc.id) : [];
  const mark = { done: '✓', failed: '✕' }[doc.status] || '';
  return `
    <div class="doc ${doc.status}">
      <div class="mark" aria-hidden="true">${mark}</div>
      <div class="id">${esc(doc.id)}</div>
      <div>
        <div class="title"><span>${esc(doc.name)}</span><span class="sr-only">${doc.status === 'running' ? ' (writing now)' : ''}</span></div>
        ${files.length ? `<div class="files">${files.map(f => `<a href="/api/jobs/${job.id}/files/${encodeURIComponent(f.name)}" target="_blank" rel="noopener" title="${esc(f.name)} (${fmtSize(f.size)})">${esc(fileLabel(f))}</a>`).join('')}</div>` : ''}
        ${doc.errors?.length ? `<div class="errs">${doc.errors.map(esc).join('<br>')}</div>` : ''}
      </div>
    </div>`;
}

function jobNotice(job) {
  if (job.status === 'failed' || job.status === 'interrupted') {
    const e = job.error || { title: 'Generation stopped', message: '' };
    return `
      <div class="notice notice-bad">
        <div>
          <strong>${esc(e.title)}</strong>
          <p>${esc(e.message)}</p>
          ${job.error_detail ? `<details><summary>Error details</summary>${esc(job.error_detail)}</details>` : ''}
        </div>
        <div class="btn-row" data-notice-actions></div>
      </div>`;
  }
  if (job.status === 'partial') {
    return `<div class="notice notice-warn"><div><strong>Some documents had errors</strong><p>${esc(job.error_detail || '')}</p></div><button class="btn btn-primary" data-act="resume">Regenerate the missing documents</button></div>`;
  }
  if (job.status === 'cancelled') {
    return `<div class="notice notice-info"><div><strong>Generation cancelled</strong><p>Finished documents are kept. Resume to generate the rest.</p></div><button class="btn btn-primary" data-act="resume">Resume</button></div>`;
  }
  if (job.status === 'queued') {
    const running = (state.jobs || []).find(j => j.status === 'running' && j.id !== job.id);
    return `<div class="notice notice-info"><div><strong>Queued</strong><p>${running ? `Starts when "${esc(running.name)}" finishes.` : 'Starting in a moment.'}</p></div></div>`;
  }
  return '';
}

function renderJob(job) {
  const pct = Math.round(progressOf(job) * 100);
  const diagStatus = job.docs.length ? 'done'
    : job.status === 'running' ? 'running'
    : (job.status === 'failed' || job.status === 'interrupted') && job.attempts ? 'failed' : 'pending';

  const groups = TIERS.map(t => ({ ...t, docs: job.docs.filter(d => tierOf(d.id) === t.prefix) })).filter(g => g.docs.length);

  const now = job.status === 'running'
    ? job.phase === 'diagnostic' ? 'Diagnosing your business'
      : job.phase === 'packaging' ? 'Packaging the ZIP'
      : job.current ? `Writing <b>${esc(job.current)}</b>` : 'Starting'
    : job.status === 'completed' ? `Finished ${esc(fmtDate(job.finished_at))}` : '';

  view.innerHTML = `
    <a class="back" href="#/">All strategies</a>
    <div class="page-head">
      <div>
        ${state.ui.renaming ? `
          <form class="rename" data-rename>
            <label class="sr-only" for="rename-input">Strategy name</label>
            <input id="rename-input" type="text" value="${esc(job.name)}" maxlength="80" required>
            <button class="btn btn-primary" type="submit">Save name</button>
            <button class="btn btn-quiet" type="button" data-act="rename-cancel">Cancel</button>
          </form>` : `<h1>${esc(job.name)}</h1>`}
        <p><span class="status status-${job.status}">${STATUS_LABEL[job.status] || job.status}</span>
           <span class="muted small">&nbsp; Started ${esc(fmtDate(job.created_at))}${job.attempts > 1 ? `, ${job.attempts} attempts` : ''}</span></p>
      </div>
    </div>

    ${jobNotice(job)}

    <div class="scoreboard">
      <div class="score"><div class="display">${job.doc_done}<small> / ${job.doc_total || '?'}</small></div><p>documents written</p></div>
      <div class="score"><div class="display">${fmtDuration(job.elapsed_s)}</div><p>generation time</p></div>
      <div class="score"><div class="display">${fmtMoney(job.cost_usd)}</div><p>${isActive(job) ? 'API cost so far' : 'API cost'}</p></div>
    </div>
    <div class="bar big" aria-label="${pct}% done"><i style="width:${pct}%"></i></div>
    <p class="now">${now}</p>

    <div class="job-layout">
      <div>
        <div class="sheet-group">
          <h3>Diagnostic</h3>
          ${docRow(job, { id: '', name: diagStatus === 'running' ? 'Reading your answers and finding the bottleneck' : 'Business diagnostic and document plan', status: diagStatus })}
        </div>
        ${groups.length ? groups.map(g => `
          <div class="sheet-group">
            <h3>${esc(g.title)}</h3>
            ${g.docs.map(d => docRow(job, d)).join('')}
          </div>`).join('') : `
          <div class="waiting">
            <h3>The document plan comes after the diagnostic</h3>
            <p class="muted">The diagnostic decides which of the 31 documents your business needs. It usually takes 3 to 6 minutes.</p>
          </div>`}
      </div>

      <aside class="side">
        <h3>Your files</h3>
        <p>${job.has_zip ? 'Everything in one archive, sorted into folders. Start with 0_START_HERE.pdf.' : 'The ZIP appears when the generation finishes. Finished documents open from the list as they arrive.'}</p>
        ${job.has_zip ? `<a class="btn btn-primary" href="/api/jobs/${job.id}/download">Download ZIP</a>` : ''}
        ${job.resumable ? `<button class="btn" data-act="resume">Resume</button>` : ''}
        ${isActive(job) ? `<button class="btn" data-act="cancel">Cancel generation</button>` : ''}
        <button class="btn btn-quiet" data-act="duplicate">Edit answers and run again</button>
        <button class="btn btn-quiet" data-act="rename">Rename</button>
        ${!isActive(job) ? `<button class="btn btn-danger" data-act="delete">Delete</button>` : ''}
      </aside>
    </div>

    <details class="log" ${state.ui.logOpen ? 'open' : ''}>
      <summary>Run log</summary>
      <pre id="log">${esc(state.ui.log || 'Loading…')}</pre>
    </details>`;

  const holder = view.querySelector('[data-notice-actions]');
  if (holder && job.error) {
    const acts = errorActions(job.error, job.id);
    if (job.resumable && job.error.action !== 'resume') acts.push({ label: 'Resume', run: () => resumeJob(job.id) });
    acts.forEach((a, i) => {
      const b = document.createElement('button');
      b.className = `btn ${i === 0 ? 'btn-primary' : ''}`;
      b.textContent = a.label;
      b.onclick = a.run;
      holder.appendChild(b);
    });
  }

  view.querySelectorAll('[data-act]').forEach(b => {
    b.onclick = () => {
      const act = b.dataset.act;
      if (act === 'resume') resumeJob(job.id);
      else if (act === 'cancel') cancelJob(job.id);
      else if (act === 'delete') deleteJob(job.id, job.name);
      else if (act === 'duplicate') go(`#/new?from=${job.id}`);
      else if (act === 'rename') { state.ui.renaming = true; renderJob(job); view.querySelector('#rename-input')?.focus(); }
      else if (act === 'rename-cancel') { state.ui.renaming = false; renderJob(job); }
    };
  });

  const form = view.querySelector('[data-rename]');
  if (form) {
    form.onsubmit = async ev => {
      ev.preventDefault();
      try {
        await api('PATCH', `/api/jobs/${job.id}`, { name: form.querySelector('input').value });
        state.ui.renaming = false;
        toast({ kind: 'success', title: 'Name saved' });
        await refreshJobView(job.id);
      } catch (err) { showError(err); }
    };
  }

  const details = view.querySelector('details.log');
  details.ontoggle = () => {
    state.ui.logOpen = details.open;
    if (details.open) refreshLog(job.id);
  };
}

async function refreshLog(id) {
  try {
    state.ui.log = await api('GET', `/api/jobs/${id}/log?lines=300`) || 'Nothing logged yet.';
  } catch { state.ui.log = 'The log could not be loaded.'; }
  const pre = document.getElementById('log');
  if (pre) {
    const atBottom = pre.scrollTop + pre.clientHeight >= pre.scrollHeight - 8;
    pre.textContent = state.ui.log;
    if (atBottom) pre.scrollTop = pre.scrollHeight;
  }
}

async function refreshJobView(id) {
  const job = await api('GET', `/api/jobs/${id}`);
  if (state.route?.name !== 'job' || state.route.id !== id) return;
  if (!state.ui.renaming) renderJob(job);
  if (state.ui.logOpen) refreshLog(id);
}

// ─── New strategy form ──────────────────────────────────────

const F = { answers: {}, step: 1, name: '', errors: {} };

function questionsOf(step) {
  return state.schema.questions.filter(q => q.step === step);
}

function hasAnswer(v) {
  if (Array.isArray(v)) return v.length > 0;
  return v !== undefined && v !== null && String(v).trim() !== '';
}

// Same rules as the server's parser (engine/form/parser.py).
function isVisible(q) {
  if (!q.conditional_on) return true;
  return Object.entries(q.conditional_on).every(([dep, required]) => {
    const val = F.answers[dep];
    if (required === '__multiple') return Array.isArray(val) && val.length > 1;
    if (Array.isArray(val)) return val.some(v => required.includes(v));
    return required.includes(val);
  });
}

function optionsFor(q) {
  if (!q.dynamic_from) return q.options;
  const src = state.schema.questions.find(x => x.id === q.dynamic_from);
  const picked = F.answers[q.dynamic_from] || [];
  return src.options.filter(o => picked.includes(o.value));
}

function persist() {
  saveDraft({ answers: F.answers, step: F.step, name: F.name });
}

function questionHtml(q) {
  const val = F.answers[q.id];
  const err = F.errors[q.id];
  const optional = q.required ? '' : '<span class="opt">Optional</span>';
  let control = '';
  if (q.type === 'dropdown') {
    control = `<select id="in-${q.id}" data-q="${q.id}">
      <option value="">Choose one</option>
      ${optionsFor(q).map(o => `<option value="${esc(o.value)}"${o.value === val ? ' selected' : ''}>${esc(o.label)}</option>`).join('')}
    </select>`;
  } else if (q.type === 'radio' || q.type === 'checkbox') {
    const multi = q.type === 'checkbox';
    const picked = multi ? (val || []) : [val];
    control = `<div class="choices" role="${multi ? 'group' : 'radiogroup'}" aria-labelledby="lbl-${q.id}">
      ${optionsFor(q).map((o, i) => `
        <label class="choice">
          <input type="${multi ? 'checkbox' : 'radio'}" name="${q.id}" value="${esc(o.value)}" data-q="${q.id}" id="in-${q.id}-${i}"${picked.includes(o.value) ? ' checked' : ''}>
          <span>${esc(o.label)}</span>
        </label>`).join('')}
    </div>`;
  } else if (q.type === 'textarea') {
    const len = (val || '').trim().length;
    control = `<textarea id="in-${q.id}" data-q="${q.id}" rows="4">${esc(val || '')}</textarea>
      ${q.min_length ? `<div class="counter ${len >= q.min_length ? 'ok' : ''}" data-counter="${q.id}">${len} characters. Aim for ${q.min_length} or more; detail makes the strategy sharper.</div>` : ''}`;
  } else {
    control = `<input type="text" id="in-${q.id}" data-q="${q.id}" value="${esc(val || '')}">`;
  }
  const forAttr = q.type === 'radio' || q.type === 'checkbox' ? '' : ` for="in-${q.id}"`;
  return `
    <div class="q ${err ? 'invalid' : ''}" id="q-${q.id}" ${isVisible(q) ? '' : 'hidden'}>
      <label class="q-label" id="lbl-${q.id}"${forAttr}>${esc(q.text)}${optional}</label>
      ${control}
      ${err ? `<div class="q-error">${esc(err)}</div>` : ''}
    </div>`;
}

function renderForm() {
  const steps = state.schema.steps;
  const total = steps.length;
  const step = steps[F.step - 1];
  const last = F.step === total;

  const stepDone = n => questionsOf(n).filter(isVisible).every(q => !q.required || hasAnswer(F.answers[q.id]));

  view.innerHTML = `
    <div class="page-head">
      <div>
        <h1>New strategy</h1>
        <p class="muted">About 10 minutes. Your answers are saved in this browser as you go.</p>
      </div>
      <div class="form-tools">
        <button class="btn-link" data-tool="example">Fill with example answers</button>
        <button class="btn-link" data-tool="clear">Clear all answers</button>
      </div>
    </div>
    <div class="wizard">
      <ol class="steps">
        ${steps.map((s, i) => {
          const n = i + 1;
          const cls = n === F.step ? 'current' : stepDone(n) ? 'done' : '';
          return `<li class="${cls}"><button data-step="${n}" ${n === F.step ? 'aria-current="step"' : ''}>${esc(s.title)}<small>Step ${n} of ${total}</small></button></li>`;
        }).join('')}
      </ol>
      <form id="qform" novalidate>
        <div class="step-head">
          <div class="step-count">Step ${F.step} of ${total}</div>
          <h2>${esc(step.title)}</h2>
          <p>${esc(step.subtitle)}</p>
        </div>
        ${questionsOf(F.step).map(questionHtml).join('')}
        ${last ? `
          <div class="q">
            <label class="q-label" for="job-name">Name this strategy<span class="opt">Optional</span></label>
            <input type="text" id="job-name" maxlength="80" value="${esc(F.name)}" placeholder="Defaults to your industry">
          </div>` : ''}
        <div class="form-nav">
          ${F.step > 1 ? '<button type="button" class="btn btn-quiet" data-nav-step="back">Back</button>' : '<span></span>'}
          <button type="submit" class="btn btn-primary">${last ? 'Generate my strategy' : 'Continue'}</button>
        </div>
      </form>
    </div>`;

  bindForm();
}

function onAnswerChanged(qid) {
  // Hide (and clear) questions whose condition no longer holds, refresh Q24's options.
  let changed = true;
  while (changed) {
    changed = false;
    for (const q of state.schema.questions) {
      if (!isVisible(q) && F.answers[q.id] !== undefined) { delete F.answers[q.id]; changed = true; }
    }
  }
  for (const q of state.schema.questions) {
    if (q.dynamic_from === qid) {
      const allowed = optionsFor(q).map(o => o.value);
      if (F.answers[q.id] && !allowed.includes(F.answers[q.id])) delete F.answers[q.id];
    }
  }
  delete F.errors[qid];
  persist();
  for (const q of questionsOf(F.step)) {
    const el = document.getElementById(`q-${q.id}`);
    if (!el) continue;
    const visible = isVisible(q);
    if (q.dynamic_from === qid || (visible && el.hidden)) {
      el.outerHTML = questionHtml(q);
    } else {
      el.hidden = !visible;
    }
  }
  bindInputs();
}

function bindInputs() {
  view.querySelectorAll('[data-q]').forEach(el => {
    if (el.dataset.bound) return;
    el.dataset.bound = '1';
    const qid = el.dataset.q;
    const q = state.schema.questions.find(x => x.id === qid);
    if (el.type === 'checkbox') {
      el.onchange = () => {
        F.answers[qid] = [...view.querySelectorAll(`input[name="${qid}"]:checked`)].map(c => c.value);
        if (!F.answers[qid].length) delete F.answers[qid];
        onAnswerChanged(qid);
      };
    } else if (el.type === 'radio' || el.tagName === 'SELECT') {
      el.onchange = () => {
        if (el.value) F.answers[qid] = el.value; else delete F.answers[qid];
        onAnswerChanged(qid);
      };
    } else {
      el.oninput = () => {
        if (el.value.trim()) F.answers[qid] = el.value; else delete F.answers[qid];
        const counter = view.querySelector(`[data-counter="${qid}"]`);
        if (counter && q.min_length) {
          const len = el.value.trim().length;
          counter.textContent = `${len} characters. Aim for ${q.min_length} or more; detail makes the strategy sharper.`;
          counter.classList.toggle('ok', len >= q.min_length);
        }
        persist();
      };
      el.onchange = () => onAnswerChanged(qid);
    }
  });
}

function bindForm() {
  bindInputs();
  const form = document.getElementById('qform');

  view.querySelectorAll('[data-step]').forEach(b => {
    b.onclick = () => { F.step = Number(b.dataset.step); persist(); renderForm(); window.scrollTo(0, 0); };
  });
  view.querySelector('[data-nav-step="back"]')?.addEventListener('click', () => {
    F.step -= 1; persist(); renderForm(); window.scrollTo(0, 0);
  });
  view.querySelector('[data-tool="example"]').onclick = async () => {
    if (Object.keys(F.answers).length && !window.confirm('Replace your current answers with the example business?')) return;
    try {
      F.answers = await api('GET', '/api/example');
      F.name = 'Example: e-commerce bookkeeping';
      F.errors = {};
      persist();
      renderForm();
      toast({ kind: 'info', title: 'Example answers loaded', message: 'A fictional bookkeeping firm. Edit anything, or go to the last step and generate.' });
    } catch (err) { showError(err); }
  };
  view.querySelector('[data-tool="clear"]').onclick = () => {
    if (!window.confirm('Clear every answer in this form?')) return;
    F.answers = {}; F.errors = {}; F.name = ''; F.step = 1;
    clearDraft();
    renderForm();
  };
  const nameInput = document.getElementById('job-name');
  if (nameInput) nameInput.oninput = () => { F.name = nameInput.value; persist(); };

  form.onsubmit = async ev => {
    ev.preventDefault();
    const missing = questionsOf(F.step).filter(q => isVisible(q) && q.required && !hasAnswer(F.answers[q.id]));
    missing.forEach(q => { F.errors[q.id] = 'Answer this to continue.'; });
    if (missing.length) {
      renderForm();
      document.getElementById(`q-${missing[0].id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
    if (F.step < state.schema.steps.length) {
      F.step += 1; persist(); renderForm(); window.scrollTo(0, 0);
      return;
    }
    await submitForm(form.querySelector('[type="submit"]'));
  };
}

async function submitForm(button) {
  // Only send answers to questions that are visible, like the server expects.
  const answers = {};
  for (const q of state.schema.questions) {
    if (isVisible(q) && hasAnswer(F.answers[q.id])) answers[q.id] = F.answers[q.id];
  }
  button.disabled = true;
  button.textContent = 'Starting…';
  try {
    const job = await api('POST', '/api/jobs', { form: answers, name: F.name || null });
    clearDraft();
    Object.assign(F, { answers: {}, step: 1, name: '', errors: {} });
    state.statuses.set(job.id, job.status);
    toast({ kind: 'success', title: 'Strategy queued', message: 'It runs in the background. You can close this tab and come back later.' });
    go(`#/job/${job.id}`);
  } catch (err) {
    button.disabled = false;
    button.textContent = 'Generate my strategy';
    if (err.fields) {
      F.errors = Object.fromEntries(Object.entries(err.fields).map(([k, v]) => [k, v]));
      const first = state.schema.questions.find(q => F.errors[q.id]);
      if (first) F.step = first.step;
      renderForm();
      toast({ kind: 'error', title: err.error.title, message: err.error.message });
    } else {
      showError(err);
    }
  }
}

async function openForm(params) {
  await getSchema();
  const fromId = params.get('from');
  if (fromId) {
    try {
      const job = await api('GET', `/api/jobs/${fromId}`);
      Object.assign(F, { answers: { ...job.form }, step: 1, name: `${job.name} (v2)`.slice(0, 80), errors: {} });
      persist();
    } catch (err) { showError(err); }
    history.replaceState(null, '', '#/new');
  } else if (params.get('example')) {
    F.answers = await api('GET', '/api/example');
    F.name = 'Example: e-commerce bookkeeping';
    F.step = 1;
    F.errors = {};
    persist();
    history.replaceState(null, '', '#/new');
  } else {
    const draft = loadDraft();
    Object.assign(F, { answers: draft?.answers || {}, step: draft?.step || 1, name: draft?.name || '', errors: {} });
  }
  renderForm();
}

// ─── Settings ───────────────────────────────────────────────

function renderSettings() {
  const s = state.settings;
  const source = { settings: 'Saved in OpenHormozi', environment: 'Read from the ANTHROPIC_API_KEY environment variable' }[s.api_key_source] || '';
  view.innerHTML = `
    <div class="page-head"><div><h1>Settings</h1></div></div>
    <div class="settings">
      <section>
        <h2>Anthropic API key</h2>
        <p class="key-status">${s.has_api_key ? `Key ${esc(s.api_key_hint)}. ${esc(source)}.` : 'No key yet. Generation needs one.'}</p>
        <form class="field" id="key-form">
          <label for="api-key">${s.has_api_key ? 'Replace the key' : 'Paste your key'}</label>
          <div class="key-input">
            <input type="password" id="api-key" placeholder="sk-ant-…" autocomplete="off" spellcheck="false">
            <button type="button" class="btn btn-quiet" id="toggle-key">Show</button>
          </div>
          <p class="help">Create one in the <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener">Anthropic Console</a>. It is stored in <code>data/settings.json</code> on this computer and only ever sent to Anthropic.</p>
          <div class="btn-row field">
            <button type="submit" class="btn btn-primary">Save key</button>
            <button type="button" class="btn" id="test-key">Test key</button>
            ${s.api_key_source === 'settings' ? '<button type="button" class="btn btn-danger" id="remove-key">Remove saved key</button>' : ''}
          </div>
        </form>
      </section>
      <section>
        <h2>Models</h2>
        <p class="help">The defaults balance quality and cost: a full strategy costs about $5 to $8. Stronger models raise both.</p>
        <form id="models-form">
          ${s.roles.map(r => `
            <div class="field">
              <label for="model-${r.id}">${esc(r.label)}</label>
              <select id="model-${r.id}" data-role="${r.id}">
                ${modelOptions(s, s.models[r.id])}
              </select>
              <p class="help">${esc(r.help)}</p>
            </div>`).join('')}
          <div class="btn-row field"><button type="submit" class="btn btn-primary">Save models</button></div>
        </form>
      </section>
    </div>`;

  const keyInput = document.getElementById('api-key');
  document.getElementById('toggle-key').onclick = ev => {
    keyInput.type = keyInput.type === 'password' ? 'text' : 'password';
    ev.target.textContent = keyInput.type === 'password' ? 'Show' : 'Hide';
  };
  document.getElementById('key-form').onsubmit = async ev => {
    ev.preventDefault();
    const key = keyInput.value.trim();
    if (!key) { keyInput.focus(); return; }
    try {
      await api('PUT', '/api/settings', { api_key: key });
      await refreshSettings();
      toast({ kind: 'success', title: 'Key saved', message: 'Use "Test key" to check it has credit.' });
      renderSettings();
    } catch (err) { showError(err); }
  };
  document.getElementById('test-key').onclick = async ev => {
    const btn = ev.target;
    btn.disabled = true; btn.textContent = 'Testing…';
    try {
      await api('POST', '/api/settings/test', { api_key: keyInput.value.trim() || null });
      toast({ kind: 'success', title: 'Key works', message: 'Anthropic accepted the key and the account can make requests.' });
    } catch (err) { showError(err); }
    btn.disabled = false; btn.textContent = 'Test key';
  };
  document.getElementById('remove-key')?.addEventListener('click', async () => {
    if (!window.confirm('Remove the saved API key from this computer?')) return;
    try {
      await api('PUT', '/api/settings', { clear_api_key: true });
      await refreshSettings();
      toast({ kind: 'info', title: 'Saved key removed' });
      renderSettings();
    } catch (err) { showError(err); }
  });
  document.getElementById('models-form').onsubmit = async ev => {
    ev.preventDefault();
    const models = {};
    view.querySelectorAll('[data-role]').forEach(sel => { models[sel.dataset.role] = sel.value; });
    try {
      await api('PUT', '/api/settings', { models });
      await refreshSettings();
      toast({ kind: 'success', title: 'Models saved', message: 'They apply to the next generation you start or resume.' });
    } catch (err) { showError(err); }
  };
}

function modelOptions(s, current) {
  const known = s.available_models.some(m => m.id === current);
  const extra = !known && current ? `<option value="${esc(current)}" selected>${esc(current)} (from config.yaml)</option>` : '';
  return extra + s.available_models.map(m =>
    `<option value="${esc(m.id)}"${m.id === current ? ' selected' : ''}>${esc(m.label)}, ${esc(m.price)}</option>`).join('');
}

// ─── Router and polling ─────────────────────────────────────

function parseRoute() {
  const [path, query] = (location.hash.slice(1) || '/').split('?');
  const params = new URLSearchParams(query || '');
  const m = path.match(/^\/job\/([a-z0-9]+)$/);
  if (m) return { name: 'job', id: m[1], params };
  if (path === '/new') return { name: 'new', params };
  if (path === '/settings') return { name: 'settings', params };
  return { name: 'list', params };
}

async function render() {
  const route = parseRoute();
  const changed = state.route?.name !== route.name || state.route?.id !== route.id;
  state.route = route;
  if (changed) state.ui = { renaming: false, logOpen: false, log: '' };

  document.querySelectorAll('.nav a').forEach(a => {
    if (a.dataset.nav === route.name) a.setAttribute('aria-current', 'page');
    else a.removeAttribute('aria-current');
  });

  try {
    if (route.name === 'list') {
      if (!state.jobs) state.jobs = await api('GET', '/api/jobs');
      renderList();
    } else if (route.name === 'new') {
      await openForm(route.params);
    } else if (route.name === 'settings') {
      await refreshSettings();
      renderSettings();
    } else if (route.name === 'job') {
      await refreshJobView(route.id);
    }
  } catch (err) {
    if (err.status === 404) {
      view.innerHTML = '<h1>Not found</h1><p class="muted" style="margin-top:12px">This strategy was deleted or never existed. <a href="#/">Back to strategies</a></p>';
    } else {
      showError(err);
    }
  }
  if (changed) { window.scrollTo(0, 0); view.focus({ preventScroll: true }); }
}

async function poll() {
  try {
    const jobs = await api('GET', '/api/jobs');
    noticeTransitions(jobs);
    state.jobs = jobs;
    if (state.route?.name === 'list') renderList();
    if (state.route?.name === 'job') await refreshJobView(state.route.id);
  } catch { /* the server may be restarting; the next poll retries */ }
}

async function start() {
  try { await refreshSettings(); } catch (err) { showError(err); }
  try {
    state.jobs = await api('GET', '/api/jobs');
    state.jobs.forEach(j => state.statuses.set(j.id, j.status));
  } catch { /* shown by render */ }
  window.addEventListener('hashchange', render);
  await render();
  setInterval(() => {
    // Poll fast while something is generating, slowly otherwise.
    const busy = (state.jobs || []).some(isActive);
    if (busy || Date.now() - (start.lastIdlePoll || 0) > 15000) {
      start.lastIdlePoll = Date.now();
      poll();
    }
  }, 2500);
}

start();
