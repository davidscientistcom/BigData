/**
 * LucentIA — lucentia.js v2.0
 * Funciones compartidas: tema dark/light, sidebar responsive, copy code.
 * Referencia en todos los HTML con:  <script src="[RUTA]/shared/lucentia.js" defer></script>
 * El script anti-flash (3 líneas) sigue siendo inline en cada <head> para evitar FOUC.
 */

/* ── TEMA ─────────────────────────────────────────────────────── */
function toggleTheme() {
  var html    = document.documentElement;
  var current = html.getAttribute('data-theme') || 'dark';
  var next    = current === 'light' ? 'dark' : 'light';
  html.setAttribute('data-theme', next);
  localStorage.setItem('lucentia-theme', next);
  _updateThemeBtn(next);
  _rerenderMermaid(next);
}

/* Re-renderiza todos los diagramas Mermaid con el nuevo tema */
function _rerenderMermaid(theme) {
  if (typeof mermaid === 'undefined') return;
  var dark = theme !== 'light';
  mermaid.initialize({
    startOnLoad: false, securityLevel: 'loose',
    flowchart: { htmlLabels: false },
    theme: dark ? 'dark' : 'default',
  });
  /* Restaurar <pre class="mermaid"> desde el source guardado, luego re-renderizar */
  document.querySelectorAll('[data-mermaid-src]').forEach(function(container) {
    var src = container.getAttribute('data-mermaid-src');
    var svg = container.querySelector('svg');
    if (svg && src) {
      var pre = document.createElement('pre');
      pre.className = 'mermaid';
      pre.textContent = src;
      svg.replaceWith(pre);
    }
  });
  var pending = document.querySelectorAll('.mermaid');
  if (pending.length) mermaid.run({ querySelector: '.mermaid' });
}

function _updateThemeBtn(theme) {
  var icon  = document.getElementById('themeIcon');
  var label = document.getElementById('themeLabel');
  if (!icon || !label) return;
  icon.textContent  = theme === 'light' ? '\uD83C\uDF19' : '\u2600';   /* 🌙 : ☀ */
  label.textContent = theme === 'light' ? 'Modo oscuro' : 'Modo claro';
}

/* ── SIDEBAR ──────────────────────────────────────────────────── */
function toggleSidebar() {
  var sidebar = document.getElementById('sidebar');
  var overlay = document.getElementById('sidebarOverlay');
  var btn     = document.getElementById('sidebarToggle');
  if (!sidebar) return;

  var isOpen = sidebar.classList.contains('open');
  if (isOpen) {
    sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
    if (btn)     btn.setAttribute('aria-expanded', 'false');
  } else {
    sidebar.classList.add('open');
    if (overlay) overlay.classList.add('active');
    if (btn)     btn.setAttribute('aria-expanded', 'true');
  }
}

/* Cierra la sidebar al hacer clic en un enlace interno (mobile) */
function _closeSidebarOnMobile() {
  if (window.innerWidth < 1100) {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebarOverlay');
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('active');
  }
}

/* ── COPY CODE ────────────────────────────────────────────────── */
function copyCode(btn) {
  var block = btn.closest('.code-block');
  if (!block) return;
  var pre = block.querySelector('pre');
  if (!pre) return;
  navigator.clipboard.writeText(pre.innerText).then(function () {
    btn.textContent = 'Copiado';
    setTimeout(function () { btn.textContent = 'Copiar'; }, 2000);
  });
}

/* ── INIT ─────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', function () {
  /* Sincroniza el botón de tema con el estado guardado */
  var saved = localStorage.getItem('lucentia-theme') || 'dark';
  _updateThemeBtn(saved);

  /* Cierra sidebar al navegar (mobile) */
  var links = document.querySelectorAll('.sidebar a, .sidebar-nav a');
  links.forEach(function (link) {
    link.addEventListener('click', _closeSidebarOnMobile);
  });

  /* Cierra sidebar con Escape */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      var sidebar = document.getElementById('sidebar');
      if (sidebar && sidebar.classList.contains('open')) toggleSidebar();
    }
  });

  /* Lleva el capítulo activo a la vista dentro del sidebar al cargar la
     página — sin esto, cada navegación reinicia el scroll del menú a
     arriba y hay que bajarlo a mano en cursos largos. */
  var activeLink = document.querySelector('.sidebar a.active');
  if (activeLink) {
    activeLink.scrollIntoView({ block: 'center' });
  }
});

/* ── TABS (Ejercicios Resueltos vs Lección) ───────────────────── */
function switchTab(tabId, btn) {
  var container = btn.closest('.tabs-container') || document;
  
  // Ocultar todos los tab-content
  var contents = container.querySelectorAll('.tab-content');
  contents.forEach(function(content) {
    content.style.display = 'none';
    content.classList.remove('active');
  });
  
  // Quitar 'active' de todos los botones
  var buttons = container.querySelectorAll('.tab-btn');
  buttons.forEach(function(b) {
    b.classList.remove('active');
  });
  
  // Activar tab target
  var target = document.getElementById(tabId);
  if (target) {
    target.style.display = 'block';
    target.classList.add('active');
  }
  
  // Activar botón
  btn.classList.add('active');
}

/* ── LIGHTBOX — modal real en body (evita problemas de stacking/overflow) ── */
var _lightboxModal = null;
function openLightbox(el) {
  if (_lightboxModal) { closeLightbox(); return; }
  var container = el.closest ? el.closest('.diagram-container') || el : el;
  if (!container) return;
  var svg = container.querySelector('svg');
  if (!svg) return;
  var modal = document.createElement('div');
  modal.id = '_lucent-lb';
  var isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  var lbBg  = isDark ? 'rgba(12,10,7,0.95)' : 'rgba(243,236,220,0.97)';
  modal.style.cssText = 'position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:' + lbBg + ';cursor:zoom-out;padding:2rem;box-sizing:border-box';
  var clone = svg.cloneNode(true);
  clone.removeAttribute('width');
  clone.removeAttribute('height');
  clone.style.cssText = 'max-width:92vw;max-height:88vh;width:auto;height:auto;cursor:default';
  modal.appendChild(clone);
  modal.addEventListener('click', function(e) { if (e.target === modal) closeLightbox(); });
  document.body.appendChild(modal);
  document.body.style.overflow = 'hidden';
  _lightboxModal = modal;
  var btn = document.getElementById('lightbox-close');
  if (btn) btn.classList.add('visible');
}
function closeLightbox() {
  if (_lightboxModal) { document.body.removeChild(_lightboxModal); _lightboxModal = null; }
  document.body.style.overflow = '';
  var btn = document.getElementById('lightbox-close');
  if (btn) btn.classList.remove('visible');
}
document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeLightbox(); });
