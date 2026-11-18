(() => {
  const KEY = 'brewhouse_cart_v1', C = window.BREW;
  const $ = s => document.querySelector(s);
  let cart = [];
  try { cart = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { cart = []; }
  const fmt = n => n.toFixed(2) + ' ' + C.cur;
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) {} render(); };
  const waLink = text => 'https://wa.me/' + C.wa.replace(/\D/g, '') + '?text=' + encodeURIComponent(text);
  function openWA(text) {
    if (!C.wa.replace(/\D/g, '')) return $('#waDialog').showModal();
    window.open(waLink(text), '_blank', 'noopener');
  }
  function toggle(open) {
    $('#drawer').classList.toggle('open', open); $('#backdrop').hidden = !open;
    $('#drawer').setAttribute('aria-hidden', String(!open));
  }
  function render() {
    const count = cart.reduce((s, i) => s + i.qty, 0), sub = cart.reduce((s, i) => s + i.qty * i.price, 0);
    const b = $('#badge'); b.textContent = count; b.hidden = !count;
    $('#subtotal').textContent = fmt(sub); $('#checkout').disabled = !cart.length;
    const box = $('#items'); box.textContent = '';
    if (!cart.length) { box.innerHTML = '<p class="center muted">Your order is empty.</p>'; return; }
    cart.forEach(i => {
      const row = document.createElement('div'); row.className = 'item';
      const info = document.createElement('div'); info.innerHTML = '<strong></strong><br><small></small>';
      info.querySelector('strong').textContent = i.name; info.querySelector('small').textContent = fmt(i.price) + ' each';
      const ctl = document.createElement('div'); ctl.className = 'qty';
      [['−', -1, 'Decrease'], [i.qty, 0], ['+', 1, 'Increase'], ['✕', null, 'Remove']].forEach(([t, d, label]) => {
        if (d === 0) { const o = document.createElement('output'); o.textContent = t; return ctl.append(o); }
        const btn = document.createElement('button'); btn.type = 'button'; btn.textContent = t; btn.setAttribute('aria-label', label + ' ' + i.name);
        btn.onclick = () => { if (d === null) cart = cart.filter(x => x.id !== i.id); else { i.qty += d; if (i.qty < 1) cart = cart.filter(x => x.id !== i.id); } save(); };
        ctl.append(btn);
      });
      row.append(info, ctl); box.append(row);
    });
  }
  document.addEventListener('click', e => {
    const t = e.target.closest('button'); if (!t) return;
    const card = t.closest('.card'), qtyEl = card && card.querySelector('[data-qty] output');
    if (t.dataset.q && qtyEl) return void (qtyEl.textContent = Math.max(1, Math.min(99, +qtyEl.textContent + +t.dataset.q)));
    if (t.hasAttribute('data-add')) {
      const qty = +qtyEl.textContent, ex = cart.find(i => i.id === t.dataset.id);
      if (ex) ex.qty = Math.min(99, ex.qty + qty); else cart.push({ id: t.dataset.id, name: t.dataset.name, price: +t.dataset.price, qty });
      save(); const old = t.innerHTML; t.textContent = 'Added ✓'; setTimeout(() => t.innerHTML = old, 900);
    } else if (t.hasAttribute('data-order')) {
      const q = +qtyEl.textContent;
      openWA(`Hello ${C.shop}! I would like to order:\n\nProduct: ${t.dataset.name}\nPrice: ${(+t.dataset.price).toFixed(2)} ${C.cur}\nQuantity: ${q}\n\nPlease confirm my order.`);
    } else if (t.id === 'checkout') {
      const lines = cart.map((i, n) => `${n + 1}. ${i.name} x${i.qty} - ${(i.price * i.qty).toFixed(2)} ${C.cur}`);
      openWA(`Hello ${C.shop}! I would like to order:\n\n${lines.join('\n')}\n\nSubtotal: ${fmt(cart.reduce((s, i) => s + i.qty * i.price, 0))}\n\nPlease confirm my order.`);
    } else if (t.id === 'openCart' || t.hasAttribute('data-open-cart')) toggle(true);
    else if (t.id === 'closeCart') toggle(false);
    else if (t.hasAttribute('data-wa-contact')) openWA(`Hello ${C.shop}!`);
  });
  $('#backdrop').addEventListener('click', () => toggle(false));
  document.addEventListener('keydown', e => e.key === 'Escape' && toggle(false));
  window.BrewCart = { waLink }; render();
})();
