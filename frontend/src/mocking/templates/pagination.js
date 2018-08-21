export default function() {
	return `
{% if numberOfButtons > pages %}
	{% set numberOfButtons = pages %}
{% endif %}
{% set delta = (numberOfButtons / 2)|round(0, 'floor') %}
{% set visibleRangeStart = activePage - delta %}
{% set visibleRangeEnd = activePage + delta %}
{% if numberOfPages % 2 == 0 %}
	{% set visibleRangeEnd = visibleRangeEnd - 1 %}
{% endif %}
{% if visibleRangeStart < 1 %}
	{% set visibleRangeEnd = visibleRangeEnd - visibleRangeStart + 1 %}
{% endif %}
{% if visibleRangeEnd > pages %}
	{% set visibleRangeStart = visibleRangeStart - visibleRangeEnd + pages %}
{% endif %}
{% if 1 > visibleRangeStart %}
	{% set visibleRangeStart = 1 %}
{% endif %}
{% if pages < visibleRangeEnd %}
	{% set visibleRangeEnd = pages %}
{% endif %}
{% if visibleRangeStart > 2 %}
	{% set hasLess = true %}
{% endif %}
{% if visibleRangeEnd + 1 < pages %}
	{% set hasMore = true %}
{% endif %}
{% for i in range(1, pages + 1) %}
	{% if i >= visibleRangeStart  and i <= visibleRangeEnd %}
		{% if i == visibleRangeStart and visibleRangeStart != 1 %}
			<button class="button pagination__page js-pagination-button" data-page="1">1</button>
			{% if hasLess %}
				<span class="pagination__page">...</span>
			{% endif %}
		{% endif %}
		<button class="button{{ ' button--highlight' if i == activePage }} pagination__page js-pagination-button" data-page="{{ i }}">{{ i }}</button>
		{% if i == visibleRangeEnd and visibleRangeEnd != pages%}
			{% if hasMore %}
				<span class="pagination__page">...</span>
			{% endif %}
			<button class="button pagination__page js-pagination-button" data-page="{{ pages }}">{{ pages }}</button>
		{% endif %}
	{% endif %}
{% endfor %}
`
}
