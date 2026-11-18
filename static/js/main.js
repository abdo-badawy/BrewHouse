(() => {
  const burger = document.getElementById('burger'), nav = document.getElementById('nav');
  burger.addEventListener('click', () => { const o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o); });
  document.querySelectorAll('.tab').forEach(tab => tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('on', t === tab));
    document.querySelectorAll('.cat').forEach(s => s.hidden = tab.dataset.cat !== 'all' && s.dataset.section !== tab.dataset.cat);
  }));
  const els = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .1 });
    els.forEach(el => { el.classList.add('reveal'); io.observe(el); });
  }
})();
