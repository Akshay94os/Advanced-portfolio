/**
 * Portfolio – Global JS utilities
 * (GSAP page animations are handled inline in templates)
 */

// ── Generic CRUD helpers ──────────────────────────────────────────────────────

/**
 * Submit a form via fetch, show toast, and optionally reload or update DOM.
 * @param {string} url
 * @param {FormData|object} formData
 * @param {function} onSuccess – called with response JSON on success
 */
async function apiPost(url, formData, onSuccess) {
  const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
  if (formData instanceof FormData) {
    if (!formData.has('csrfmiddlewaretoken')) formData.append('csrfmiddlewaretoken', csrf);
  }
  try {
    const res  = await fetch(url, { method: 'POST', body: formData });
    const data = await res.json();
    if (data.success) {
      showToast(data.message || 'Done!', 'success');
      if (typeof onSuccess === 'function') onSuccess(data);
    } else {
      showToast(data.message || 'Something went wrong.', 'error');
    }
    return data;
  } catch (err) {
    showToast('Network error: ' + err.message, 'error');
    return { success: false };
  }
}

async function apiGet(url) {
  try {
    const res  = await fetch(url);
    const data = await res.json();
    return data;
  } catch (err) {
    showToast('Network error: ' + err.message, 'error');
    return { success: false };
  }
}

// ── Confirm delete helper ─────────────────────────────────────────────────────
function confirmDelete(message, onConfirm) {
  if (confirm(message || 'Are you sure you want to delete this?')) {
    onConfirm();
  }
}

// ── File extension → icon ─────────────────────────────────────────────────────
function extIcon(ext) {
  const e = (ext || '').toLowerCase();
  if (['pdf'].includes(e))                    return '<i class="fas fa-file-pdf ext-pdf"></i>';
  if (['jpg','jpeg','png','gif','webp'].includes(e)) return '<i class="fas fa-image ext-img"></i>';
  if (['doc','docx'].includes(e))             return '<i class="fas fa-file-word ext-doc"></i>';
  if (['zip','rar','tar','gz'].includes(e))   return '<i class="fas fa-file-archive ext-zip"></i>';
  if (['mp4','mkv','avi'].includes(e))        return '<i class="fas fa-file-video ext-other"></i>';
  return '<i class="fas fa-file ext-other"></i>';
}

// ── Populate form fields from object ─────────────────────────────────────────
function populateForm(formEl, data) {
  for (const [key, val] of Object.entries(data)) {
    const el = formEl.querySelector(`[name="${key}"]`);
    if (!el) continue;
    if (el.type === 'checkbox') el.checked = Boolean(val);
    else el.value = val ?? '';
  }
}

// ── Loading spinner on button ─────────────────────────────────────────────────
function setLoading(btn, loading) {
  if (!btn) return;
  if (loading) {
    btn.dataset.origText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Saving…';
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.origText || btn.innerHTML;
    btn.disabled = false;
  }
}

// ── Animated counter ─────────────────────────────────────────────────────────
function animateCounter(el, target, suffix = '') {
  let start = 0;
  const duration = 1500;
  const step = 16;
  const increment = target / (duration / step);
  const timer = setInterval(() => {
    start += increment;
    if (start >= target) { el.textContent = target + suffix; clearInterval(timer); }
    else el.textContent = Math.floor(start) + suffix;
  }, step);
}

// ── Scroll reveal (supplement GSAP inline) ───────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Animate any progress bars
  document.querySelectorAll('.progress-bar-inner[data-width]').forEach(bar => {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          bar.style.width = bar.dataset.width + '%';
          observer.unobserve(bar);
        }
      });
    }, { threshold: 0.3 });
    bar.style.width = '0%';
    observer.observe(bar);
  });

  // Floating particles (hero)
  const hero = document.getElementById('hero-particles');
  if (hero) {
    for (let i = 0; i < 20; i++) {
      const p = document.createElement('div');
      const size = Math.random() * 4 + 2;
      p.style.cssText = `
        position:absolute;width:${size}px;height:${size}px;border-radius:50%;
        background:rgba(124,58,237,${Math.random()*.4+.1});
        left:${Math.random()*100}%;top:${Math.random()*100}%;
        animation:float ${Math.random()*4+4}s ease-in-out infinite;
        animation-delay:${Math.random()*3}s;pointer-events:none;
      `;
      hero.appendChild(p);
    }
  }
});
