import DropDown from './components/dropdown/dropdown'

let dropDowns = document.querySelectorAll('.js-dropdown, .js-auto-complete')
if (dropDowns) {
	dropDowns.forEach(dropDown => {
		DropDown(dropDown)
	})
}
