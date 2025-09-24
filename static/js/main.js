//(function () {
//  const header = document.querySelector('header');
//  const hero   = document.getElementById('hero');
//  const canvas = document.getElementById('canvas');
//  const nav    = document.getElementById('nav');
//  const logo   = document.getElementById('logo');
//  const icons  = document.getElementById('icons');
//
//  const CW = 1540, CH = 700;
//
//  function fit() {
//    if (!header) return;
//    if (!hero || !canvas) { paintNav(); return; }
//
//    const availH = Math.max(560, window.innerHeight - header.offsetHeight);
//    hero.style.height = availH + 'px';
//
//    const cs   = getComputedStyle(hero);
//    const padL = parseFloat(cs.paddingLeft) || 0;
//    const padR = parseFloat(cs.paddingRight) || 0;
//    const padT = parseFloat(cs.paddingTop) || 0;
//    const padB = parseFloat(cs.paddingBottom) || 0;
//
//    const innerW = hero.clientWidth  - (padL + padR);
//    const innerH = hero.clientHeight - (padT + padB);
//
//    const s = Math.min(innerW / CW, innerH / CH);
//    canvas.style.transform = 'scale(' + s + ')';
//
//    const usedW = CW * s, usedH = CH * s;
//    canvas.style.position = 'absolute';
//    canvas.style.left = (padL + (innerW - usedW) / 2) + 'px';
//    canvas.style.top  = (padT + (innerH - usedH) / 2) + 'px';
//
//    paintNav();
//  }
//
//  function paintNav() {
//    if (!nav || !logo || !icons) return;
//    const mid = window.innerWidth / 2;
//    logo.style.color = '#F5EAE6';
//    Array.from(nav.children).forEach(a => {
//      const r = a.getBoundingClientRect(), cx = r.left + r.width / 2;
//      a.style.color = (cx < mid) ? '#DCC7C1' : '#4C2F27';
//    });
//    Array.from(icons.children).forEach(ic => {
//      const r = ic.getBoundingClientRect(), cx = r.left + r.width / 2;
//      const col = (cx < mid) ? '#DCC7C1' : '#4C2F27';
//      ic.style.color = col;
//    });
//  }
//
//  addEventListener('resize', fit);
//  addEventListener('DOMContentLoaded', fit);
//})();
//
//(function () {
//  const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
//  const $count = document.getElementById('js-cart-count');
//
//  function updateCount(n) {
//    if ($count) $count.textContent = n;
//  }
//
//  async function postJSON(url) {
//    const res = await fetch(url, {
//      method: 'POST',
//      headers: {
//        'X-CSRFToken': csrftoken
//      }
//    });
//    return await res.json();
//  }
//
//  // Каталог: "В корзину"
//  document.addEventListener('click', async (e) => {
//    const addBtn = e.target.closest('.js-add-to-cart');
//    if (addBtn) {
//      e.preventDefault();
//      const slug = addBtn.dataset.slug;
//      const data = await postJSON(`/shop/cart/add/${slug}/`);
//      if (data && data.ok) updateCount(data.count);
//    }
//
//    // Корзина: +/-
//    const inc = e.target.closest('.js-inc');
//    const dec = e.target.closest('.js-dec');
//
//    if (inc) {
//      e.preventDefault();
//      const slug = inc.dataset.slug;
//      const data = await postJSON(`/shop/cart/add/${slug}/`);
//      if (data.ok) {
//        updateCount(data.count);
//        const el = document.getElementById(`qty-${slug}`);
//        if (el) el.textContent = data.qty;
//      }
//    }
//    if (dec) {
//      e.preventDefault();
//      const slug = dec.dataset.slug;
//      const data = await postJSON(`/shop/cart/remove/${slug}/`);
//      if (data.ok) {
//        updateCount(data.count);
//        const wrap = document.querySelector(`.basket-card[data-slug="${slug}"]`);
//        const el = document.getElementById(`qty-${slug}`);
//        if (data.qty <= 0 && wrap) {
//          wrap.remove();
//        } else if (el) {
//          el.textContent = data.qty;
//        }
//        // Пересчитать итого на клиенте можно тут при желании.
//        // Сейчас итог пересчитывается сервером на перезагрузке,
//        // чтобы не усложнять — оставим так.
//      }
//    }
//  });
//})();

/* ===== hero fit & nav paint (как было) ===== */
(function () {
  const header = document.querySelector('header');
  const hero   = document.getElementById('hero');
  const canvas = document.getElementById('canvas');
  const nav    = document.getElementById('nav');
  const logo   = document.getElementById('logo');
  const icons  = document.getElementById('icons');

  const CW = 1540, CH = 700;

  function fit() {
    if (!header) return;
    if (!hero || !canvas) { paintNav(); return; }

    const availH = Math.max(560, window.innerHeight - header.offsetHeight);
    hero.style.height = availH + 'px';

    const cs   = getComputedStyle(hero);
    const padL = parseFloat(cs.paddingLeft) || 0;
    const padR = parseFloat(cs.paddingRight) || 0;
    const padT = parseFloat(cs.paddingTop) || 0;
    const padB = parseFloat(cs.paddingBottom) || 0;

    const innerW = hero.clientWidth  - (padL + padR);
    const innerH = hero.clientHeight - (padT + padB);

    const s = Math.min(innerW / CW, innerH / CH);
    canvas.style.transform = 'scale(' + s + ')';

    const usedW = CW * s, usedH = CH * s;
    canvas.style.position = 'absolute';
    canvas.style.left = (padL + (innerW - usedW) / 2) + 'px';
    canvas.style.top  = (padT + (innerH - usedH) / 2) + 'px';

    paintNav();
  }

  function paintNav() {
    if (!nav || !logo || !icons) return;
    const mid = window.innerWidth / 2;
    logo.style.color = '#F5EAE6';
    Array.from(nav.children).forEach(a => {
      const r = a.getBoundingClientRect(), cx = r.left + r.width / 2;
      a.style.color = (cx < mid) ? '#DCC7C1' : '#4C2F27';
    });
    Array.from(icons.children).forEach(ic => {
      const r = ic.getBoundingClientRect(), cx = r.left + r.width / 2;
      const col = (cx < mid) ? '#DCC7C1' : '#4C2F27';
      ic.style.color = col;
    });
  }

  addEventListener('resize', fit);
  addEventListener('DOMContentLoaded', fit);
})();
/* ===== cart logic (AJAX, без перезагрузки) ===== */
(function () {
  // CSRF из <meta name="csrf-token"> или cookie
  function getCookie(name) {
    const m = document.cookie.match('(?:^|; )' + name.replace(/([.$?*|{}()[\]\\/+^])/g, '\\$1') + '=([^;]*)');
    return m ? decodeURIComponent(m[1]) : '';
  }
  const meta = document.querySelector('meta[name="csrf-token"]');
  const csrftoken = meta ? meta.getAttribute('content') : getCookie('csrftoken');

  const $count = document.getElementById('js-cart-count');
  function updateCount(n) { if ($count) $count.textContent = n; }

  // ------ пересчёт Итого ------
  const $total = document.getElementById('js-cart-total');

  function num(x){ const n = parseFloat(String(x).replace(',', '.')); return Number.isFinite(n) ? n : 0; }
  function fmtRU(n){ return Math.round(n).toLocaleString('ru-RU'); }

  function lineTotal($item){
    const price = $item.dataset.price ? num($item.dataset.price)
      : num(($item.querySelector('.cart-price')?.textContent||'').replace(/[^\d.,]/g,''));
    const qtyEl = $item.querySelector('.qty-val');
    const qty = parseInt(qtyEl ? qtyEl.textContent : '0', 10) || 0;
    return price * qty;
  }

  function recalcCartTotal(){
    if (!$total) return;
    let sum = 0;
    document.querySelectorAll('.cart-item').forEach($it => { sum += lineTotal($it); });
    $total.textContent = fmtRU(sum);
  }

  // при загрузке страницы корзины посчитаем сразу
  document.addEventListener('DOMContentLoaded', recalcCartTotal);

  async function fetchJSON(url, body) {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      body: body || null,
      credentials: 'same-origin'
    });
    const ct = res.headers.get('content-type') || '';
    if (!ct.includes('application/json')) return { ok: false };
    return await res.json();
  }

  // 1) Каталог: сабмит формы добавления (берём quantity)
  document.addEventListener('submit', async (e) => {
    const form = e.target.closest('form');
    if (!form) return;
    const action = form.getAttribute('action') || '';
    if (!/\/shop\/cart\/add\//.test(action)) return;
    e.preventDefault();

    const fd = new FormData(form);
    const q = parseInt(fd.get('quantity') || '1', 10);
    fd.set('quantity', Number.isFinite(q) && q > 0 ? q : 1);

    const data = await fetchJSON(action, fd);
    if (data && data.ok) updateCount(data.count);
  });

  // 2) Каталог: кнопка .js-add-to-cart (если она есть)
  document.addEventListener('click', async (e) => {
    const addBtn = e.target.closest('.js-add-to-cart');
    if (addBtn) {
      e.preventDefault();
      const slug = addBtn.dataset.slug;
      const form = addBtn.closest('form');
      const fd = new FormData();
      const q = parseInt(form?.querySelector('input[name="quantity"]')?.value || '1', 10);
      fd.append('quantity', Number.isFinite(q) && q > 0 ? q : 1);
      const data = await fetchJSON(`/shop/cart/add/${slug}/`, fd);
      if (data && data.ok) updateCount(data.count);
    }
  });

  // 3) Корзина: + / − / × (всё без перезагрузки)
  document.addEventListener('click', async (e) => {
    // плюс
    const inc = e.target.closest('.js-inc');
    if (inc) {
      e.preventDefault();
      inc.disabled = true;
      try {
        const slug = inc.dataset.slug;
        const data = await fetchJSON(`/shop/cart/add/${slug}/`);
        if (data.ok) {
          updateCount(data.count);
          const qtyEl = document.getElementById(`qty-${slug}`);
          if (qtyEl) qtyEl.textContent = data.qty;
          recalcCartTotal();
        }
      } finally { inc.disabled = false; }
      return;
    }

    // минус
    const dec = e.target.closest('.js-dec');
    if (dec) {
      e.preventDefault();
      dec.disabled = true;
      try {
        const slug = dec.dataset.slug;
        const data = await fetchJSON(`/shop/cart/remove/${slug}/`);
        if (data.ok) {
          updateCount(data.count);
          const row = document.querySelector(`.cart-item[data-slug="${slug}"]`);
          const qtyEl = document.getElementById(`qty-${slug}`);
          if (data.qty <= 0) {
            if (row) row.remove();
            // если корзина опустела — убираем блоки и показываем заглушку
            if (!document.querySelector('.cart-item')) {
              const wrap = document.querySelector('.cart-wrap');
              const summary = document.querySelector('.cart-summary');
              if (wrap) wrap.remove();
              if (summary) summary.remove();
              const container = document.querySelector('.cart .container');
              if (container) {
                const p = document.createElement('p');
                p.className = 'cart-empty';
                p.textContent = 'Корзина пуста.';
                container.appendChild(p);
              }
            }
          } else if (qtyEl) {
            qtyEl.textContent = data.qty;
          }
          recalcCartTotal();
        }
      } finally { dec.disabled = false; }
      return;
    }

    // крестик (удалить всю строку)
    const del = e.target.closest('.js-remove');
    if (del) {
      e.preventDefault();
      del.disabled = true;
      try {
        const slug = del.dataset.slug;
        const data = await fetchJSON(`/shop/cart/delete/${slug}/`);
        if (data.ok) {
          updateCount(data.count);
          const row = document.querySelector(`.cart-item[data-slug="${slug}"]`);
          if (row) row.remove();
          if (!document.querySelector('.cart-item')) {
            const wrap = document.querySelector('.cart-wrap');
            const summary = document.querySelector('.cart-summary');
            if (wrap) wrap.remove();
            if (summary) summary.remove();
            const container = document.querySelector('.cart .container');
            if (container) {
              const p = document.createElement('p');
              p.className = 'cart-empty';
              p.textContent = 'Корзина пуста.';
              container.appendChild(p);
            }
          }
          recalcCartTotal();
        }
      } finally { del.disabled = false; }
    }
  });
})();


