(function() {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
})();

function initThemeToggle() {
  const wrapper = document.getElementById('theme-toggle');
  if (!wrapper) return;

  wrapper.innerHTML = `
    <span id="tt-knob"></span>
    <canvas id="tt-stars"></canvas>
  `;

  const canvas = document.getElementById('tt-stars');
  const ctx = canvas.getContext('2d');

  function sizeCanvas() {
    canvas.width  = wrapper.getBoundingClientRect().width;
    canvas.height = wrapper.getBoundingClientRect().height;
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

  let animFrame;
  let starInterval;
  let isNight = false;

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
    isNight = (t === 'dark');
    wrapper.dataset.time = isNight ? 'night' : 'day';
    wrapper.title = isNight ? 'Switch to day' : 'Switch to night';
    if (isNight) { startStars(); } else { stopStars(); }
  }

  setTheme(getTheme());

  wrapper.addEventListener('click', function() {
    setTheme(getTheme() === 'dark' ? 'light' : 'dark');
  });
}

document.addEventListener('DOMContentLoaded', initThemeToggle);
