import Message from '../notification/notification'
import {ServerError} from '../notification/errors'

export default function(element) {
	/**
	 * @type {HTMLElement}
	 */
	let root
	/**
	 * @type {HTMLElement}
	 */
	let filter
	let list
	/** @type {HTMLElement}  */
	let pagination
	let paginationButtonContainer
	let itemsPerPage
	let lastRequestParameters = {
		query: '',
		page: 1,
		itemsPerPage: null
	}
	let requestParameters = {
		page: 1,
		query: '',
		itemsPerPage: null
	}
	let url
	let abortController
	let message

	let initialize = element => {
		root = element
		url = root.dataset.url

		// Initialize filter input
		filter = root.querySelector('.js-list-filter')
		initializeFilter()

		// Initialize pagination
		pagination = root.querySelector('.js-pagination')
		paginationButtonContainer = pagination.querySelector('.js-pagination-buttons')
		itemsPerPage = root.querySelector('.js-pagination-size')
		initializePagination()

		// Initialize list
		list = root.querySelector('.js-list-holder')

		// Initialize notification
		message = new Message(document.querySelector('.js-notification'))
	}

	let initializeFilter = () => {
		let filterChangeTimeout
		// Define the event handler
		let filterChangeHandler = ev => {
			if (filterChangeTimeout) {
				clearTimeout(filterChangeTimeout)
			}
			if (ev.currentTarget.value.length > 2 || ev.currentTarget.value === '') {
				let filterInput = ev.currentTarget
				filterChangeTimeout = setTimeout(() => {
					requestParameters.query = filterInput.value
					hasSearchCriteriaChanged().then(hasChanged => {
						if (hasChanged) {
							loadList()
						}
					})
				}, 300)
			}
		}
		// Register the event handler for change, keyup and click
		filter.addEventListener('change', filterChangeHandler)
		filter.addEventListener('keyup', filterChangeHandler)
		filter.addEventListener('click', filterChangeHandler)
	}

	let initializePagination = () => {
		// Set current value of "itemsPerPage"
		requestParameters.itemsPerPage = parseInt(itemsPerPage.value)
		lastRequestParameters.itemsPerPage = requestParameters.itemsPerPage
		// Add "itemsPerPage" change listener
		itemsPerPage.addEventListener('change', () => {
			requestParameters.itemsPerPage = parseInt(itemsPerPage.value)
			hasSearchCriteriaChanged().then(hasChanged => {
				if (hasChanged) {
					loadList()
				}
			})
		})
		initializePaginationButtons()
	}

	let initializePaginationButtons = () => {
		pagination.querySelectorAll('.js-pagination-button').forEach(button => {
			button.addEventListener('click', ev => {
				requestParameters.page = parseInt(ev.currentTarget.dataset.page)
				hasSearchCriteriaChanged().then(hasChanged => {
					if (hasChanged) {
						loadList()
					}
				})
			})
		})
	}

	/**
	 * Check if the current request parameters are different from the last ones,
	 * to determine, if the list should be loaded or not. If `query` or `itemsPerPage`
	 * is changed, the page is reset to the first page.
	 *
	 * @returns {Promise<boolean>}
	 */
	let hasSearchCriteriaChanged = () => {
		return new Promise((resolve) => {
			let stateChanged = false
			// Check if the filter value has changed
			if (requestParameters.query !== lastRequestParameters.query) {
				// If the filter value has changed, reset the page to 1
				requestParameters.page = 1
				stateChanged = true
			}
			// Check if the "itemsPerPage" has changed
			if (requestParameters.itemsPerPage !== lastRequestParameters.itemsPerPage) {
				// If "itemsPerPage" has changed, go back to page 1
				requestParameters.page = 1
				stateChanged = true
			}
			// Check if the page has changed
			if (requestParameters.page !== lastRequestParameters.page) {
				stateChanged = true
			}
			// Finally resolve the promise
			resolve(stateChanged)
		})
	}

	let loadList = () => {
		// If the abort controller exists (a request is running) it must be aborted
		if (abortController instanceof AbortController && abortController.signal.aborted === false) {
			abortController.abort()
			abortController = null
		}
		// Create a new abort controller
		if (!abortController) {
			abortController = new AbortController()
		}
		root.classList.add('is-loading')
		fetch(url, {
			method: 'get',
			credentials: 'same-origin',
			body: requestParameters,
			signal: abortController.signal
		}).then(response => {
			if (response.ok && response.status === 200) {
				response.json().then(data => {
					list.innerHTML = data.list
					paginationButtonContainer.innerHTML = data.pagination
					initializePaginationButtons()
					// Set the current request parameters as the last request parameters
					updateRequestParameters(requestParameters, lastRequestParameters)
				})
			} else {
				throw new ServerError(response.statusText, response.status)
			}
		}).catch(reason => {
			// If anything went wrong, reset the request parameters
			updateRequestParameters(lastRequestParameters, requestParameters)
			if (reason instanceof ServerError) {
				message.show('Server Error', 'The server responded with status code ' + reason.status + '. Please contact your admin.', 'error')
			} else if (reason instanceof TypeError) {
				message.show('Network error', 'There seems to be an error with your network connection', 'error')
			} else {
				message.show('Error', 'An error occurred. Unfortunately there are no further details available.', 'error')
			}
		}).finally(() => {
			root.classList.remove('is-loading')
		})
	}

	/**
	 * Copy the request parameters from `from` to `to`. Used to update the parameters
	 * after the request. Can be used on both direction (current to last or last to current),
	 * depending on if the request was successful or not.
	 *
	 * @param from {object}
	 * @param to {object}
	 */
	let updateRequestParameters = (from, to) => {
		for (let property in from) {
			if (from.hasOwnProperty(property)) {
				to[property] = from[property]
			}
		}
	}

	initialize(element)

	return {}
}
