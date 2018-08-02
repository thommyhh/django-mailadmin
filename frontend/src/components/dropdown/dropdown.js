/* globals AbortController, fetch */
import getParents from 'dom-parents'
/**
 * The drop-down/auto-complete element
 * @param dropDown HTMLElement
 * @returns {{}}
 */
export default function(dropDown) {
	/**
	 * The expanding/collapsing panel
	 */
	let panel
	/**
	 * The abort controller to abort fetch requests
	 */
	let abortController
	/**
	 * Initialize the element
	 *
	 * @param dropDown HTMLElement
	 */
	let initialize = function(dropDown) {
		panel = dropDown.querySelector('.js-dropdown-panel')

		if (dropDown.dataset.url) {
			initializeAutoComplete(dropDown)
		} else {
			initializeDropDown(dropDown)
		}
		document.addEventListener('click', ev => {
			if (ev.target !== dropDown) {
				let closeDropDown = true
				let parentElements = getParents(ev.target)
				parentElements.forEach(element => {
					if (element === dropDown) {
						closeDropDown = false
					}
				})
				if (closeDropDown) {
					close()
				}
			}
		})
	}

	/**
	 * Initialize the auto-complete element
	 *
	 * @param dropDown HTMLElement
	 */
	let initializeAutoComplete = function(dropDown) {
		abortController = new AbortController()
		let input = dropDown.querySelector('.js-auto-complete-input')
		input.addEventListener('keyup', () => {
			if (input.value.length >= 3) {
				fetch(dropDown.dataset.url + '?q=' + encodeURIComponent(input.value), {
					method: 'GET',
					credentials: 'same-origin',
					signal: abortController.signal
				}).then(response => {
					response.text().then(responseText => {
						panel.innerHTML = responseText
						open()
					})
				})
			}
		})
	}

	/**
	 * Initialize the normal drop-down element
	 *
	 * @param dropDown HTMLElement
	 */
	let initializeDropDown = function(dropDown) {
		dropDown.addEventListener('click', ev => {
			ev.preventDefault()
			if (isOpen()) {
				close();
			} else {
				open()
			}
		})
	}

	let isOpen = function() {
		return dropDown.classList.contains('is-visible')
	}

	let open = function() {
		dropDown.classList.add('is-visible')
	}

	let close = function() {
		dropDown.classList.remove('is-visible')
	}

	initialize(dropDown)

	return {}
}
