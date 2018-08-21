/**
 * @param element {HTMLElement}
 */
export default function(element) {
	/**
	 * @type {HTMLElement}
	 */
	let root
	/**
	 * @type {HTMLElement}
	 */
	let titleElement
	/**
	 * @type {HTMLElement}
	 */
	let messageElement
	/**
	 *  @type {HTMLElement}
	 */
	let closeButton
	/**
	 * @type {boolean}
	 */
	let visible = false

	let initialize = (element) => {
		root = element
		titleElement = root.querySelector('.js-notification-headline')
		messageElement = root.querySelector('.js-notification-message')
		closeButton = root.querySelector('.js-notification-close')

		closeButton.addEventListener('click', () => {
			hide()
		})
	}

	let show = (title, message, type) => {
		if (visible) {
			// If there is a notification visible, hide it first
			hide()
		}
		titleElement.innerText = title
		messageElement.innerText = message
		root.classList.add('notification--' + type)
		root.classList.remove('is-hidden')
		visible = true
	}

	let hide = () => {
		titleElement.innerText = ''
		messageElement.innerText = ''
		root.classList.add('is-hidden')
		for (let className of root.classList) {
			if (/notification--/.test(className)) {
				root.classList.remove(className)
			}
		}
		visible = false
	}

	initialize(element)

	return {
		show: show,
		hide: hide
	}
}
