(function() {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
})();

function initThemeToggle() {
  const wrappers = document.querySelectorAll('.theme-toggle-btn');
  if (!wrappers.length) return;

  // Inject knob into every toggle button
  wrappers.forEach((w, i) => {
    if (i === 0) {
      w.innerHTML = `<span id="tt-knob"></span><canvas id="tt-stars"></canvas>`;
    } else {
      w.innerHTML = `<span class="tt-knob-secondary"></span>`;
    }
  });

  const primaryWrapper = wrappers[0];
  const canvas = document.getElementById('tt-stars');
  const ctx = canvas.getContext('2d');

  function sizeCanvas() {
    canvas.width  = primaryWrapper.getBoundingClientRect().width;
    canvas.height = primaryWrapper.getBoundingClientRect().height;
  }
  sizeCanvas();
  window.addEventListener('resize', sizeCanvas);

  let stars = [];
  class Star {
    constructor(x, y) {
      this.x = x; this.y = y;
      this.size = 0; this.growth = 0.06;
      this.isIncreasing = true;
    }
    update() {
      if (this.size > 1.2) this.isIncreasing = false;
      this.size += this.isIncreasing ? this.growth : -this.growth * 0.5;
      ctx.beginPath();
      ctx.arc(this.x, this.y, Math.max(0, this.size), 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.fill();
      ctx.closePath();
    }
  }

  let animFrame, starInterval;

  function startStars() {
    starInterval = setInterval(() => {
      stars.push(new Star(
        Math.random() * canvas.width,
        Math.random() * canvas.height
      ));
    }, 150);
    function flicker() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach((star, i) => {
        if (!star.isIncreasing && star.size < 0.1) stars.splice(i, 1);
        star.update();
      });
      animFrame = requestAnimationFrame(flicker);
    }
    flicker();
  }

  function stopStars() {
    clearInterval(starInterval);
    cancelAnimationFrame(animFrame);
    stars = [];
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  function getTheme() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  }

  function setTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    localStorage.setItem('theme', t);
    const isNight = (t === 'dark');
    wrappers.forEach(w => {
      w.dataset.time = isNight ? 'night' : 'day';
      w.title = isNight ? 'Switch to day' : 'Switch to night';
    });
    if (isNight) { startStars(); } else { stopStars(); }
  }

  setTheme(getTheme());

  wrappers.forEach(w => {
    w.addEventListener('click', function() {
      setTheme(getTheme() === 'dark' ? 'light' : 'dark');
    });
  });
}

function initMobileNav() {
  const hamburger = document.querySelector('.nav-hamburger');
  const overlay   = document.querySelector('.mobile-nav-overlay');
  const panel     = document.querySelector('.mobile-nav-panel');
  const closeBtn  = document.querySelector('.mobile-nav-close');
  if (!hamburger || !panel) return;

  function openPanel() {
    hamburger.classList.add('open');
    overlay.classList.add('open');
    panel.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closePanel() {
    hamburger.classList.remove('open');
    overlay.classList.remove('open');
    panel.classList.remove('open');
    document.body.style.overflow = '';
  }

  hamburger.addEventListener('click', () => {
    panel.classList.contains('open') ? closePanel() : openPanel();
  });
  if (closeBtn) closeBtn.addEventListener('click', closePanel);
  if (overlay) overlay.addEventListener('click', closePanel);
  panel.querySelectorAll('a').forEach(a => a.addEventListener('click', closePanel));
}

document.addEventListener('DOMContentLoaded', function() {
  initThemeToggle();
  initMobileNav();
});
