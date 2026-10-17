/* Ply theme scripts: cart drawer, quick add, variant selection, delivery dates, sticky buy bar. */
(function () {
  'use strict';

  var Ply = window.Ply || {};
  var DRAWER_SECTION = 'cart-drawer';

  function formatMoney(cents) {
    var format = Ply.moneyFormat || '${{amount}}';
    var value = cents / 100;
    var whole = cents % 100 === 0;
    var amount = whole ? String(Math.round(value)) : value.toFixed(2);
    return format.replace(/\{\{\s*(\w+)\s*\}\}/, function (match, key) {
      if (key === 'amount_no_decimals') return String(Math.round(value));
      if (key === 'amount_with_comma_separator') return amount.replace('.', ',');
      return amount;
    });
  }

  function sizedImage(src, width) {
    if (!src) return '';
    return src + (src.indexOf('?') > -1 ? '&' : '?') + 'width=' + width;
  }

  function getDrawer() {
    return document.querySelector('cart-drawer');
  }

  function updateCartCount(count) {
    document.querySelectorAll('[data-cart-count]').forEach(function (el) {
      if (el.closest('cart-drawer')) return;
      el.textContent = count;
    });
  }

  /* Cart drawer */
  class CartDrawer extends HTMLElement {
    connectedCallback() {
      this.addEventListener('click', this.onClick.bind(this));
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.classList.contains('is-open')) this.close();
      });
      document.querySelectorAll('[data-open-cart]').forEach((el) => {
        el.addEventListener('click', (e) => {
          e.preventDefault();
          this.open(el);
        });
      });
    }

    open(trigger) {
      this.lastFocus = trigger || document.activeElement;
      this.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      var panel = this.querySelector('.drawer');
      if (panel) panel.removeAttribute('aria-hidden');
      var focusTarget = this.querySelector('[data-drawer-close]');
      if (focusTarget) setTimeout(function () { focusTarget.focus(); }, 50);
    }

    close() {
      this.classList.remove('is-open');
      document.body.style.overflow = '';
      var panel = this.querySelector('.drawer');
      if (panel) panel.setAttribute('aria-hidden', 'true');
      if (this.lastFocus && this.lastFocus.focus) this.lastFocus.focus();
    }

    render(html) {
      if (!html) return;
      var doc = new DOMParser().parseFromString(html, 'text/html');
      var fresh = doc.querySelector('[data-drawer-inner]');
      var current = this.querySelector('[data-drawer-inner]');
      if (fresh && current) current.replaceWith(fresh);
      var countEl = this.querySelector('[data-drawer-count]');
      if (countEl) updateCartCount(countEl.getAttribute('data-drawer-count'));
    }

    onClick(e) {
      if (e.target.closest('[data-drawer-close]') || e.target.classList.contains('drawer-overlay')) {
        this.close();
        return;
      }
      var change = e.target.closest('[data-line-change]');
      if (change) {
        e.preventDefault();
        this.changeLine(change.getAttribute('data-line'), parseInt(change.getAttribute('data-quantity'), 10));
      }
    }

    changeLine(line, quantity) {
      var body = this.querySelector('.drawer__body');
      if (body) body.style.opacity = '0.6';
      fetch(Ply.routes.cartChange + '.js', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ line: Number(line), quantity: quantity, sections: [DRAWER_SECTION], sections_url: window.location.pathname })
      })
        .then(function (r) { return r.json(); })
        .then((data) => {
          if (data.sections) this.render(data.sections[DRAWER_SECTION]);
        })
        .catch(function () {})
        .finally(() => {
          var b = this.querySelector('.drawer__body');
          if (b) b.style.opacity = '';
        });
    }
  }
  customElements.define('cart-drawer', CartDrawer);

  /* Add to cart without leaving the page */
  class ProductForm extends HTMLElement {
    connectedCallback() {
      this.form = this.querySelector('form');
      if (!this.form) return;
      this.form.addEventListener('submit', this.onSubmit.bind(this));
    }

    onSubmit(e) {
      var drawer = getDrawer();
      if (!drawer) return;
      e.preventDefault();
      var button = this.form.querySelector('[type="submit"]');
      var error = this.querySelector('[data-form-error]');
      if (button) {
        button.classList.add('is-loading');
        button.setAttribute('aria-busy', 'true');
      }
      if (error) error.hidden = true;
      var formData = new FormData(this.form);
      formData.append('sections', DRAWER_SECTION);
      formData.append('sections_url', window.location.pathname);
      fetch(Ply.routes.cartAdd + '.js', { method: 'POST', headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' }, body: formData })
        .then(function (r) { return r.json().then(function (data) { return { ok: r.ok, data: data }; }); })
        .then(function (res) {
          if (!res.ok || res.data.status) {
            if (error) {
              error.textContent = res.data.description || res.data.message || Ply.strings.error;
              error.hidden = false;
            }
            return;
          }
          if (res.data.sections) drawer.render(res.data.sections[DRAWER_SECTION]);
          drawer.open(button);
        })
        .catch(function () {
          if (error) {
            error.textContent = Ply.strings.error;
            error.hidden = false;
          }
        })
        .finally(function () {
          if (button) {
            button.classList.remove('is-loading');
            button.removeAttribute('aria-busy');
          }
        });
    }
  }
  customElements.define('product-form', ProductForm);

  /* Variant selection for cards and the product page */
  class VariantPicker extends HTMLElement {
    connectedCallback() {
      var json = this.querySelector('script[type="application/json"]');
      this.variants = json ? JSON.parse(json.textContent) : [];
      this.scope = this.closest('[data-product-scope]') || this;
      this.addEventListener('change', this.onChange.bind(this));
      this.syncUpsells();
    }

    /* Cross-sell rows follow the colour the shopper picked */
    syncUpsells() {
      var checked = this.querySelector('.swatch input:checked');
      if (!checked) return;
      var colour = checked.value;
      this.scope.querySelectorAll('[data-match-colour]').forEach(function (row) {
        var json = row.querySelector('script[data-upsell-variants]');
        if (!json) return;
        var variants = JSON.parse(json.textContent);
        var match = variants.find(function (v) { return v.available && v.options.indexOf(colour) > -1; });
        if (!match) return;
        var input = row.querySelector('[data-upsell-input]');
        if (input) input.value = match.id;
        var title = row.querySelector('[data-upsell-variant]');
        if (title) title.textContent = match.title;
        var price = row.querySelector('[data-upsell-price]');
        if (price) price.textContent = formatMoney(match.price);
        var img = row.querySelector('.js-upsell-image');
        if (img && match.featured_image) {
          img.src = sizedImage(match.featured_image.src, 160);
          img.removeAttribute('srcset');
        }
      });
    }

    selectedOptions() {
      return Array.from(this.querySelectorAll('fieldset')).map(function (fs) {
        var checked = fs.querySelector('input:checked');
        return checked ? checked.value : null;
      });
    }

    onChange(e) {
      var input = e.target;
      if (input && input.matches('input[type="radio"]')) {
        var current = input.closest('fieldset').querySelector('[data-option-current]');
        if (current) current.textContent = input.value;
      }
      var options = this.selectedOptions();
      var variant = this.variants.find(function (v) {
        return v.options.every(function (opt, i) { return opt === options[i]; });
      });
      this.applyVariant(variant);
    }

    applyVariant(variant) {
      var scope = this.scope;
      var idInputs = scope.querySelectorAll('input[name="id"][data-variant-input]');
      var buttons = scope.querySelectorAll('[data-add-button]');
      if (!variant) {
        buttons.forEach(function (b) {
          b.disabled = true;
          var label = b.querySelector('[data-add-label]');
          if (label) label.textContent = Ply.strings.unavailable;
        });
        return;
      }
      idInputs.forEach(function (i) { i.value = variant.id; });
      scope.querySelectorAll('[data-price]').forEach(function (el) { el.textContent = formatMoney(variant.price); });
      scope.querySelectorAll('[data-compare-price]').forEach(function (el) {
        var show = variant.compare_at_price && variant.compare_at_price > variant.price;
        el.hidden = !show;
        if (show) el.textContent = formatMoney(variant.compare_at_price);
      });
      buttons.forEach(function (b) {
        b.disabled = !variant.available;
        var label = b.querySelector('[data-add-label]');
        if (label) label.textContent = variant.available ? Ply.strings.addToCart : Ply.strings.soldOut;
      });
      scope.querySelectorAll('[data-variant-title]').forEach(function (el) { el.textContent = variant.title; });
      this.syncUpsells();

      if (variant.featured_media && this.dataset.gallery === 'true') {
        var gallery = scope.querySelector('media-gallery');
        if (gallery) gallery.show(String(variant.featured_media.id));
      } else if (variant.featured_image) {
        var img = scope.querySelector('.js-card-image');
        if (img) {
          img.src = sizedImage(variant.featured_image.src, 900);
          img.srcset = [500, 700, 900, 1200].map(function (w) { return sizedImage(variant.featured_image.src, w) + ' ' + w + 'w'; }).join(', ');
          if (variant.featured_image.alt) img.alt = variant.featured_image.alt;
        }
      }

      if (this.dataset.updateUrl === 'true') {
        var url = new URL(window.location.href);
        url.searchParams.set('variant', variant.id);
        window.history.replaceState({}, '', url.toString());
        scope.querySelectorAll('[data-whatsapp-link]').forEach(function (a) {
          var base = a.getAttribute('data-base-text') || '';
          var number = a.getAttribute('data-number') || '';
          var text = base + ' ' + variant.title + ' ' + url.toString();
          a.href = 'https://wa.me/' + number + '?text=' + encodeURIComponent(text);
        });
      }
    }
  }
  customElements.define('variant-picker', VariantPicker);

  /* Product gallery */
  class MediaGallery extends HTMLElement {
    connectedCallback() {
      this.addEventListener('click', (e) => {
        var thumb = e.target.closest('[data-media-thumb]');
        if (thumb) this.show(thumb.getAttribute('data-media-thumb'));
      });
    }

    show(id) {
      var found = false;
      this.querySelectorAll('[data-media-id]').forEach(function (el) {
        var match = el.getAttribute('data-media-id') === id;
        el.hidden = !match;
        if (match) found = true;
      });
      if (!found) return;
      this.querySelectorAll('[data-media-thumb]').forEach(function (b) {
        b.setAttribute('aria-current', b.getAttribute('data-media-thumb') === id ? 'true' : 'false');
      });
    }
  }
  customElements.define('media-gallery', MediaGallery);

  /* Quantity steppers on the product page */
  document.addEventListener('click', function (e) {
    var step = e.target.closest('[data-qty-step]');
    if (!step) return;
    var input = step.parentElement.querySelector('input[type="number"]');
    if (!input) return;
    var next = Math.max(1, Math.min(99, (parseInt(input.value, 10) || 1) + parseInt(step.getAttribute('data-qty-step'), 10)));
    input.value = next;
    input.dispatchEvent(new Event('change', { bubbles: true }));
  });

  /* Delivery dates: business days, no deliveries on Sunday */
  function addBusinessDays(days) {
    var d = new Date();
    var added = 0;
    while (added < days) {
      d.setDate(d.getDate() + 1);
      if (d.getDay() !== 0) added += 1;
    }
    return d;
  }

  function renderEta() {
    var locale = Ply.locale === 'ar' ? 'ar-LB' : 'en-GB';
    document.querySelectorAll('[data-eta]').forEach(function (el) {
      var min = parseInt(el.getAttribute('data-min'), 10) || 2;
      var max = parseInt(el.getAttribute('data-max'), 10) || 4;
      var fmt = { weekday: 'short', day: 'numeric', month: 'short' };
      try {
        var from = addBusinessDays(min).toLocaleDateString(locale, fmt);
        var to = addBusinessDays(max).toLocaleDateString(locale, fmt);
        var template = el.getAttribute('data-template') || '{from} – {to}';
        el.textContent = template.replace('{from}', from).replace('{to}', to);
      } catch (err) { /* keep the server-rendered fallback */ }
    });
  }

  /* Sticky buy bar on phones */
  function initStickyBuy() {
    var bar = document.querySelector('[data-sticky-buy]');
    var target = document.querySelector('[data-main-add]');
    if (!bar || !target || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var past = !entry.isIntersecting && entry.boundingClientRect.top < 0;
        bar.classList.toggle('is-visible', past);
        bar.setAttribute('aria-hidden', past ? 'false' : 'true');
      });
    });
    io.observe(target);
  }

  /* Close the mobile menu on Escape or link tap */
  function initMobileMenu() {
    var menu = document.querySelector('[data-mobile-menu]');
    if (!menu) return;
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) menu.removeAttribute('open');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.hasAttribute('open')) {
        menu.removeAttribute('open');
        var summary = menu.querySelector('summary');
        if (summary) summary.focus();
      }
    });
  }

  function initLocaleSelect() {
    document.querySelectorAll('[data-locale-select]').forEach(function (select) {
      select.addEventListener('change', function () { if (select.form) select.form.submit(); });
    });
  }

  function init() {
    initLocaleSelect();
    renderEta();
    initStickyBuy();
    initMobileMenu();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  document.addEventListener('shopify:section:load', init);
})();
