/* ==========================================================================
   SANTOSH GASTRO GYNAE CLINIC — site behaviour
   1. Header state   2. Mobile drawer   3. Reveal on scroll
   4. Accordion      5. Testimonial scroller   6. Back to top
   ========================================================================== */

(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.remove('no-js');
  root.classList.add('js');

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }


  /* 1. Header state -------------------------------------------------------- */

  var header = $('.sg-header');
  var toTop = $('.sg-float__top');

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) { header.classList.toggle('is-scrolled', y > 12); }
    if (toTop) { toTop.classList.toggle('show', y > 700); }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();


  /* 2. Mobile drawer ------------------------------------------------------- */

  var drawerWrap = $('.sg-drawer-wrap');
  var burger = $('.sg-burger');
  var lastFocus = null;

  function setDrawer(open) {
    if (!drawerWrap) { return; }
    drawerWrap.classList.toggle('open', open);
    drawerWrap.setAttribute('aria-hidden', open ? 'false' : 'true');
    if (burger) { burger.setAttribute('aria-expanded', open ? 'true' : 'false'); }
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) {
      lastFocus = document.activeElement;
      var close = $('.sg-drawer__close', drawerWrap);
      if (close) { close.focus(); }
    } else if (lastFocus) {
      lastFocus.focus();
    }
  }

  if (drawerWrap) {
    drawerWrap.setAttribute('aria-hidden', 'true');
    if (burger) { burger.addEventListener('click', function () { setDrawer(true); }); }
    $('.sg-overlay', drawerWrap).addEventListener('click', function () { setDrawer(false); });
    $('.sg-drawer__close', drawerWrap).addEventListener('click', function () { setDrawer(false); });
    $$('a', drawerWrap).forEach(function (a) {
      a.addEventListener('click', function () { setDrawer(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawerWrap.classList.contains('open')) { setDrawer(false); }
    });
  }


  /* 3. Reveal on scroll ---------------------------------------------------- */

  var risers = $$('[data-rise]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    risers.forEach(function (el) { io.observe(el); });
  } else {
    risers.forEach(function (el) { el.classList.add('in'); });
  }


  /* 4. Accordion ----------------------------------------------------------- */

  function setAc(item, open) {
    var btn = $('.sg-ac__q', item);
    var answer = $('.sg-ac__a', item);
    item.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    answer.style.maxHeight = open ? answer.scrollHeight + 'px' : null;
  }

  $$('.sg-ac').forEach(function (item) {
    var btn = $('.sg-ac__q', item);
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function () {
      setAc(item, !item.classList.contains('open'));
    });
  });

  /* Open the question named in the URL hash (links from the home page). */
  function openFromHash() {
    if (!location.hash) { return; }
    var target = document.getElementById(location.hash.slice(1));
    if (target && target.classList.contains('sg-ac')) {
      setAc(target, true);
      setTimeout(function () { target.scrollIntoView({ block: 'start' }); }, 60);
    }
  }
  openFromHash();
  window.addEventListener('hashchange', openFromHash);


  /* 5. Testimonial scroller ------------------------------------------------ */

  $$('[data-quotes]').forEach(function (wrap) {
    var track = $('.sg-quotes', wrap);
    var prev = $('[data-prev]', wrap);
    var next = $('[data-next]', wrap);
    function step(dir) {
      var card = $('.sg-quote', track);
      var w = card ? card.getBoundingClientRect().width + 20 : 320;
      track.scrollBy({ left: dir * w, behavior: 'smooth' });
    }
    if (prev) { prev.addEventListener('click', function () { step(-1); }); }
    if (next) { next.addEventListener('click', function () { step(1); }); }
  });


  /* 6. Back to top --------------------------------------------------------- */

  if (toTop) {
    toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }

  var year = $('[data-year]');
  if (year) { year.textContent = new Date().getFullYear(); }
}());
