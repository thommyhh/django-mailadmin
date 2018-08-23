export default function() {
	return `
<ul class="list">
	{% for user in results %}
		{% if loop.index !== 3 %}
			{% set active = true %}
		{% endif %}
		<li class="list__item js-list-item">
			<div class="list__group list__group--title">
				<a href="#" class="list__link">
					<h3 class="list__title">
						<span title="{{ user }}@{{ domain }}">{{ user }}@{{ domain }}</span>
					</h3>
				</a>
	
				<button class="icon-button icon-button--active-rotate list__toggle-button js-toggle-button">
					<svg class="icon-button__icon"><use xlink:href="assets/icons.svg#dropdown-icon"/></svg>
					<span class="sr-only">Show Actions</span>
				</button>
			</div>
	
			<div class="list__group list__group--actions js-toggle-panel">
				<div class="list__action-group">
					<input class="form__checkbox-input" type="checkbox" name="{{ from }}-active" value="1" id="{{ from }}-active"{% if active %} checked="checked"{% endif %} />
					<label class="form__checkbox-label" for="{{ from }}-active">Active</label>
				</div>
	
				<div class="list__action-group">
					<button class="button button--icon">
						<svg class="button__icon"><use xlink:href="assets/icons.svg#settings-icon"/></svg>
						<span class="button__text sr-only-md">Settings</span>
					</button>
	
					<button class="button button--icon">
						<svg class="button__icon"><use xlink:href="assets/icons.svg#delete-icon"/></svg>
						<span class="button__text sr-only-md">Delete</span>
					</button>
				</div>
			</div>
		</li>
	{% endfor %}
</ul>
`
}
