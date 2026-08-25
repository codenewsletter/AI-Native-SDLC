/* The AI-Native SDLC — page behaviour.
   No dependencies. Every feature degrades to a readable page if it fails. */
(function () {
  'use strict';

  /* --- copy buttons -------------------------------------- */
  /* The async Clipboard API rejects with NotAllowedError inside a sandboxed
     iframe (the page is embedded that way in previews), so execCommand is a
     real fallback here, not legacy politeness. If both fail the button says
     so rather than silently pretending it worked. */
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var pre = btn.parentElement.querySelector('pre');
      if (!pre) return;
      var text = pre.innerText;

      var done = function (ok) {
        btn.textContent = ok ? 'Copied' : 'Press \u2318C';
        btn.dataset.state = ok ? 'done' : 'manual';
        if (!ok) select(pre);
        setTimeout(function () {
          btn.textContent = 'Copy';
          delete btn.dataset.state;
        }, ok ? 1600 : 3000);
      };

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () { done(true); },
          function () { done(execCopy(text)); }
        );
      } else {
        done(execCopy(text));
      }
    });
  });

  /* Copies via a throwaway textarea. Returns whether it actually worked,
     and puts the user's own selection back when it is finished. */
  function execCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:0;left:-9999px;opacity:0';
    document.body.appendChild(ta);

    var sel = window.getSelection();
    var previous = sel && sel.rangeCount ? sel.getRangeAt(0) : null;

    var ok = false;
    try {
      ta.select();
      ta.setSelectionRange(0, text.length);
      ok = document.execCommand('copy');
    } catch (e) {
      ok = false;
    }

    document.body.removeChild(ta);
    if (sel) {
      sel.removeAllRanges();
      if (previous) sel.addRange(previous);
    }
    return ok;
  }

  function select(pre) {
    var r = document.createRange();
    r.selectNodeContents(pre);
    var s = window.getSelection();
    s.removeAllRanges();
    s.addRange(r);
  }

  /* --- reading progress --------------------------------- */
  var bar = document.getElementById('progress');
  if (bar) {
    var tick = false;
    var paint = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var pct = h > 0 ? (window.scrollY / h) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, pct)) + '%';
      tick = false;
    };
    window.addEventListener('scroll', function () {
      if (!tick) { tick = true; requestAnimationFrame(paint); }
    }, { passive: true });
    paint();
  }

  /* --- rail scrollspy ----------------------------------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('#rail-list a'));
  if (links.length) {
    var pairs = links.map(function (a) {
      return { link: a, el: document.querySelector(a.getAttribute('href')) };
    }).filter(function (p) { return p.el; });

    // the last section whose heading has passed the reading line is the one
    // being read; near the document end the final section always wins, so a
    // short last section still gets highlighted
    var LINE = 140;
    var spy = function () {
      var atEnd = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4;
      var current = pairs[0];
      if (atEnd) {
        current = pairs[pairs.length - 1];
      } else {
        pairs.forEach(function (p) {
          if (p.el.getBoundingClientRect().top <= LINE) current = p;
        });
      }
      pairs.forEach(function (p) {
        if (p === current) p.link.setAttribute('aria-current', 'true');
        else p.link.removeAttribute('aria-current');
      });
    };

    var pending = false;
    var onScroll = function () {
      if (pending) return;
      pending = true;
      requestAnimationFrame(function () { pending = false; spy(); });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    spy();
  }

  /* --- horizontal-scroll affordance on wide diagrams ----- */
  document.querySelectorAll('.scroller').forEach(function (el) {
    var sync = function () {
      var over = el.scrollWidth - el.clientWidth;
      el.classList.toggle('is-scrollable', over > 4);
      el.classList.toggle('is-end', over <= 4 || el.scrollLeft >= over - 4);
    };
    el.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    if (window.ResizeObserver) new ResizeObserver(sync).observe(el);
    sync();
  });

  /* --- scorecard ---------------------------------------- */
  var card = document.getElementById('scorecard');
  if (card) {
    var KEY = 'the-code.ai-native-sdlc.score.v1';
    var items = Array.prototype.slice.call(card.querySelectorAll('.score__item'));
    var num = document.getElementById('score-num');
    var verdict = document.getElementById('score-verdict');
    var live = document.getElementById('score-live');
    var reset = document.getElementById('score-reset');

    var read = function () {
      try {
        var raw = localStorage.getItem(KEY);
        return raw ? JSON.parse(raw) : [];
      } catch (e) { return []; }
    };
    var write = function (state) {
      try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* private mode */ }
    };

    var verdictFor = function (n) {
      if (n <= 3) return 'Your AI gains are sitting in a review queue right now. Start Week 1 today.';
      if (n <= 6) return 'Your gap is enforcement. Do the Decision 04 sort.';
      return 'You’re ahead of most teams on this page. Tell us what you learned: thecode@joinsuperhuman.io';
    };

    var touched = false;
    var PROMPT = verdict.textContent;   // the neutral "tap the items" line from the markup

    var render = function (announce) {
      var n = items.filter(function (b) { return b.getAttribute('aria-pressed') === 'true'; }).length;
      num.textContent = n + ' / ' + items.length;
      // a score of zero before anyone has answered is not a verdict, it is an empty form
      verdict.textContent = (!touched && n === 0) ? PROMPT : verdictFor(n);
      if (announce && live) live.textContent = n + ' of ' + items.length + '. ' + verdict.textContent;
    };

    var saved = read();
    if (saved.length) touched = true;
    items.forEach(function (btn, i) {
      if (saved.indexOf(i) !== -1) btn.setAttribute('aria-pressed', 'true');
      btn.addEventListener('click', function () {
        var on = btn.getAttribute('aria-pressed') === 'true';
        btn.setAttribute('aria-pressed', on ? 'false' : 'true');
        touched = true;
        write(items.reduce(function (acc, b, j) {
          if (b.getAttribute('aria-pressed') === 'true') acc.push(j);
          return acc;
        }, []));
        render(true);
      });
    });

    if (reset) {
      reset.addEventListener('click', function () {
        items.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        write([]);
        touched = false;
        render(true);
      });
    }

    render(false);
  }
})();
