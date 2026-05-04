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
        <a href="${p.link}" target="_blank" rel="noopener" class="card" style="display:block;text-decoration:none;transition:all 0.3s">
          <div style="margin-bottom:12px">
            <strong style="color:#e6eef8;font-size:1.05rem;line-height:1.4;display:block">${p.title}</strong>
          </div>
          <div class="small" style="color:var(--muted);line-height:1.6;margin-bottom:12px">${p.excerpt}</div>
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
        <div class="card" style="text-align:center;padding:16px;cursor:pointer" onclick="scrollToCertCategory('${key}')">
          <div style="font-size:2rem;margin-bottom:8px">${cat.icon}</div>
          <div style="font-weight:600;font-size:1.2rem;color:${cat.color}">${cat.count}</div>
          <div class="small" style="margin-top:4px">${cat.display_name}</div>
        </div>
      `).join('');

      // Render full certificate list by category
      listContainer.innerHTML = Object.entries(categories).map(([key, cat]) => `
        <div id="cert-category-${key}" style="margin-bottom:40px">
          <h3 style="display:flex;align-items:center;gap:10px;margin-bottom:20px">
            <span style="font-size:1.5rem">${cat.icon}</span>
            ${cat.display_name}
            <span class="small" style="color:var(--muted);font-weight:normal">(${cat.count} certificates)</span>
          </h3>
          <div class="grid">
            ${cat.certificates.map(cert => `
              <a href="${cert.path}" target="_blank" class="card" style="display:block;text-decoration:none;padding:20px;transition:all 0.3s">
                <div style="display:flex;align-items:flex-start;gap:12px">
                  <div style="font-size:2rem;opacity:0.6;flex-shrink:0">📄</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-weight:600;font-size:1.05rem;color:#e6eef8;margin-bottom:8px;line-height:1.4;word-wrap:break-word">${cert.title}</div>
                    <div class="small" style="color:var(--accent);font-weight:600">${cert.provider}</div>
                  </div>
                </div>
              </a>
            `).join('')}
          </div>
        </div>
      `).join('');
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
  const credentialsContainer = document.getElementById('credentials-certifications-grid');

  // If container doesn't exist, exit early
  if (!credentialsContainer) return;

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

      // Render all certifications
      credentialsContainer.innerHTML = allCertifications.map(cert => {
        const hasVerification = cert.verification_url && !cert.verification_url.includes('YOUR-');
        const expiryWarning = cert.expiry_date && new Date(cert.expiry_date) < new Date() ?
          '<div class="small" style="color:#EF4444;margin-top:4px">⚠️ Expired</div>' : '';

        const content = `
          <div class="badge">
            <img src="${cert.badge_path}"
                 alt="${cert.title}"
                 onerror="this.src='${cert.fallback_svg}'">
            <div class="issuer" style="margin-top:8px">
              <strong style="display:block;margin-bottom:4px;color:#e6eef8">${cert.title}</strong>
              <span style="color:var(--muted)">${cert.provider}</span>
              ${cert.issue_date ? `<div class="small" style="margin-top:4px;color:var(--muted)">Issued: ${new Date(cert.issue_date).toLocaleDateString('en-US', {year: 'numeric', month: 'short'})}</div>` : ''}
              ${cert.expiry_date ? `<div class="small" style="color:var(--muted)">Expires: ${new Date(cert.expiry_date).toLocaleDateString('en-US', {year: 'numeric', month: 'short'})}</div>` : ''}
              ${expiryWarning}
              ${cert.description ? `<div class="small" style="margin-top:8px;color:var(--muted);font-style:italic">${cert.description}</div>` : ''}
            </div>
          </div>
        `;

        if (hasVerification) {
          return `<a href="${cert.verification_url}" target="_blank" rel="noopener" style="text-decoration:none">${content}</a>`;
        } else {
          return content;
        }
      }).join('');

      // If no certifications, show placeholder
      if (allCertifications.length === 0) {
        credentialsContainer.innerHTML = '<div class="small" style="color:var(--muted);padding:20px;text-align:center">Configure your certifications in tools/badge_certifications.yaml</div>';
      }
    })
    .catch(err => {
      console.warn('badge certifications load failed', err);
      credentialsContainer.innerHTML = '<div class="small" style="color:var(--muted);padding:20px;text-align:center">Configure your certifications in tools/badge_certifications.yaml</div>';
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
        <a href="${cert.verification_url}" target="_blank" rel="noopener" style="text-decoration:none; display:block;">
          <div style="text-align:center;">
            <div style="width:100%; aspect-ratio:1; background:rgba(255,255,255,0.95); border-radius:6px; padding:6px; border:1px solid rgba(96,165,250,0.3); transition:all 0.3s; overflow:hidden;"
                 onmouseover="this.style.borderColor='#60a5fa'; this.style.transform='translateY(-2px)'"
                 onmouseout="this.style.borderColor='rgba(96,165,250,0.3)'; this.style.transform='translateY(0)'">
              <img src="${cert.badge_path}"
                   alt="${cert.title}"
                   onerror="this.src='${cert.fallback_svg}'"
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
