/* TOGGLE
 * Adds or removes class with the press of a button.
============================================================================= */

// Toggle Buttons

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

  element.getElementsByClassName('js-toggle-button')[0].addEventListener('click', function() {
    this.classList.toggle(buttonClass)
    element.getElementsByClassName('js-toggle-panel')[0].classList.toggle(panelClass)
  })
}
