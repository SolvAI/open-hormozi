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
  ui: { renaming: false, logOpen: false, log: '', menuOpen: false, sig: '' },
  views: new Map(),      // "jobId:docId" → index of the view shown in that card
  cards: new Map(),      // "jobId:docId" → { sig, el }, so polling never reloads previews
  readerSig: '',         // what the reader shows, so polling doesn't reload it
  readerPushed: false,   // the reader was opened from the strategy page
  readerReturn: null,    // element to focus again when the reader closes
};

const TIERS = [
  { prefix: 'U', title: 'Strategy', blurb: 'The foundation. Every other document builds on these.' },
  { prefix: 'CH', title: 'Acquisition channels', blurb: 'Where the next clients come from, picked for this business.' },
  { prefix: 'FC', title: 'Funnel', blurb: 'The path from first click to a booked call or a sale.' },
  { prefix: 'BM', title: 'Sales and operations', blurb: 'Closing, delivering and keeping clients.' },
  { prefix: 'MT', title: 'Proof and tools', blurb: 'Credibility, and the systems that run in the background.' },
];

// Name and one-line summary of every document the engine can write.
const DOC_INFO = {
  U1: ['Diagnostic Report', 'Where the business stands, the bottleneck that limits growth, and the priorities ranked by impact.'],
  U2: ['Avatar & ICP', 'Who buys, what pushes them to buy now, where to find them and the words they use.'],
  U3: ['Grand Slam Offer', 'The offer stack, its name, bonuses and guarantee, built on the Value Equation.'],
  U4: ['Pricing & Packaging', 'Price tiers, anchoring and the comparison table, with a calculator to test the numbers.'],
  U5: ['Positioning & Messaging', 'How you differ from the alternatives, the angles to lead with, and where you sit on the map.'],
  U6: ['Sales Funnel Blueprint', 'Every step from first contact to paying client, with the automations in between.'],
  U7: ['Financial Model', 'Revenue projections, break-even, acquisition cost against lifetime value.'],
  U8: ['KPI & Tracking Framework', 'The numbers to watch at each stage, how to track them and when to act on them.'],
  U9: ['Launch Roadmap', 'Week by week actions with milestones and dependencies.'],
  CH1: ['SEA Strategy (Google Ads)', 'Keywords, campaign structure, ad copy, bids and budget, with a keyword sheet.'],
  CH2: ['Social Ads Strategy', 'Platform choice, targeting, creative briefs and budget.'],
  CH3: ['Cold Outbound Playbook', 'Target lists, email and LinkedIn sequences, and call scripts.'],
  CH4: ['Organic Content Strategy', 'Content pillars, a publishing calendar and how to reuse each piece.'],
  CH5: ['Local SEO & Maps Strategy', 'Google Business Profile, directories, reviews and local pages.'],
  CH6: ['Referral & Partnership Strategy', 'Partner profiles, incentives and the messages that recruit them.'],
  CH7: ['Marketplace Strategy', 'Which platform to list on, how to write the listing and how to price it.'],
  FC1: ['Landing Page', 'Conversion copy section by section, plus a ready-to-edit HTML page.'],
  FC2: ['Lead Magnet', 'Topic, outline and delivery, plus the lead magnet itself as a PDF.'],
  FC3: ['Webinar / VSL Script', 'A complete script: hook, teaching, offer and close.'],
  FC4: ['Email Sequences', 'Every nurture, follow-up and onboarding email written out, with a map of the sequences.'],
  FC5: ['Retargeting Strategy', 'Audiences, creatives, budget and frequency caps.'],
  BM1: ['Sales Playbook', 'Discovery call script, objection handling and how to present the proposal.'],
  BM2: ['Booking & Scheduling Flow', 'Booking setup, reminders and no-show recovery.'],
  BM3: ['Local Visibility Baseline', 'Foot traffic, signage and neighborhood partnerships.'],
  BM4: ['On-Site Experience & Upsell', 'Customer touchpoints, staff scripts and upsells, with a staff cheat sheet.'],
  BM5: ['Retention, Loyalty & Referral Playbook', 'Loyalty mechanics, rewards and a referral program clients actually use.'],
  BM6: ['Client Operations Playbook', 'Onboarding, scope, contracts and the rhythm of client communication.'],
  BM7: ['Online Purchase Optimization', 'Product pages, checkout and cart recovery, with a page audit checklist.'],
  MT1: ['Proof & Credibility Kit', 'Case study formats, testimonial scripts and the proof to collect first.'],
  MT2: ['Proof Generation Plan', 'How to ask for reviews and turn client wins into case studies.'],
  MT3: ['Automation & Tech Stack Guide', 'The tools to use, the setup checklist and the automations to build.'],
};

// What each document's companion files are called on its card.
const VISUAL_LABEL = {
  U2: 'Persona card', U4: 'Pricing table', U5: 'Positioning map', BM4: 'Staff cheat sheet',
  BM5: 'Loyalty card', BM7: 'Page wireframe', CH1: 'Ad preview', CH2: 'Ad mockups',
  FC5: 'Retargeting ads', MT1: 'Case studies',
};
const RENDER_LABEL = {
  U9: 'Roadmap', FC1: 'Landing page', FC2: 'Lead magnet', FC4: 'Email preview', BM7: 'Audit checklist',
};
// Cards open on their most visual view, then the report. The Value Equation
// image is the same for everyone, so it comes after the report.
const VIEW_RANK = { render: 0, visual: 1, chart: 1, report: 2, diagram: 3, value: 3, sheet: 4 };

const BOTTLENECK = {
  visibility: 'Visibility', lead_generation: 'Lead generation', conversion: 'Conversion',
  pricing: 'Pricing', retention: 'Retention', wrong_clients: 'Wrong clients',
};
const MATURITY = { STARTER: 'Starting out', GROWING: 'Growing', ESTABLISHED: 'Established', PIVOT: 'Pivoting' };
const CHANNEL = {
  CH1: 'Google Ads', CH2: 'Social ads', CH3: 'Cold outbound', CH4: 'Organic content',
  CH5: 'Local SEO', CH6: 'Referrals and partners', CH7: 'Marketplaces',
};

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

function icon(name) {
  return `<svg class="i" aria-hidden="true"><use href="#i-${name}"/></svg>`;
}

function fmtMoney(usd) {
  return '$' + (usd || 0).toFixed(usd >= 100 ? 0 : 2);
}

function fmtDuration(seconds) {
  const s = Math.max(0, Math.round(seconds || 0));
  if (s < 60) return `${s} s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m} min`;
  return `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, '0')}`;
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

function fileUrl(job, file) {
  return `/api/jobs/${job.id}/files/${encodeURIComponent(file.name)}?v=${file.v}`;
}

function previewUrl(job, file, part) {
  return `/api/jobs/${job.id}/previews/${encodeURIComponent(file.name)}/${part}?v=${file.v}`;
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
    ${actions.length ? `<div class="btn-row">${actions.map((a, i) => `<button class="btn ${i === 0 ? 'btn-primary' : ''}" data-i="${i}">${esc(a.label)}</button>`).join('')}</div>` : ''}`;
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

// Images fade in once loaded. Tall diagrams start at the top, at a readable
// size, and run off the bottom edge. A preview that can't be rendered leaves a note.
function wireImages(root) {
  root.querySelectorAll('.slide img, .job-cover img').forEach(img => {
    const loaded = () => {
      img.classList.add('is-loaded');
      const slide = img.closest('.slide-image');
      if (slide && img.naturalHeight > img.naturalWidth * 1.15) slide.classList.add('is-tall');
    };
    const failed = () => {
      const slide = img.closest('.slide');
      if (slide) slide.outerHTML = '<div class="slide slide-empty">No preview for this file. Open it with the buttons below.</div>';
      else img.remove();
    };
    if (img.complete && img.naturalWidth) loaded();
    else {
      img.addEventListener('load', loaded, { once: true });
      img.addEventListener('error', failed, { once: true });
    }
  });
}

function ghostHtml(label) {
  return `<div class="slide"><div class="ghost"><i></i><i></i><i></i><i></i><i></i><i></i></div>${label ? `<span class="ghost-label">${esc(label)}</span>` : ''}</div>`;
}

// ─── Strategy list ──────────────────────────────────────────

function progressOf(job) {
  if (!job.doc_total) return job.status === 'completed' ? 1 : 0;
  return job.doc_done / job.doc_total;
}

function jobProgressText(job) {
  if (job.status === 'queued') return 'Waiting to start';
  if (job.error && !isActive(job)) return job.error.title;
  if (!job.doc_total) return job.status === 'running' ? 'Diagnosing the business' : 'No documents yet';
  if (job.status === 'running' && job.phase === 'documents' && job.current) return `Writing ${job.current}`;
  if (job.status === 'running' && job.phase === 'packaging') return 'Packaging the ZIP';
  return job.finished_at ? `${endVerb(job)} ${fmtDate(job.finished_at)}` : '';
}

function endVerb(job) {
  return { cancelled: 'Cancelled', failed: 'Stopped', interrupted: 'Stopped' }[job.status] || 'Finished';
}

// The parts of a job that change every poll while it runs. They are patched in
// place so the page (and its images) isn't rebuilt every few seconds.
function liveFree(job) {
  const { elapsed_s, cost_usd, ...rest } = job;
  return rest;
}

function patchLive(job) {
  view.querySelectorAll(`[data-live$=":${job.id}"]`).forEach(el => {
    const what = el.dataset.live.split(':')[0];
    if (what === 'elapsed') el.textContent = fmtDuration(job.elapsed_s);
    if (what === 'cost') el.textContent = fmtMoney(job.cost_usd);
  });
}

function coverHtml(job) {
  const thumbs = job.thumbs || [];
  if (!thumbs.length) {
    const label = job.status === 'running' ? 'Writing now' : job.status === 'queued' ? 'Queued' : '';
    return `<a class="job-cover empty ${job.status === 'running' ? 'is-running' : ''}" href="#/job/${job.id}" tabindex="-1" aria-hidden="true" style="position:relative">${ghostHtml(label)}</a>`;
  }
  return `<a class="job-cover n${thumbs.length}" href="#/job/${job.id}" tabindex="-1" aria-hidden="true">
    ${thumbs.map(t => `<img alt="" loading="lazy" src="/api/jobs/${job.id}/files/${encodeURIComponent(t.name)}?v=${t.v}">`).join('')}
  </a>`;
}

function renderList() {
  const jobs = state.jobs || [];
  const s = state.settings;
  const sig = JSON.stringify(['list', jobs.map(liveFree), !!s?.has_api_key]);
  if (sig === state.ui.sig) { jobs.forEach(patchLive); return; }
  state.ui.sig = sig;

  if (!jobs.length) {
    view.innerHTML = `
      <section class="band"><div class="wrap">
        ${s && !s.has_api_key ? `
          <div class="setup-note">
            <div><strong>First, add your Anthropic API key.</strong><p>OpenHormozi runs on your own Anthropic account. Generation costs go to your key; nothing else is charged.</p></div>
            <a class="btn" href="#/settings">${icon('key')}Add API key</a>
          </div>` : ''}
        <div class="intro">
          <div>
            <h1>Your whole acquisition strategy from one form.</h1>
            <p class="lede">Answer questions about your business. OpenHormozi diagnoses your real bottleneck with Alex Hormozi's frameworks, then writes your offer, pricing, funnel, sales scripts, channel playbooks and launch roadmap. Everything runs on this computer with your own Anthropic API key.</p>
            <div class="btn-row">
              <a class="btn btn-primary" href="#/new">${icon('plus')}Start a strategy</a>
              <a class="btn" href="#/new?example=1">Try the example answers</a>
            </div>
          </div>
          <dl class="intro-facts">
            <div><dt>18 to 31 documents</dt><dd>Picked for your business model and channels.</dd></div>
            <div><dt>25 to 40 minutes</dt><dd>In the background. You can close this tab.</dd></div>
            <div><dt>$3 to $8 per strategy</dt><dd>Of Anthropic API credit with the default models.</dd></div>
          </dl>
        </div>
      </div></section>
      <div class="wrap page">
        <div class="section-head">
          <h2>Everything it can write</h2>
          <p>The diagnostic keeps the documents your business needs.</p>
        </div>
        <div class="library">
          ${TIERS.map(t => `
            <div>
              <h3>${esc(t.title)}</h3>
              <ul>${Object.entries(DOC_INFO).filter(([id]) => tierOf(id) === t.prefix).map(([, [name]]) => `<li>${esc(name)}</li>`).join('')}</ul>
            </div>`).join('')}
        </div>
      </div>`;
    return;
  }

  view.innerHTML = `
    <section class="band"><div class="wrap band-head">
      <div>
        <h1>Strategies</h1>
        <p>Generations run one at a time, in the order you start them. Everything stays in the data folder on this computer.</p>
      </div>
      <a class="btn btn-primary" href="#/new">${icon('plus')}New strategy</a>
    </div></section>
    <div class="wrap page">
      <div class="job-grid">
        ${jobs.map(job => `
          <article class="job-card">
            ${coverHtml(job)}
            <div class="job-card-body">
              <div class="job-card-top">
                <span class="status status-${job.status}">${STATUS_LABEL[job.status] || job.status}</span>
                <span>Started ${esc(fmtDate(job.created_at))}</span>
              </div>
              <h2><a href="#/job/${job.id}">${esc(job.name)}</a></h2>
              ${isActive(job) || (job.doc_total && job.status !== 'completed') ? `<div class="progress ${job.status === 'running' ? 'is-live' : ''}" aria-hidden="true"><i style="width:${Math.round(progressOf(job) * 100)}%"></i></div>` : ''}
              <p class="now-line">${esc(jobProgressText(job))}</p>
              <dl class="facts-row">
                <div><dt>Documents</dt><dd>${job.doc_done}${job.doc_total ? ` / ${job.doc_total}` : ''}</dd></div>
                <div><dt>Cost</dt><dd data-live="cost:${job.id}">${fmtMoney(job.cost_usd)}</dd></div>
                <div><dt>Time</dt><dd data-live="elapsed:${job.id}">${fmtDuration(job.elapsed_s)}</dd></div>
              </dl>
              <div class="btn-row">
                <a class="btn btn-sm" href="#/job/${job.id}">Open</a>
                ${job.has_zip ? `<a class="btn btn-sm" href="/api/jobs/${job.id}/download">${icon('download')}ZIP</a>` : ''}
                ${job.resumable ? `<button class="btn btn-sm" data-resume="${job.id}">${icon('resume')}Resume</button>` : ''}
                ${isActive(job) ? `<button class="btn btn-sm" data-cancel="${job.id}">${icon('stop')}Cancel</button>` : ''}
              </div>
            </div>
          </article>`).join('')}
        <a class="job-card-new" href="#/new">${icon('plus')}New strategy</a>
      </div>
    </div>`;

  wireImages(view);
  view.querySelectorAll('[data-resume]').forEach(b => { b.onclick = () => resumeJob(b.dataset.resume); });
  view.querySelectorAll('[data-cancel]').forEach(b => { b.onclick = () => cancelJob(b.dataset.cancel); });
}

// ─── Strategy page ──────────────────────────────────────────

function tierOf(id) {
  return TIERS.find(t => t.prefix !== 'U' && id.startsWith(t.prefix))?.prefix || 'U';
}

function filesFor(job, docId) {
  const prefix = docId.toLowerCase() + '_';
  return (job.files || []).filter(f => f.name.toLowerCase().startsWith(prefix));
}

function variantOf(file) {
  if (['xlsx', 'xls', 'csv'].includes(file.kind)) return 'sheet';
  const stem = file.name.replace(/\.[^.]+$/, '').toLowerCase();
  const m = stem.match(/_(diagram|chart|visual|render)$/);
  if (m) return m[1];
  if (stem.endsWith('_value_stack')) return 'value';
  return 'report';
}

function labelOf(docId, variant) {
  if (variant === 'visual') return VISUAL_LABEL[docId] || 'Visual';
  if (variant === 'render') return RENDER_LABEL[docId] || 'Preview';
  return { diagram: 'Diagram', chart: 'Chart', value: 'Value equation', sheet: 'Spreadsheet', report: 'Report' }[variant];
}

// The files of one document, most visual first, each with its card label.
function docFiles(job, docId) {
  return filesFor(job, docId)
    .map(f => { const variant = variantOf(f); return { ...f, variant, label: labelOf(docId, variant) }; })
    .sort((a, b) => VIEW_RANK[a.variant] - VIEW_RANK[b.variant] || a.name.localeCompare(b.name));
}

function slideHtml(job, f) {
  if (f.preview === 'report') {
    return `<div class="slide slide-report">
      <img class="sheet" alt="" loading="lazy" src="${previewUrl(job, f, 0)}">
      <img class="sheet" alt="" loading="lazy" src="${previewUrl(job, f, 1)}">
    </div>`;
  }
  if (f.preview === 'page') {
    return `<div class="slide"><img class="sheet" alt="" loading="lazy" src="${previewUrl(job, f, 0)}"></div>`;
  }
  if (f.preview === 'web') {
    return `<div class="slide slide-web"><div class="browser"><div class="browser-bar"><i></i><i></i><i></i></div>
      <img alt="" loading="lazy" src="${previewUrl(job, f, 0)}"></div></div>`;
  }
  return `<div class="slide slide-image"><img alt="" loading="lazy" src="${fileUrl(job, f)}"></div>`;
}

function showView(card, job, doc, views, index) {
  const key = `${job.id}:${doc.id}`;
  const f = views[index];
  state.views.set(key, index);
  const holder = card.querySelector('[data-stage]');
  holder.innerHTML = `
    <a class="stage" href="${readerHash(job, doc.id, index)}" aria-label="Read the ${esc(f.label.toLowerCase())} of ${esc(doc.name)}">
      ${slideHtml(job, f)}
      <span class="stage-open">${icon('read')}Read ${esc(f.label.toLowerCase())}</span>
    </a>`;
  card.querySelector('[data-read]').href = readerHash(job, doc.id, index);
  card.querySelectorAll('.view-tab').forEach(t => t.setAttribute('aria-pressed', String(Number(t.dataset.view) === index)));
  wireImages(holder);
}

const GHOST_LABEL = { pending: 'In the plan', running: 'Writing now', failed: 'Failed' };

function cardEl(job, doc) {
  const key = `${job.id}:${doc.id}`;
  const files = doc.status === 'done' || doc.status === 'failed' ? docFiles(job, doc.id) : [];
  const sig = JSON.stringify([doc.status, doc.name, doc.errors, files.map(f => f.name + f.v)]);
  const hit = state.cards.get(key);
  if (hit && hit.sig === sig) return hit.el;

  const views = files.filter(f => f.preview);
  const el = document.createElement('article');
  el.className = `card is-${doc.status}`;
  el.innerHTML = `
    <div data-stage>${views.length ? '' : `<div class="stage">${ghostHtml(GHOST_LABEL[doc.status] || '')}</div>`}</div>
    ${views.length > 1 ? `
      <div class="views" role="group" aria-label="Views of ${esc(doc.name)}">
        ${views.map((f, i) => `<button type="button" class="view-tab" data-view="${i}">${esc(f.label)}</button>`).join('')}
      </div>` : ''}
    <div class="card-body">
      <div class="card-title"><span class="doc-id">${esc(doc.id)}</span><h3>${esc(doc.name)}</h3></div>
      <p class="card-desc">${esc(DOC_INFO[doc.id]?.[1] || '')}</p>
      ${doc.errors?.length ? `<p class="card-errs">${doc.errors.map(esc).join('<br>')}</p>` : ''}
      ${files.length ? `
        <div class="files">
          ${views.length ? `<a class="btn btn-sm btn-ink" data-read href="#">${icon('read')}Read</a>` : ''}
          ${files.map(f => `<a class="file" href="${fileUrl(job, f)}" download="${esc(f.name)}" title="Download ${esc(f.name)}">${icon('download')}<span>${esc(f.label)}</span><small>${f.kind.toUpperCase()} ${fmtSize(f.size)}</small></a>`).join('')}
        </div>` : ''}
    </div>`;

  if (views.length) {
    const saved = state.views.get(key) || 0;
    showView(el, job, doc, views, saved < views.length ? saved : 0);
    el.querySelectorAll('.view-tab').forEach(t => {
      t.onclick = () => showView(el, job, doc, views, Number(t.dataset.view));
    });
  }
  state.cards.set(key, { sig, el });
  return el;
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
    return `<div class="notice notice-warn"><div><strong>Some documents had errors</strong><p>${esc(job.error_detail || '')} Resume to regenerate only those.</p></div></div>`;
  }
  if (job.status === 'cancelled') {
    return `<div class="notice notice-info"><div><strong>Generation cancelled</strong><p>Finished documents are kept. Resume to generate the rest.</p></div></div>`;
  }
  return '';
}

function verdictHtml(d) {
  if (!d?.bottleneck) return '';
  const items = [
    ['Bottleneck', BOTTLENECK[d.bottleneck] || d.bottleneck, 'key'],
    ['Main channel', CHANNEL[d.primary_channel]],
    ['Backup channel', CHANNEL[d.secondary_channel]],
    ['Stage', MATURITY[d.maturity]],
  ].filter(([, v]) => v);
  return `<dl class="verdict">${items.map(([k, v, cls]) => `<div class="${cls || ''}"><dt>${k}</dt><dd><span>${esc(v)}</span></dd></div>`).join('')}</dl>`;
}

function nowHtml(job) {
  if (job.status === 'running') {
    if (job.phase === 'diagnostic') return 'Diagnosing the business';
    if (job.phase === 'packaging') return 'Packaging the ZIP';
    return job.current ? `Writing <b>${esc(job.current)}</b>` : 'Starting';
  }
  if (job.status === 'queued') {
    const running = (state.jobs || []).find(j => j.status === 'running' && j.id !== job.id);
    return running ? `Starts when <b>${esc(running.name)}</b> finishes` : 'Starting in a moment';
  }
  return job.finished_at ? `${endVerb(job)} ${esc(fmtDate(job.finished_at))}` : '';
}

function waitingHtml(job) {
  if (job.status === 'queued') {
    return `<div class="waiting"><div class="stage">${ghostHtml('')}</div><div><h2>Waiting for its turn</h2><p>Strategies are generated one at a time. This one starts as soon as the generation before it finishes.</p></div></div>`;
  }
  if (job.status === 'running') {
    return `<div class="waiting is-running"><div class="stage">${ghostHtml('Reading')}</div><div><h2>Reading your answers</h2><p>The diagnostic finds the bottleneck and decides which of the 31 documents your business needs. It usually takes 3 to 6 minutes, then the documents appear here one by one.</p></div></div>`;
  }
  return `<div class="waiting"><div class="stage">${ghostHtml('')}</div><div><h2>No documents yet</h2><p>The run stopped before the diagnostic finished. Resume to start again from the diagnostic.</p></div></div>`;
}

function startHtml(job) {
  const done = id => job.docs.some(d => d.id === id && d.status === 'done') && docFiles(job, id).some(f => f.preview);
  if (!done('U1')) return '';
  // The diagnostic opens on its report, the roadmap on its week-by-week view.
  const reportView = docFiles(job, 'U1').filter(f => f.preview).findIndex(f => f.variant === 'report');
  return `
    <section class="start">
      <div>
        <h2>Where to start</h2>
        <p>Read the diagnostic first: it explains the bottleneck the rest of the plan attacks. Then open the launch roadmap and do the first task of week 1. Come back to the other documents as the roadmap points to them.</p>
      </div>
      <div class="btn-row">
        <a class="btn btn-primary" href="${readerHash(job, 'U1', Math.max(0, reportView))}">${icon('read')}Read the diagnostic</a>
        ${done('U9') ? `<a class="btn" href="${readerHash(job, 'U9', 0)}">${icon('read')}Open the roadmap</a>` : ''}
      </div>
    </section>`;
}

function renderJob(job) {
  const sig = JSON.stringify(['job', liveFree(job), state.ui.renaming, (state.jobs || []).find(j => j.status === 'running')?.id]);
  if (sig === state.ui.sig) { patchLive(job); return; }
  state.ui.sig = sig;

  const pct = Math.round(progressOf(job) * 100);
  const groups = TIERS.map(t => ({ ...t, docs: job.docs.filter(d => tierOf(d.id) === t.prefix) })).filter(g => g.docs.length);

  view.innerHTML = `
    <section class="band"><div class="wrap">
      <a class="back" href="#/">${icon('back')}All strategies</a>
      <div class="hero">
        <div class="hero-main">
          <div class="hero-meta">
            <span class="status status-${job.status}">${STATUS_LABEL[job.status] || job.status}</span>
            <span>Started ${esc(fmtDate(job.created_at))}${job.attempts > 1 ? `, ${job.attempts} attempts` : ''}</span>
          </div>
          ${state.ui.renaming ? `
            <form class="rename" data-rename>
              <label class="sr-only" for="rename-input">Strategy name</label>
              <input id="rename-input" type="text" value="${esc(job.name)}" maxlength="80" required>
              <button class="btn btn-primary" type="submit">Save name</button>
              <button class="btn" type="button" data-act="rename-cancel">Cancel</button>
            </form>` : `<h1>${esc(job.name)}</h1>`}
          ${verdictHtml(job.diagnosis)}
        </div>
        <div class="hero-actions">
          ${job.has_zip ? `<a class="btn btn-primary" href="/api/jobs/${job.id}/download">${icon('download')}Download ZIP</a>` : ''}
          ${job.resumable ? `<button class="btn ${job.has_zip ? '' : 'btn-primary'}" data-act="resume">${icon('resume')}Resume</button>` : ''}
          ${isActive(job) ? `<button class="btn" data-act="cancel">${icon('stop')}Cancel generation</button>` : ''}
          <details class="menu" ${state.ui.menuOpen ? 'open' : ''}>
            <summary class="btn" aria-label="More actions">${icon('more')}More</summary>
            <div class="menu-list">
              <button data-act="duplicate">${icon('copy')}Edit answers and run again</button>
              <button data-act="rename">${icon('pencil')}Rename</button>
              ${!isActive(job) ? `<button class="danger" data-act="delete">${icon('trash')}Delete</button>` : ''}
            </div>
          </details>
        </div>
      </div>
      <div class="stats">
        <div class="stat"><b>${job.doc_done}<small>/ ${job.doc_total || '?'}</small></b><span>documents written</span></div>
        <div class="stat"><b data-live="elapsed:${job.id}">${fmtDuration(job.elapsed_s)}</b><span>generation time</span></div>
        <div class="stat"><b data-live="cost:${job.id}">${fmtMoney(job.cost_usd)}</b><span>${isActive(job) ? 'API cost so far' : 'API cost'}</span></div>
        <p class="now">${nowHtml(job)}</p>
      </div>
      <div class="progress ${job.status === 'running' ? 'is-live' : ''}" role="progressbar" aria-label="Documents written" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100"><i style="width:${pct}%"></i></div>
    </div></section>

    <div class="wrap page">
      ${jobNotice(job)}
      ${startHtml(job)}
      ${groups.length ? groups.map(g => `
        <section class="tier">
          <header class="tier-head">
            <h2>${esc(g.title)}</h2>
            <p>${esc(g.blurb)}</p>
            <span class="tier-count">${g.docs.length} ${g.docs.length > 1 ? 'documents' : 'document'}</span>
          </header>
          <div class="cards" data-tier="${g.prefix}"></div>
        </section>`).join('') : waitingHtml(job)}
      <details class="log" ${state.ui.logOpen ? 'open' : ''}>
        <summary>Run log</summary>
        <pre id="log">${esc(state.ui.log || 'Loading…')}</pre>
      </details>
    </div>`;

  for (const g of groups) {
    view.querySelector(`[data-tier="${g.prefix}"]`).append(...g.docs.map(d => cardEl(job, d)));
  }

  // Resume lives in the header; the notice only offers the fix for the error.
  const holder = view.querySelector('[data-notice-actions]');
  if (holder && job.error && job.error.action !== 'resume') {
    errorActions(job.error, job.id).forEach((a, i) => {
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
      state.ui.menuOpen = false;
      if (act === 'resume') resumeJob(job.id);
      else if (act === 'cancel') cancelJob(job.id);
      else if (act === 'delete') deleteJob(job.id, job.name);
      else if (act === 'duplicate') go(`#/new?from=${job.id}`);
      else if (act === 'rename') { state.ui.renaming = true; renderJob(job); view.querySelector('#rename-input')?.focus(); }
      else if (act === 'rename-cancel') { state.ui.renaming = false; renderJob(job); }
    };
  });

  const menu = view.querySelector('details.menu');
  menu.ontoggle = () => { state.ui.menuOpen = menu.open; };

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
  if (!state.ui.renaming || !view.querySelector('[data-rename]')) renderJob(job);
  if (state.ui.logOpen) refreshLog(id);
  syncReader(job);
}

// ─── Reader ─────────────────────────────────────────────────
// Documents open full screen inside the app: a report as its web version or
// its PDF, a landing page or roadmap live, a visual or diagram at full size.
// It lives in the URL (#/job/<id>/doc/<docId>?view=<n>&as=pdf) on top of the
// strategy page, so Back closes it and the page keeps its scroll position.

const reader = document.getElementById('reader');
const FRAME_SANDBOX = 'allow-scripts allow-popups allow-popups-to-escape-sandbox allow-forms';

function readerHash(job, docId, viewIndex = 0, as = '') {
  return `#/job/${job.id}/doc/${docId}?view=${viewIndex}${as ? `&as=${as}` : ''}`;
}

// Documents with something to read, in the order the strategy page shows them.
function readableDocs(job) {
  return TIERS.flatMap(t => job.docs.filter(d => tierOf(d.id) === t.prefix))
    .filter(d => (d.status === 'done' || d.status === 'failed') && docFiles(job, d.id).some(f => f.preview));
}

function syncReader(job) {
  const route = state.route;
  const docs = route?.doc ? readableDocs(job) : [];
  const pos = docs.findIndex(d => d.id === route.doc);
  if (pos < 0) { closeReaderUi(); return; }

  const doc = docs[pos];
  const views = docFiles(job, doc.id).filter(f => f.preview);
  const index = Math.min(Math.max(0, Number(route.params.get('view')) || 0), views.length - 1);
  const f = views[index];
  let as = 'image';
  if (f.preview !== 'image') as = route.params.get('as') === 'pdf' && f.pdf ? 'pdf' : f.web ? 'web' : 'pdf';
  const sig = JSON.stringify([job.id, doc.id, index, as, f.name, f.v, docs.map(d => d.id)]);
  if (sig === state.readerSig) return;
  state.readerSig = sig;

  const src = as === 'image' ? fileUrl(job, f) : fileUrl(job, { name: as === 'pdf' ? f.pdf : f.web, v: f.v });
  const step = (d, dir) => d
    ? `<a class="btn btn-sm" href="${readerHash(job, d.id)}" data-replace data-focus="${dir}" aria-label="${dir === 'prev' ? 'Previous' : 'Next'} document: ${esc(d.name)}" title="${esc(d.name)}">${icon(dir)}</a>`
    : `<span class="btn btn-sm" aria-disabled="true">${icon(dir)}</span>`;
  const keep = reader.contains(document.activeElement) ? document.activeElement.dataset.focus : null;

  reader.innerHTML = `
    <div class="reader-bar">
      <div class="reader-top">
        <button type="button" class="reader-close" data-reader-close data-focus="close" aria-label="Close the reader">${icon('back')}<span>All documents</span></button>
        <div class="reader-title"><span class="doc-id">${esc(doc.id)}</span><h2 id="reader-title">${esc(doc.name)}</h2></div>
        <div class="reader-step">${step(docs[pos - 1], 'prev')}<span>${pos + 1} of ${docs.length}</span>${step(docs[pos + 1], 'next')}</div>
      </div>
      <div class="reader-tools">
        <div class="views" role="group" aria-label="Views of ${esc(doc.name)}">
          ${views.length > 1 ? views.map((v, i) => `<a class="view-tab" href="${readerHash(job, doc.id, i)}" data-replace data-focus="view-${i}" aria-pressed="${i === index}">${esc(v.label)}</a>`).join('') : ''}
        </div>
        <div class="reader-actions">
          ${f.web && f.pdf ? `
            <div class="seg" role="group" aria-label="Format">
              <a href="${readerHash(job, doc.id, index, 'web')}" data-replace data-focus="web" aria-pressed="${as === 'web'}">Web page</a>
              <a href="${readerHash(job, doc.id, index, 'pdf')}" data-replace data-focus="pdf" aria-pressed="${as === 'pdf'}">PDF</a>
            </div>` : ''}
          <a class="btn btn-sm" href="${src}" target="_blank" rel="noopener">${icon('open')}New tab</a>
          <a class="btn btn-sm btn-primary" href="${fileUrl(job, f)}" download="${esc(f.name)}">${icon('download')}Download ${f.kind.toUpperCase()}</a>
        </div>
      </div>
    </div>
    <div class="reader-body">
      ${as === 'image'
        ? `<div class="reader-image"><img src="${src}" alt="${esc(f.label)} of ${esc(doc.name)}" title="Click to zoom"></div>`
        : `<iframe class="reader-frame" src="${src}" title="${esc(doc.name)}, ${esc(as === 'pdf' ? 'PDF' : f.label.toLowerCase())}"${as === 'web' ? ` sandbox="${FRAME_SANDBOX}"` : ''}></iframe>`}
    </div>`;

  const img = reader.querySelector('.reader-image img');
  if (img) {
    // Visuals and diagrams are rendered at twice their size: show them at
    // their natural size, and at full resolution on click.
    const size = () => { img.style.width = `${img.naturalWidth / (img.classList.contains('is-zoomed') ? 1 : 2)}px`; };
    if (img.complete && img.naturalWidth) size(); else img.addEventListener('load', size, { once: true });
    img.onclick = () => { img.classList.toggle('is-zoomed'); size(); };
  }
  openReaderUi();
  (reader.querySelector(`[data-focus="${keep}"]`) || reader.querySelector('[data-reader-close]')).focus();
}

function openReaderUi() {
  if (!reader.hidden) return;
  state.readerReturn = document.activeElement;
  reader.hidden = false;
  document.documentElement.classList.add('is-reading');
  view.inert = true;
  document.querySelector('.topbar').inert = true;
}

function closeReaderUi() {
  if (reader.hidden) return;
  reader.hidden = true;
  reader.innerHTML = '';
  state.readerSig = '';
  document.documentElement.classList.remove('is-reading');
  view.inert = false;
  document.querySelector('.topbar').inert = false;
  if (document.contains(state.readerReturn)) state.readerReturn.focus({ preventScroll: true });
}

function closeReader() {
  // Opened from the strategy page: going back is closing. Opened from a link: replace.
  if (state.readerPushed) history.back();
  else { history.replaceState(null, '', `#/job/${state.route.id}`); render(); }
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
    <section class="band"><div class="wrap band-head">
      <div>
        <h1>New strategy</h1>
        <p>About 10 minutes. Your answers are saved in this browser as you go.</p>
      </div>
      <div class="form-tools">
        <button class="btn" data-tool="example">Fill with example answers</button>
        <button class="btn" data-tool="clear">Clear all answers</button>
      </div>
    </div></section>
    <div class="wrap page">
      <div class="wizard">
        <ol class="steps">
          ${steps.map((s, i) => {
            const n = i + 1;
            const cls = n === F.step ? 'current' : stepDone(n) ? 'done' : '';
            const dot = cls === 'done' ? icon('check') : n;
            return `<li class="${cls}"><button data-step="${n}" ${n === F.step ? 'aria-current="step"' : ''}><span class="step-dot">${dot}</span><span>${esc(s.title)}</span></button></li>`;
          }).join('')}
        </ol>
        <form id="qform" class="form-card" novalidate>
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
            ${F.step > 1 ? '<button type="button" class="btn" data-nav-step="back">Back</button>' : '<span></span>'}
            <button type="submit" class="btn btn-primary">${last ? 'Generate my strategy' : 'Continue'}</button>
          </div>
        </form>
      </div>
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
    <section class="band"><div class="wrap band-head">
      <div>
        <h1>Settings</h1>
        <p>Your Anthropic key and the models each part of the generation uses.</p>
      </div>
    </div></section>
    <div class="wrap page">
      <div class="settings">
        <section class="panel">
          <h2>Anthropic API key</h2>
          <p class="key-status ${s.has_api_key ? 'ok' : ''}">${s.has_api_key ? `Key ${esc(s.api_key_hint)}. ${esc(source)}.` : 'No key yet. Generation needs one.'}</p>
          <form class="field" id="key-form">
            <label for="api-key">${s.has_api_key ? 'Replace the key' : 'Paste your key'}</label>
            <div class="key-input">
              <input type="password" id="api-key" placeholder="sk-ant-…" autocomplete="off" spellcheck="false">
              <button type="button" class="btn" id="toggle-key">Show</button>
            </div>
            <p class="help">Create one in the <a href="https://console.anthropic.com/settings/keys" target="_blank" rel="noopener">Anthropic Console</a>. It is stored in <code>data/settings.json</code> on this computer and only ever sent to Anthropic.</p>
            <div class="btn-row field">
              <button type="submit" class="btn btn-primary">Save key</button>
              <button type="button" class="btn" id="test-key">Test key</button>
              ${s.api_key_source === 'settings' ? '<button type="button" class="btn btn-danger" id="remove-key">Remove saved key</button>' : ''}
            </div>
          </form>
        </section>
        <section class="panel">
          <h2>Models</h2>
          <p class="help">The defaults balance quality and cost: a full strategy costs about $3 to $8. Stronger models raise both.</p>
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
      </div>
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
  const m = path.match(/^\/job\/([a-z0-9]+)(?:\/doc\/([A-Z]+[0-9]+))?$/);
  if (m) return { name: 'job', id: m[1], doc: m[2] || null, params };
  if (path === '/new') return { name: 'new', params };
  if (path === '/settings') return { name: 'settings', params };
  return { name: 'list', params };
}

async function render() {
  const route = parseRoute();
  const before = state.route;
  const changed = before?.name !== route.name || before?.id !== route.id;
  // The reader was opened from this strategy's page (a history entry was pushed).
  if (route.doc && !before?.doc) state.readerPushed = !changed;
  state.route = route;
  if (route.name !== 'job') closeReaderUi();
  if (changed) {
    state.ui = { renaming: false, logOpen: false, log: '', menuOpen: false, sig: '' };
    state.cards.clear();
  }
  // Views other than the list and the job page always rebuild.
  if (route.name !== 'list' && route.name !== 'job') state.ui.sig = '';

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
      closeReaderUi();
      view.innerHTML = '<div class="wrap page"><h1>Not found</h1><p class="muted" style="margin-top:12px">This strategy was deleted or never existed. <a href="#/">Back to strategies</a></p></div>';
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
  // A click outside an open menu closes it.
  document.addEventListener('click', ev => {
    document.querySelectorAll('details.menu[open]').forEach(d => { if (!d.contains(ev.target)) d.open = false; });
  });
  // Inside the reader, switching views or documents replaces the history entry,
  // so Back always returns to the strategy page.
  reader.addEventListener('click', ev => {
    if (ev.target.closest('[data-reader-close]')) { closeReader(); return; }
    const a = ev.target.closest('a[data-replace]');
    if (a && ev.button === 0 && !ev.metaKey && !ev.ctrlKey && !ev.shiftKey) {
      ev.preventDefault();
      history.replaceState(null, '', a.getAttribute('href'));
      render();
    }
  });
  document.addEventListener('keydown', ev => {
    if (reader.hidden || ev.altKey || ev.ctrlKey || ev.metaKey) return;
    if (ev.key === 'Escape') { ev.preventDefault(); closeReader(); }
    if (ev.key === 'ArrowLeft') reader.querySelector('a[data-focus="prev"]')?.click();
    if (ev.key === 'ArrowRight') reader.querySelector('a[data-focus="next"]')?.click();
  });
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
