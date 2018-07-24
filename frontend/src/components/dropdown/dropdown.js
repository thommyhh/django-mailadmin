/* eslint-disable no-unused-vars */
import toggle from '../../functions/toggle'
import toggleInput from '../../functions/toggleInput'
/* DROPDOWN
 * Click a button and an awesome menu pops up.
============================================================================= */

/* globals toggle, toggleInput */

(function() {
  'use strict'

  let items = document.getElementsByClassName('js-dropdown')

  for (let i = 0; i < items.length; i++) {
    toggle(items[i], 'is-active', 'is-visible')
  }
})();

(function() {
  'use strict'

  let items = document.getElementsByClassName('js-form-autocomplete')

  for (let i = 0; i < items.length; i++) {
    toggleInput(items[i], 'is-active', 'is-visible')
  }
})()
