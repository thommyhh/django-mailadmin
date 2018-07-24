/* TOGGLE
 * Adds or removes class with the press of a button.
============================================================================= */

// Toggle Form Autocomplete

export default function(element, buttonClass, panelClass) {
  if (!element) {
    throw new Error('Element missing.')
  }

  if (!buttonClass) {
    throw new Error('Class for activated button missing.')
  }

  if (!panelClass) {
    throw new Error('Class for activated panel missing.')
  }

  element.getElementsByClassName('js-form-autocomplete-input')[0].addEventListener('focus', function() {
    this.classList.add(buttonClass)
    element.getElementsByClassName('js-form-autocomplete-panel')[0].classList.add(panelClass)
  })

  element.getElementsByClassName('js-form-autocomplete-input')[0].addEventListener('blur', function() {
    this.classList.remove(buttonClass)
    element.getElementsByClassName('js-form-autocomplete-panel')[0].classList.remove(panelClass)
  })
}
