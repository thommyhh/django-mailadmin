export default function() {
	return `
<ul class="dropdown__list">
	{% if results|length > 0 %}
		{% for item in results %}
			<li class="dropdown__item" data-value="{{ item.id }}"><a href="#" class="dropdown__link">{{ item.name }}</a></li>
		{% endfor %}
	{% else %}
		<li class="dropdown__item">No matching results</li>
	{% endif %}
</ul>
`
}
