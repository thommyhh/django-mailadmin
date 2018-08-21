export default function() {
	return `
<ul class="list">
	{% for domain in results %}
		{% if loop.index !== 3 %}
			{% set active = true %}
		{% endif %}
		<li class="list__item js-list-item">
			<div class="list__group list__group--title">
				<a href="#" class="list__link" title="{{ domain }}">
					<h3 class="list__title">{{ domain }}</h3>
				</a>
	
				<button class="icon-button icon-button--active-rotate list__toggle-button js-toggle-button">
					<svg class="icon-button__icon">
						<use xlink:href="assets/icons.svg#dropdown-icon"/>
					</svg>
					<span class="sr-only">Show Actions</span>
				</button>
			</div>
	
			<div class="list__group list__group--actions js-toggle-panel">
				<div class="list__action-group">
					<input class="form__checkbox-input" type="checkbox" name="{{ domain }}-active" value="1"
						   id="{{ domain }}-active"{% if active %} checked="checked"{% endif %} />
					<label class="form__checkbox-label" for="{{ domain }}-active">Active</label>
				</div>
	
				<div class="list__action-group">
					<button class="button button--icon">
						<svg class="button__icon">
							<use xlink:href="assets/icons.svg#group-icon"/>
						</svg>
						<span class="button__text sr-only-sm sr-only-md">Aliases</span>
					</button>
	
					<button class="button button--icon">
						<svg class="button__icon">
							<use xlink:href="assets/icons.svg#device-hub-icon"/>
						</svg>
						<span class="button__text sr-only-sm sr-only-md">Mailing Lists</span>
					</button>
	
					<button class="button button--icon">
						<svg class="button__icon">
							<use xlink:href="assets/icons.svg#forward-icon"/>
						</svg>
						<span class="button__text sr-only-sm sr-only-md">Forwards</span>
					</button>
				</div>
	
				<div class="list__action-group">
					<button class="button button--icon">
						<svg class="button__icon">
							<use xlink:href="assets/icons.svg#settings-icon"/>
						</svg>
						<span class="button__text sr-only-sm sr-only-md sr-only-lg">Settings</span>
					</button>
	
					<button class="button button--icon">
						<svg class="button__icon">
							<use xlink:href="assets/icons.svg#delete-icon"/>
						</svg>
						<span class="button__text sr-only-sm sr-only-md sr-only-lg">Delete</span>
					</button>
				</div>
			</div>
		</li>
	{% endfor %}
</ul>
`
}
