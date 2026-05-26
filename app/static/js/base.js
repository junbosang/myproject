/**
 * cnAgentOS - Base JavaScript Utilities
 */
(function() {
  'use strict';

  /* --- Sidebar toggle --- */
  function initSidebar() {
    var sidebar = document.querySelector('.sidebar');
    var toggleBtn = document.querySelector('.sidebar-toggle');
    if (!sidebar || !toggleBtn) return;

    // Restore state
    var collapsed = localStorage.getItem('sidebar_collapsed') === '1';
    if (collapsed) sidebar.classList.add('collapsed');

    toggleBtn.addEventListener('click', function() {
      sidebar.classList.toggle('collapsed');
      localStorage.setItem('sidebar_collapsed', sidebar.classList.contains('collapsed') ? '1' : '0');
    });
  }

  /* --- Modal helpers --- */
  window.openModal = function(id) {
    var el = document.getElementById(id);
    if (el) el.style.display = 'flex';
  };
  window.closeModal = function(id) {
    var el = document.getElementById(id);
    if (el) el.style.display = 'none';
  };

  /* Click outside modal to close */
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
      e.target.style.display = 'none';
    }
  });

  /* --- Toast notifications --- */
  window.showToast = function(msg, type) {
    type = type || 'info';
    var container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    var icons = { success: 'fa-check-circle', error: 'fa-times-circle', warning: 'fa-exclamation-triangle', info: 'fa-info-circle' };
    toast.innerHTML = '<i class="fas ' + (icons[type] || icons.info) + '"></i> ' + msg;
    container.appendChild(toast);
    setTimeout(function() {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s';
      setTimeout(function() { toast.remove(); }, 300);
    }, 3000);
  };

  /* --- Active menu item highlight --- */
  function highlightMenu() {
    var path = window.location.pathname;
    var items = document.querySelectorAll('.menu-item');
    var best = null, bestLen = 0;
    items.forEach(function(item) {
      var href = item.getAttribute('href') || item.getAttribute('data-href') || '';
      if (href && path.startsWith(href) && href.length > bestLen) {
        best = item; bestLen = href.length;
      }
    });
    if (best) best.classList.add('active');
  }

  /* --- Chat tab switching --- */
  window.switchChatTab = function(tab) {
    document.querySelectorAll('.chat-tab').forEach(function(t) { t.classList.remove('active'); });
    document.getElementById('tab-' + tab).classList.add('active');
    document.querySelectorAll('.chat-tab-content').forEach(function(c) { c.style.display = 'none'; });
    var target = document.getElementById('list-' + tab);
    if (target) target.style.display = 'block';
  };

  /* --- Init on DOM ready --- */
  document.addEventListener('DOMContentLoaded', function() {
    initSidebar();
    highlightMenu();
  });

  console.log('cnAgentOS v2.0 - system ready');
})();
