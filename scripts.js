// Escape remote or generated text before rendering it into HTML.
function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  })[character]);
}

function safeUrl(value, { allowRelative = false } = {}) {
  try {
    const url = new URL(String(value), window.location.origin);
    if ((allowRelative && url.origin === window.location.origin) || ['http:', 'https:'].includes(url.protocol)) {
      return url.href;
    }
  } catch (_) {
    // Render no link for malformed values.
  }
  return '#';
}

// Load and render Medium posts
function renderMediumPosts(targetId='medium-posts') {
  const container = document.getElementById(targetId);
  if (!container) return;

  fetch('assets/medium_posts.json')
    .then(r => r.ok ? r.json() : Promise.reject('no json'))
    .then(data => {
      const posts = data.posts || [];
      if (!posts.length) {
        container.innerHTML = '<div class="card" style="text-align:center;padding:40px"><div class="small" style="color:var(--muted)">No recent posts yet.</div></div>';
        return;
      }

      container.innerHTML = posts.map(p => `
        <a href="${safeUrl(p.link)}" target="_blank" rel="noopener" class="card" style="display:block;text-decoration:none;transition:all 0.3s">
          <div style="margin-bottom:12px">
            <strong style="color:#e6eef8;font-size:1.05rem;line-height:1.4;display:block">${escapeHtml(p.title)}</strong>
          </div>
          <div class="small" style="color:var(--muted);line-height:1.6;margin-bottom:12px">${escapeHtml(p.excerpt)}</div>
          <div class="small" style="color:var(--accent);font-weight:600;display:flex;justify-content:space-between;align-items:center">
            <span>${p.date ? new Date(p.date).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : 'Read article'}</span>
            <span style="font-size:0.8rem">Read more →</span>
          </div>
        </a>
      `).join('');
    })
    .catch(err => {
      console.warn('medium posts load failed', err);
      container.innerHTML = '<div class="card" style="text-align:center;padding:40px"><div class="small" style="color:var(--muted)">Unable to load Medium posts.</div></div>';
    });
}

// Load and render certificates
function renderCertificates() {
  const summaryContainer = document.getElementById('certificates-summary');
  const listContainer = document.getElementById('certificates-list');

  if (!summaryContainer || !listContainer) return;

  fetch('assets/certificates.json')
    .then(r => r.ok ? r.json() : Promise.reject('no json'))
    .then(data => {
      // Render category summary cards
      const categories = data.categories || {};
      const summaryGrid = summaryContainer.querySelector('.grid');

      summaryGrid.innerHTML = Object.entries(categories).map(([key, cat]) => `
        <div class="card" style="text-align:center;padding:16px;cursor:pointer" data-cert-category="${escapeHtml(key)}" role="button" tabindex="0">
          <div style="font-size:2rem;margin-bottom:8px">${escapeHtml(cat.icon)}</div>
          <div style="font-weight:600;font-size:1.2rem;color:${escapeHtml(cat.color)}">${escapeHtml(cat.count)}</div>
          <div class="small" style="margin-top:4px">${escapeHtml(cat.display_name)}</div>
        </div>
      `).join('');

      // Render full certificate list by category
      listContainer.innerHTML = Object.entries(categories).map(([key, cat]) => `
        <div id="cert-category-${key}" style="margin-bottom:40px">
          <h3 style="display:flex;align-items:center;gap:10px;margin-bottom:20px">
            <span style="font-size:1.5rem">${escapeHtml(cat.icon)}</span>
            ${escapeHtml(cat.display_name)}
            <span class="small" style="color:var(--muted);font-weight:normal">(${escapeHtml(cat.count)} certificates)</span>
          </h3>
          <div class="grid">
            ${cat.certificates.map(cert => `
              <a href="${safeUrl(cert.path, { allowRelative: true })}" target="_blank" rel="noopener" class="card" style="display:block;text-decoration:none;padding:20px;transition:all 0.3s">
                <div style="display:flex;align-items:flex-start;gap:12px">
                  <div style="font-size:2rem;opacity:0.6;flex-shrink:0">📄</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-weight:600;font-size:1.05rem;color:#e6eef8;margin-bottom:8px;line-height:1.4;word-wrap:break-word">${escapeHtml(cert.title)}</div>
                    <div class="small" style="color:var(--accent);font-weight:600">${escapeHtml(cert.provider)}</div>
                  </div>
                </div>
              </a>
            `).join('')}
          </div>
        </div>
      `).join('');
      summaryGrid.querySelectorAll('[data-cert-category]').forEach(card => {
        const handleActivate = () => scrollToCertCategory(card.dataset.certCategory);
        card.addEventListener('click', handleActivate);
        card.addEventListener('keydown', event => {
          if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); handleActivate(); }
        });
      });
    })
    .catch(err => {
      console.warn('certificates load failed', err);
      listContainer.innerHTML = '<div class="small">Unable to load certificates. Please check the certificates.json file.</div>';
    });
}

// Scroll to specific certificate category
function scrollToCertCategory(categoryKey) {
  const element = document.getElementById(`cert-category-${categoryKey}`);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    // Highlight briefly
    element.style.transition = 'background 0.3s';
    element.style.background = 'rgba(96,165,250,0.1)';
    element.style.borderRadius = '8px';
    element.style.padding = '16px';
    setTimeout(() => {
      element.style.background = '';
      element.style.padding = '';
    }, 1500);
  }
}

// Render certificate summary (for homepage)
function renderCertificatesSummary() {
  const container = document.getElementById('certificates-summary-home');
  if (!container) return;

  fetch('assets/certificates.json')
    .then(r => r.ok ? r.json() : Promise.reject('no json'))
    .then(data => {
      const categories = data.categories || {};
      const grid = container.querySelector('.grid');

      grid.innerHTML = Object.entries(categories).map(([key, cat]) => `
        <a href="certifications.html#cert-category-${key}" class="card" style="text-align:center;padding:16px;display:block;text-decoration:none;transition:all 0.3s">
          <div style="font-size:2rem;margin-bottom:8px">${cat.icon}</div>
          <div style="font-weight:600;font-size:1.2rem;color:${cat.color}">${cat.count}</div>
          <div class="small" style="margin-top:4px;color:#e6eef8">${cat.display_name}</div>
        </a>
      `).join('');
    })
    .catch(err => {
      console.warn('certificates summary load failed', err);
    });
}

// Load and render badge certifications
function renderBadgeCertifications() {
  const certsGrid = document.getElementById('credentials-certificates-grid');
  const badgesGrid = document.getElementById('credentials-badges-grid');

  // If containers don't exist, exit early
  if (!certsGrid && !badgesGrid) return;

  fetch('assets/badge_certifications.json')
    .then(r => r.ok ? r.json() : Promise.reject('no json'))
    .then(data => {
      const categories = data.categories || {};

      // Combine all certifications from all categories
      let allCertifications = [];

      Object.entries(categories).forEach(([categoryKey, category]) => {
        if (category.certifications && category.certifications.length > 0) {
          allCertifications = allCertifications.concat(category.certifications);
        }
      });

      // Sort by issue date (newest first)
      allCertifications.sort((a, b) => {
        const dateA = a.issue_date ? new Date(a.issue_date) : new Date(0);
        const dateB = b.issue_date ? new Date(b.issue_date) : new Date(0);
        return dateB - dateA;
      });

      // Split into types
      const certificates = allCertifications.filter(c => (c.cert_type || 'Certified Badges') === 'Certificates');
      const certifiedBadges = allCertifications.filter(c => (c.cert_type || 'Certified Badges') === 'Certified Badges');

      // Helper function to render a list of certs to HTML
      const renderCerts = (certs) => {
        if (certs.length === 0) {
          return '<div class="small" style="color:var(--muted);padding:20px;text-align:center;grid-column:1/-1;">No credentials available</div>';
        }
        
        return certs.map(cert => {
          const hasVerification = cert.verification_url && !cert.verification_url.includes('YOUR-');
          const expiryWarning = cert.expiry_date && new Date(cert.expiry_date) < new Date() ?
            '<div class="small" style="color:#EF4444;margin-top:4px">⚠️ Expired</div>' : '';

          const content = `
            <div class="badge">
              <img src="${safeUrl(cert.badge_path, { allowRelative: true })}"
                   alt="${escapeHtml(cert.title)}">
              <div class="issuer" style="margin-top:8px">
                <strong style="display:block;margin-bottom:4px;color:#e6eef8">${escapeHtml(cert.title)}</strong>
                <span style="color:var(--muted)">${escapeHtml(cert.provider)}</span>
                ${cert.issue_date ? `<div class="small" style="margin-top:4px;color:var(--muted)">Issued: ${new Date(cert.issue_date).toLocaleDateString('en-US', {year: 'numeric', month: 'short'})}</div>` : ''}
                ${cert.expiry_date ? `<div class="small" style="color:var(--muted)">Expires: ${new Date(cert.expiry_date).toLocaleDateString('en-US', {year: 'numeric', month: 'short'})}</div>` : ''}
                ${expiryWarning}
                ${cert.description ? `<div class="small" style="margin-top:8px;color:var(--muted);font-style:italic">${escapeHtml(cert.description)}</div>` : ''}
              </div>
            </div>
          `;

          if (hasVerification) {
            return `<a href="${safeUrl(cert.verification_url)}" target="_blank" rel="noopener" style="text-decoration:none">${content}</a>`;
          } else {
            return content;
          }
        }).join('');
      };

      if (certsGrid) certsGrid.innerHTML = renderCerts(certificates);
      if (badgesGrid) badgesGrid.innerHTML = renderCerts(certifiedBadges);
    })
    .catch(err => {
      console.warn('badge certifications load failed', err);
      const errMsg = '<div class="small" style="color:var(--muted);padding:20px;text-align:center;grid-column:1/-1;">Configure your certifications in tools/badge_certifications.yaml</div>';
      if (certsGrid) certsGrid.innerHTML = errMsg;
      if (badgesGrid) badgesGrid.innerHTML = errMsg;
    });
}

// Render badge certifications summary (for homepage)
function renderBadgeCertificationsSummary() {
  const container = document.getElementById('badge-certifications-summary-home');
  if (!container) return;

  fetch('assets/badge_certifications.json')
    .then(r => r.ok ? r.json() : Promise.reject('no json'))
    .then(data => {
      const categories = data.categories || {};

      // Get all certifications from all categories
      let allCerts = [];
      Object.values(categories).forEach(cat => {
        if (cat.certifications) {
          allCerts = allCerts.concat(cat.certifications);
        }
      });

      // Sort by issue date (newest first)
      allCerts.sort((a, b) => {
        const dateA = a.issue_date ? new Date(a.issue_date) : new Date(0);
        const dateB = b.issue_date ? new Date(b.issue_date) : new Date(0);
        return dateB - dateA;
      });

      // Render ALL badges in smaller size
      container.innerHTML = allCerts.map(cert => `
        <a href="${safeUrl(cert.verification_url)}" target="_blank" rel="noopener" style="text-decoration:none; display:block;">
          <div style="text-align:center;">
            <div style="width:100%; aspect-ratio:1; background:rgba(255,255,255,0.95); border-radius:6px; padding:6px; border:1px solid rgba(96,165,250,0.3); transition:all 0.3s; overflow:hidden;"
                 onmouseover="this.style.borderColor='#60a5fa'; this.style.transform='translateY(-2px)'"
                 onmouseout="this.style.borderColor='rgba(96,165,250,0.3)'; this.style.transform='translateY(0)'">
              <img src="${safeUrl(cert.badge_path, { allowRelative: true })}"
                   alt="${escapeHtml(cert.title)}"
                   style="width:100%; height:100%; object-fit:contain;">
            </div>
          </div>
        </a>
      `).join('');

      // Update total count if element exists
      const totalElement = document.getElementById('badge-total-count');
      if (totalElement) {
        totalElement.textContent = data.total_count || allCerts.length;
      }
    })
    .catch(err => {
      console.warn('badge certifications summary load failed', err);
      container.innerHTML = '<div class="small" style="color:var(--muted);padding:20px;text-align:center;">Configure your certifications in tools/badge_certifications.yaml</div>';
    });
}

// Mobile navigation handler
document.addEventListener('DOMContentLoaded', function() {
  const mobileNav = document.getElementById('mobile-nav');
  if (mobileNav) {
    mobileNav.addEventListener('change', function() {
      if (this.value) {
        window.location.href = this.value;
      }
    });
  }

  // Automatically render Medium posts if container exists
  renderMediumPosts();

  // Automatically render certificates if container exists
  renderCertificates();

  // Render certificate summary on homepage
  renderCertificatesSummary();

  // Render badge certifications if containers exist
  renderBadgeCertifications();

  // Render badge certifications summary on homepage
  renderBadgeCertificationsSummary();
});
