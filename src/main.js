// Behaviour port of the reference (framer-motion + next-themes + React state), in vanilla JS.
const EASE = 'cubic-bezier(0.22, 1, 0.36, 1)';
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const NAV = [
  ['Profile', '#about'],
  ['Stack', '#skills'],
  ['Experience', '#experience'],
  ['Work', '#projects'],
  ['Contact', '#contact'],
];

const animate = (el, from, to, duration, delay = 0) => {
  if (reduced) {
    Object.assign(el.style, to);
    return;
  }
  el.style.transition = 'none';
  Object.assign(el.style, from);
  el.getBoundingClientRect();
  el.style.transition = Object.keys(to).map((k) => `${k === 'transform' ? 'transform' : k} ${duration}s ${EASE} ${delay}s`).join(',');
  Object.assign(el.style, to);
};

const onceInView = (el, margin, cb) => {
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) {
      io.disconnect();
      cb();
    }
  }, { rootMargin: `0px 0px -${margin}px 0px` });
  io.observe(el);
};

// Reveal / hero fades
document.querySelectorAll('[style*="opacity:0"]').forEach((el) => {
  const inHero = el.closest('#hero');
  const y16 = el.style.transform.includes('16px');
  const rest = { opacity: '1', transform: 'translateY(0px)' };
  if (inHero && y16) {
    const delays = [0.1, 0.55, 0.7, 0.85];
    const order = [...document.querySelectorAll('#hero [style*="opacity:0"]')].indexOf(el);
    animate(el, { opacity: '0', transform: 'translateY(16px)' }, rest, 0.8, delays[order] ?? 0.1);
  } else {
    if (reduced) { Object.assign(el.style, rest); return; }
    onceInView(el, 80, () => animate(el, { opacity: '0', transform: 'translateY(24px)' }, rest, 0.7));
  }
});

// Masked line reveals (h1 and contact email)
document.querySelectorAll('.overflow-hidden > .will-change-transform').forEach((el) => {
  const group = el.parentElement.parentElement;
  const idx = [...group.children].indexOf(el.parentElement);
  const isHero = !!el.closest('#hero');
  const delay = (isHero ? 0.25 : 0) + idx * 0.09;
  const run = () => animate(el, { transform: 'translateY(112%)' }, { transform: 'translateY(0%)' }, 0.8, delay);
  if (reduced) { el.style.transform = 'none'; return; }
  onceInView(group, 60, run);
});

// Header scroll state
const header = document.querySelector('header');
const SCROLLED = ['border-line', 'bg-bg/85', 'backdrop-blur-md'];
const TOP = ['border-transparent', 'bg-transparent'];
let menuOpen = false;
const syncHeader = () => {
  const scrolled = window.scrollY > 8 && !menuOpen;
  SCROLLED.forEach((c) => header.classList.toggle(c, scrolled));
  TOP.forEach((c) => header.classList.toggle(c, !scrolled));
};
syncHeader();
window.addEventListener('scroll', syncHeader, { passive: true });

// Active section
let active = '';
const navLinks = [...document.querySelectorAll('header nav .md\\:flex a')];
const setActive = (hash) => {
  active = hash;
  navLinks.forEach((a) => {
    const on = a.getAttribute('href') === hash;
    a.classList.toggle('is-drawn', on);
    a.classList.toggle('text-accent', on);
    a.classList.toggle('text-muted', !on);
    a.classList.toggle('hover:text-ink', !on);
  });
  document.querySelectorAll('#mobile-menu a').forEach((a) => {
    const on = a.getAttribute('href') === hash;
    a.classList.toggle('text-accent', on);
    a.classList.toggle('text-ink', !on);
  });
};
const sections = NAV.map(([, h]) => document.querySelector(h));
const spy = new IntersectionObserver((entries) => {
  entries.forEach((e) => e.isIntersecting && setActive(`#${e.target.id}`));
}, { rootMargin: '-40% 0px -55% 0px' });
sections.forEach((s) => s && spy.observe(s));

// Theme toggle (next-themes: class on <html>, key "sb-theme", default dark)
const root = document.documentElement;
const theme = () => (root.classList.contains('dark') ? 'dark' : 'light');
const applyTheme = (t) => {
  root.classList.remove('light', 'dark');
  root.classList.add(t);
  root.style.colorScheme = t;
  try { localStorage.setItem('sb-theme', t); } catch (e) { /* ignore */ }
  themeButtons.forEach(paintTheme);
};
const paintTheme = (b) => {
  const next = theme() === 'dark' ? 'light' : 'dark';
  b.setAttribute('aria-label', `Switch to ${next} theme`);
  b.textContent = next === 'dark' ? 'Dark' : 'Light';
};
const themeButtons = [];
document.querySelectorAll('header .text-label.inline-block.w-10').forEach((span) => {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'text-label link-underline text-muted transition-colors hover:text-ink';
  b.addEventListener('click', () => applyTheme(theme() === 'dark' ? 'light' : 'dark'));
  paintTheme(b);
  themeButtons.push(b);
  span.replaceWith(b);
});

// Mobile menu
const menuBtn = document.querySelector('header button[aria-expanded]');
let overlay = null;
const closeMenu = () => {
  if (!menuOpen) return;
  menuOpen = false;
  menuBtn.setAttribute('aria-expanded', 'false');
  menuBtn.setAttribute('aria-label', 'Open menu');
  menuBtn.textContent = 'Menu';
  document.body.style.overflow = '';
  document.querySelector('main').inert = false;
  window.removeEventListener('keydown', menuKey);
  menuBtn.focus();
  const o = overlay;
  overlay = null;
  o.style.transition = `opacity .3s ${EASE}`;
  o.style.opacity = '0';
  setTimeout(() => o.remove(), 300);
  syncHeader();
};
const menuKey = (e) => {
  if (e.key === 'Escape') { closeMenu(); return; }
  if (e.key !== 'Tab') return;
  const f = [menuBtn, ...overlay.querySelectorAll('a')];
  const i = f.indexOf(document.activeElement);
  if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
  else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
};
const openMenu = () => {
  menuOpen = true;
  menuBtn.setAttribute('aria-expanded', 'true');
  menuBtn.setAttribute('aria-label', 'Close menu');
  menuBtn.textContent = 'Close';
  document.body.style.overflow = 'hidden';
  overlay = document.createElement('div');
  overlay.id = 'mobile-menu';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Site navigation');
  overlay.className = 'fixed inset-0 top-16 z-40 bg-bg md:hidden';
  overlay.innerHTML = `<div class="flex h-full flex-col justify-center gap-2 px-6">${NAV.map(([l, h]) => `<a href="${h}" class="text-display-md border-t border-line py-4 ${active === h ? 'text-accent' : 'text-ink'}">${l}</a>`).join('')}<div class="text-label mt-8 text-muted">AI Engineer — Pune</div></div>`;
  header.appendChild(overlay);
  document.querySelector('main').inert = true;
  window.addEventListener('keydown', menuKey);
  overlay.querySelector('a').focus();
  animate(overlay, { opacity: '0' }, { opacity: '1' }, 0.3);
  overlay.querySelectorAll('a').forEach((a, i) => {
    a.addEventListener('click', closeMenu);
    animate(a, { opacity: '0', transform: 'translateY(20px)' }, { opacity: '1', transform: 'translateY(0px)' }, 0.5, 0.06 * i);
  });
  syncHeader();
};
menuBtn.addEventListener('click', () => (menuOpen ? closeMenu() : openMenu()));

// Project demo video modal
document.querySelectorAll('button[aria-label^="Watch "]').forEach((btn) => {
  const name = btn.getAttribute('aria-label').replace(/^Watch | demo video$/g, '');
  const src = btn.dataset.video ?? '';
  const poster = btn.querySelector('img').getAttribute('src');
  btn.addEventListener('click', () => {
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 z-[100] flex items-center justify-center bg-bg/90 p-4 backdrop-blur-sm sm:p-8';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', `${name} demo video`);
    modal.innerHTML = `<div class="relative w-full max-w-5xl"><button type="button" aria-label="Close video" class="text-label absolute -top-11 right-0 flex h-9 items-center gap-2 text-muted transition-colors hover:text-ink">Close <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg></button><video controls autoplay playsinline preload="none" poster="${poster}" src="${src}" class="aspect-video w-full rounded-sm border border-line bg-black"></video></div>`;
    const inner = modal.firstElementChild;
    const close = () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
      modal.style.transition = `opacity .25s ${EASE}`;
      modal.style.opacity = '0';
      inner.style.transition = `transform .3s ${EASE}, opacity .3s ${EASE}`;
      inner.style.transform = 'scale(0.97)';
      inner.style.opacity = '0';
      setTimeout(() => modal.remove(), 300);
    };
    const onKey = (e) => e.key === 'Escape' && close();
    modal.addEventListener('click', close);
    inner.addEventListener('click', (e) => e.stopPropagation());
    inner.querySelector('button').addEventListener('click', close);
    window.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    document.body.appendChild(modal);
    animate(modal, { opacity: '0' }, { opacity: '1' }, 0.25);
    animate(inner, { opacity: '0', transform: 'scale(0.97)' }, { opacity: '1', transform: 'scale(1)' }, 0.3);
  });
});
