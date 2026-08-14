/* ============================================================
   InfoLab · 核心脚本
   原则：所有内容默认可见；JS 只做增强，绝不控制显隐。
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 侧栏当前项高亮 ---------- */
  function initScrollSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll('.side a[href^="#"]'));
    if (!links.length) return;
    var targets = links.map(function (a) {
      var el = document.getElementById(a.getAttribute('href').slice(1));
      return el ? { a: a, el: el } : null;
    }).filter(Boolean);
    if (!targets.length) return;

    function spy() {
      var y = window.scrollY + 110, cur = targets[0];
      for (var i = 0; i < targets.length; i++) {
        if (targets[i].el.offsetTop <= y) cur = targets[i];
      }
      links.forEach(function (a) { a.classList.remove('act'); });
      cur.a.classList.add('act');
    }
    var tick = false;
    window.addEventListener('scroll', function () {
      if (tick) return;
      tick = true;
      requestAnimationFrame(function () { spy(); tick = false; });
    }, { passive: true });
    spy();
  }

  /* ---------- 数学工具 ---------- */
  var M = {
    log2: function (x) { return Math.log(x) / Math.LN2; },
    // 二元熵 H(p)，单位 bit
    h2: function (p) {
      if (p <= 0 || p >= 1) return 0;
      return -p * M.log2(p) - (1 - p) * M.log2(1 - p);
    },
    // 离散熵
    H: function (ps) {
      var s = 0;
      for (var i = 0; i < ps.length; i++) {
        if (ps[i] > 0) s -= ps[i] * M.log2(ps[i]);
      }
      return s;
    },
    fmt: function (x, n) {
      if (!isFinite(x)) return '—';
      return x.toFixed(n === undefined ? 4 : n);
    }
  };
  window.ILMath = M;

  /* ---------- 画布助手：带坐标轴的函数图 ---------- */
  function Plot(canvas, opt) {
    opt = opt || {};
    this.c = canvas;
    this.ctx = canvas.getContext('2d');
    this.pad = opt.pad || { l: 52, r: 16, t: 16, b: 38 };
    this.xr = opt.xr || [0, 1];
    this.yr = opt.yr || [0, 1];
    this.xlabel = opt.xlabel || '';
    this.ylabel = opt.ylabel || '';
    this.resize();
  }
  Plot.prototype.resize = function () {
    var dpr = window.devicePixelRatio || 1;
    var w = this.c.clientWidth || 600;
    var h = this.c.getAttribute('data-h') ? +this.c.getAttribute('data-h') : 260;
    this.c.width = w * dpr;
    this.c.height = h * dpr;
    this.c.style.height = h + 'px';
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.w = w; this.h = h;
  };
  Plot.prototype.px = function (x) {
    var p = this.pad;
    return p.l + (x - this.xr[0]) / (this.xr[1] - this.xr[0]) * (this.w - p.l - p.r);
  };
  Plot.prototype.py = function (y) {
    var p = this.pad;
    return this.h - p.b - (y - this.yr[0]) / (this.yr[1] - this.yr[0]) * (this.h - p.t - p.b);
  };
  Plot.prototype.clear = function () {
    var x = this.ctx;
    x.clearRect(0, 0, this.w, this.h);
    x.fillStyle = '#0d1220';
    x.fillRect(0, 0, this.w, this.h);
  };
  Plot.prototype.axes = function (xt, yt) {
    var x = this.ctx, p = this.pad, i;
    x.strokeStyle = '#26304a'; x.lineWidth = 1;
    x.fillStyle = '#8592ab';
    x.font = '10px ui-monospace,Menlo,monospace';

    xt = xt || 5; yt = yt || 5;
    // 网格 + 刻度
    for (i = 0; i <= xt; i++) {
      var xv = this.xr[0] + (this.xr[1] - this.xr[0]) * i / xt;
      var X = this.px(xv);
      x.globalAlpha = .35;
      x.beginPath(); x.moveTo(X, p.t); x.lineTo(X, this.h - p.b); x.stroke();
      x.globalAlpha = 1;
      x.textAlign = 'center'; x.textBaseline = 'top';
      x.fillText(this._n(xv), X, this.h - p.b + 7);
    }
    for (i = 0; i <= yt; i++) {
      var yv = this.yr[0] + (this.yr[1] - this.yr[0]) * i / yt;
      var Y = this.py(yv);
      x.globalAlpha = .35;
      x.beginPath(); x.moveTo(p.l, Y); x.lineTo(this.w - p.r, Y); x.stroke();
      x.globalAlpha = 1;
      x.textAlign = 'right'; x.textBaseline = 'middle';
      x.fillText(this._n(yv), p.l - 8, Y);
    }
    // 轴线
    x.strokeStyle = '#3a4763'; x.lineWidth = 1.4;
    x.beginPath();
    x.moveTo(p.l, p.t); x.lineTo(p.l, this.h - p.b); x.lineTo(this.w - p.r, this.h - p.b);
    x.stroke();
    // 轴标签
    x.fillStyle = '#b8c2d6'; x.font = '11px ui-monospace,Menlo,monospace';
    if (this.xlabel) { x.textAlign = 'center'; x.textBaseline = 'bottom'; x.fillText(this.xlabel, (p.l + this.w - p.r) / 2, this.h - 2); }
    if (this.ylabel) {
      x.save(); x.translate(11, (p.t + this.h - p.b) / 2); x.rotate(-Math.PI / 2);
      x.textAlign = 'center'; x.textBaseline = 'top'; x.fillText(this.ylabel, 0, 0); x.restore();
    }
  };
  Plot.prototype._n = function (v) {
    if (Math.abs(v) >= 100) return v.toFixed(0);
    if (Math.abs(v - Math.round(v)) < 1e-9) return String(Math.round(v));
    return v.toFixed(Math.abs(v) < 1 ? 2 : 1);
  };
  Plot.prototype.line = function (fn, color, width) {
    var x = this.ctx, p = this.pad, started = false;
    x.strokeStyle = color || '#38bdf8'; x.lineWidth = width || 2;
    x.beginPath();
    var N = 260;
    for (var i = 0; i <= N; i++) {
      var xv = this.xr[0] + (this.xr[1] - this.xr[0]) * i / N;
      var yv = fn(xv);
      if (!isFinite(yv)) { started = false; continue; }
      yv = Math.max(this.yr[0], Math.min(this.yr[1], yv));
      var X = this.px(xv), Y = this.py(yv);
      if (!started) { x.moveTo(X, Y); started = true; } else { x.lineTo(X, Y); }
    }
    x.stroke();
  };
  Plot.prototype.dot = function (xv, yv, color, label) {
    var x = this.ctx;
    var X = this.px(xv), Y = this.py(Math.max(this.yr[0], Math.min(this.yr[1], yv)));
    x.fillStyle = color || '#f472b6';
    x.beginPath(); x.arc(X, Y, 4.5, 0, Math.PI * 2); x.fill();
    x.strokeStyle = '#0d1220'; x.lineWidth = 1.5; x.stroke();
    if (label) {
      x.fillStyle = '#e8edf7'; x.font = '10.5px ui-monospace,Menlo,monospace';
      x.textAlign = 'left'; x.textBaseline = 'bottom';
      x.fillText(label, X + 8, Y - 5);
    }
  };
  Plot.prototype.vline = function (xv, color, dash) {
    var x = this.ctx, p = this.pad;
    x.save();
    x.strokeStyle = color || '#8592ab'; x.lineWidth = 1.2;
    if (dash !== false) x.setLineDash([4, 4]);
    x.beginPath(); x.moveTo(this.px(xv), p.t); x.lineTo(this.px(xv), this.h - p.b); x.stroke();
    x.restore();
  };
  Plot.prototype.bars = function (vals, colors) {
    var x = this.ctx, p = this.pad, n = vals.length;
    var bw = (this.w - p.l - p.r) / n;
    for (var i = 0; i < n; i++) {
      var X = p.l + i * bw, Y = this.py(vals[i]);
      x.fillStyle = (colors && colors[i]) || '#38bdf8';
      x.fillRect(X + bw * .18, Y, bw * .64, this.h - p.b - Y);
    }
  };
  window.ILPlot = Plot;

  /* ---------- 滑块绑定助手 ---------- */
  window.ILBind = function (ids, render) {
    var els = ids.map(function (id) { return document.getElementById(id); }).filter(Boolean);
    if (els.length !== ids.length) return;
    function go() { render(); }
    els.forEach(function (el) {
      el.addEventListener('input', go);
      el.addEventListener('change', go);
    });
    go();
    window.addEventListener('resize', function () {
      clearTimeout(window.__ilrz);
      window.__ilrz = setTimeout(go, 160);
    });
  };

  /* ---------- 启动 ---------- */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollSpy);
  } else {
    initScrollSpy();
  }
})();
