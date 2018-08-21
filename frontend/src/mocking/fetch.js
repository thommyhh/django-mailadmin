import dropDownTemplateCode from './templates/dropDown'
import domainTemplateCode from './templates/domains'
import paginationTemplateCode from './templates/pagination'
import getDummyDomains from './data/domains'
import fetchMock from 'fetch-mock'

let nunjucks = require('nunjucks')
nunjucks.configure({
	autoescape: true
})
let dropDownResultTemplate = nunjucks.compile(dropDownTemplateCode())
let domainListTemplate = nunjucks.compile(domainTemplateCode())
let paginationTemplate = nunjucks.compile(paginationTemplateCode())

let delay = (min, max) => {
	return new Promise(resolve => {
		setTimeout(resolve, Math.random() * (max - min) + min)
	})
}

fetchMock.config.fallbackToNetwork = true
fetchMock.mock('begin:/dummy/data/auto-complete', (url, options) => {
	/\?q=(.+)/.test(url)
	let results = []
	let domains = getDummyDomains()
	for (let index in domains) {
		if (domains.hasOwnProperty(index) && domains[index].name.indexOf(RegExp.$1) > -1 && results.length < 5) {
			results.push(domains[index])
		}
	}
	return dropDownResultTemplate.render({results: results})
})
fetchMock.mock('begin:/dummy/domains/list', (url, options) => {
	return delay(200, 1000).then(() => {
		let query = options.body.query
		let page = parseInt(options.body.page)
		let itemsPerPage = parseInt(options.body.itemsPerPage)
		// Throw an error on page 6
		if (page === 6) {
			return {
				status: 500
			}
		} else if (page === 7) {
			throw new TypeError('Simulated network error')
		}
		let results = []
		let domains = getDummyDomains()
		for (let index in domains) {
			if (domains.hasOwnProperty(index) && (query === null || domains[index].name.indexOf(query) > -1) && results.indexOf(domains[index].name) === -1) {
				results.push(domains[index].name)
			}
		}
		results.sort()
		let start = Math.max(0, (page - 1) * itemsPerPage)
		let end = start + itemsPerPage
		let pages = Math.ceil(results.length / itemsPerPage)
		results = results.slice(start, end)

		return {
			list: domainListTemplate.render({results: results}),
			pagination: paginationTemplate.render({pages: pages, activePage: page, numberOfButtons: 5})
		}
	})
})
