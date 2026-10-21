/**
 * LucentIA — diagrams.js v1.0
 * Helpers para diagramas UML con viz.js (Graphviz). Theme-aware (dark/light).
 *
 * Uso en una página:
 *   <script src="https://cdn.jsdelivr.net/npm/viz.js@2.1.2/viz.js"></script>
 *   <script src="https://cdn.jsdelivr.net/npm/viz.js@2.1.2/full.render.js"></script>
 *   <script src="[RUTA]/shared/diagrams.js" defer></script>
 *   <div class="diagram-container" id="diag1" onclick="LucentDiag.openLightbox(this)"></div>
 *   <script>
 *     LucentDiag.register('diag1', LucentDiag.dot(function(t) {
 *       return `digraph G {
 *         ${LucentDiag.gBase(t)}
 *         ${LucentDiag.cls('GeoData','purple','abstract',['+geometry'],['+method()'], t)}
 *         ${LucentDiag.cls('GeoTrajectory','blue','',['+points'],['+plot()'], t)}
 *         ${LucentDiag.inh('GeoTrajectory','GeoData')}
 *       }`;
 *     }));
 *   </script>
 *
 * El render se dispara automáticamente y se re-renderiza al cambiar tema.
 */
window.LucentDiag = (function () {
  'use strict';

  /* ── Paletas (deep para dark, pastel para light) ────────────────── */
  var PALETTE = {
    dark: {
      purple: ['#2d1b4e', '#a855f7', '#e9d5ff'],   // bg, border, text
      blue:   ['#1e3a5f', '#3b82f6', '#bfdbfe'],
      green:  ['#14532d', '#22c55e', '#bbf7d0'],
      orange: ['#7c2d12', '#f97316', '#fed7aa'],
      gray:   ['#1c1c1c', '#64748b', '#cbd5e1'],
    },
    light: {
      purple: ['#ede9fe', '#7c3aed', '#3b1f6e'],   // pastel bg, border, deep text
      blue:   ['#dbeafe', '#1d4ed8', '#1e3a5f'],
      green:  ['#d9e8dd', '#15803d', '#14532d'],
      orange: ['#f0e1c7', '#92400e', '#5a2a08'],
      gray:   ['#e7e2d4', '#525252', '#1f1810'],
    }
  };

  /* ── Tema actual ────────────────────────────────────────────────── */
  function currentTheme() {
    var t = document.documentElement.getAttribute('data-theme');
    return t === 'light' ? 'light' : 'dark';
  }

  /* ── Helpers DOT ────────────────────────────────────────────────── */
  function escHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function cls(name, palKey, stereotype, attrs, methods, theme) {
    var p = PALETTE[theme || currentTheme()][palKey] || PALETTE.dark.blue;
    var bg = p[0], border = p[1], fg = p[2];
    var stereoRow = stereotype
      ? '<TR><TD ALIGN="CENTER"><FONT COLOR="' + fg + '" FACE="Courier New" POINT-SIZE="9">&lt;&lt;' + escHtml(stereotype) + '&gt;&gt;</FONT></TD></TR>'
      : '';
    var attrRows = (attrs && attrs.length)
      ? '<TR><TD ALIGN="LEFT"><FONT COLOR="' + fg + '" FACE="Courier New" POINT-SIZE="10">' + attrs.map(function (a) { return escHtml(a) + '<BR ALIGN="LEFT"/>'; }).join('') + '</FONT></TD></TR>'
      : '<TR><TD><FONT POINT-SIZE="6"> </FONT></TD></TR>';
    var methRows = (methods && methods.length)
      ? '<TR><TD ALIGN="LEFT"><FONT COLOR="' + fg + '" FACE="Courier New" POINT-SIZE="10">' + methods.map(function (m) { return escHtml(m) + '<BR ALIGN="LEFT"/>'; }).join('') + '</FONT></TD></TR>'
      : '<TR><TD><FONT POINT-SIZE="6"> </FONT></TD></TR>';
    return '"' + name + '" [shape=none, margin=0, label=<\n' +
      '<TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="7" BGCOLOR="' + bg + '" COLOR="' + border + '">\n' +
      '<TR><TD ALIGN="CENTER"><FONT COLOR="' + fg + '" FACE="Courier New"><B>' + escHtml(name) + '</B></FONT></TD></TR>\n' +
      stereoRow + attrRows + methRows + '</TABLE>>]';
  }

  function gBase(theme) {
    var t = theme || currentTheme();
    var edgeCol = t === 'light' ? '#525252' : '#6b7280';
    var labelCol = t === 'light' ? '#4a3f2c' : '#94a3b8';
    return 'bgcolor="transparent"\n' +
      '    node [shape=none, margin=0]\n' +
      '    edge [color="' + edgeCol + '", fontsize=9, fontcolor="' + labelCol + '", fontname="Courier New"]';
  }

  function inh(from, to)       { var c = currentTheme() === 'light' ? '#7c3aed' : '#a78bfa'; return '"' + from + '" -> "' + to + '" [arrowhead=onormal, color="' + c + '", penwidth=1.5]'; }
  function comp(from, to, lbl) { var c = currentTheme() === 'light' ? '#1d4ed8' : '#60a5fa'; return '"' + from + '" -> "' + to + '" [arrowhead=diamond, color="' + c + '"' + (lbl ? ', label="' + lbl + '"' : '') + ', penwidth=1.5]'; }
  function agg(from, to, lbl)  { var c = currentTheme() === 'light' ? '#1d4ed8' : '#60a5fa'; return '"' + from + '" -> "' + to + '" [arrowhead=odiamond, color="' + c + '"' + (lbl ? ', label="' + lbl + '"' : '') + ', penwidth=1.5]'; }
  function dep(from, to, lbl)  { var c = currentTheme() === 'light' ? '#525252' : '#64748b'; return '"' + from + '" -> "' + to + '" [style=dashed, arrowhead=vee, color="' + c + '"' + (lbl ? ', label="' + lbl + '"' : '') + ']'; }

  /* ── Render registry + ejecutor ─────────────────────────────────── */
  var registry = {};   // id → function(theme)→DOT string

  function dot(fn) { return fn; }   // sugar — declarativo

  function register(id, dotFn) {
    registry[id] = dotFn;
    renderOne(id);
  }

  function renderOne(id) {
    if (typeof Viz === 'undefined') return;       // CDN aún no cargado
    var container = document.getElementById(id);
    var fn = registry[id];
    if (!container || !fn) return;
    var src = fn(currentTheme());
    var viz = new Viz();
    viz.renderSVGElement(src)
      .then(function (svg) {
        svg.style.cssText = 'display:inline-block;max-width:100%;height:auto';
        container.innerHTML = '';
        container.appendChild(svg);
      })
      .catch(function (err) {
        container.innerHTML = '<p style="color:#f87171;padding:1rem;font-family:monospace">Error en ' + id + ': ' + err.message + '</p>';
      });
  }

  function renderAll() { Object.keys(registry).forEach(renderOne); }

  /* ── Lightbox ───────────────────────────────────────────────────── */
  var _open = null;
  function openLightbox(el) {
    var c = el.closest ? el.closest('.diagram-container') || el : el;
    if (!c) return;
    _open = c;
    c.classList.add('lightbox-open');
    var btn = document.getElementById('lightbox-close');
    if (btn) btn.classList.add('visible');
    document.body.style.overflow = 'hidden';
  }
  function closeLightbox() {
    if (_open) { _open.classList.remove('lightbox-open'); _open = null; }
    var btn = document.getElementById('lightbox-close');
    if (btn) btn.classList.remove('visible');
    document.body.style.overflow = '';
  }

  /* ── Init ───────────────────────────────────────────────────────── */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeLightbox();
  });
  document.addEventListener('click', function (e) {
    if (_open && e.target === _open) closeLightbox();
  });

  // Re-render al cambiar tema (observer sobre data-theme del <html>)
  var observer = new MutationObserver(function () { renderAll(); });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  // Render inicial cuando viz.js esté listo
  function whenVizReady(cb) {
    if (typeof Viz !== 'undefined') return cb();
    var i = setInterval(function () {
      if (typeof Viz !== 'undefined') { clearInterval(i); cb(); }
    }, 50);
  }
  document.addEventListener('DOMContentLoaded', function () { whenVizReady(renderAll); });

  return {
    cls: cls, gBase: gBase,
    inh: inh, comp: comp, agg: agg, dep: dep,
    register: register, renderAll: renderAll, dot: dot,
    openLightbox: openLightbox, closeLightbox: closeLightbox,
    PALETTE: PALETTE
  };
})();

// Aliases globales para inline onclick (compatibilidad)
function openDiagram(el) { window.LucentDiag.openLightbox(el); }
function closeDiagram()  { window.LucentDiag.closeLightbox(); }
