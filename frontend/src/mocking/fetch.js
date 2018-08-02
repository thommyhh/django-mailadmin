let fetchMock = require('fetch-mock')
let nunjucks = require('nunjucks')
nunjucks.configure({
	autoescape: true
})
let dropDownResultTemplate = nunjucks.compile(`
<ul class="dropdown__list">
	{% if results|length > 0 %}
		{% for item in results %}
			<li class="dropdown__item" data-value="{{ item.id }}"><a href="#" class="dropdown__link">{{ item.name }}</a></li>
		{% endfor %}
	{% else %}
		<li class="dropdown__item">No matching results</li>
	{% endif %}
</ul>
`)
let dropDownResult = require('./dummyDropDownData')

fetchMock.config.fallbackToNetwork = true
fetchMock.mock('begin:/dummy/data/auto-complete', (url, options) => {
	/\?q=(.+)/.test(url)
	let results = []
	for (let index in dropDownResult) {
		if (dropDownResult.hasOwnProperty(index) && dropDownResult[index].name.indexOf(RegExp.$1) > -1 && results.length < 5) {
			results.push(dropDownResult[index])
		}
	}
	return dropDownResultTemplate.render({results: results})
})
