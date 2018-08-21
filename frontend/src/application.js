import DropDown from './components/dropdown/dropdown'
import List from './components/list/list'

let dropDowns = document.querySelectorAll('.js-dropdown, .js-auto-complete')
if (dropDowns) {
	dropDowns.forEach(dropDown => {
		DropDown(dropDown)
	})
}

let lists = document.querySelectorAll('.js-list')
if (lists) {
	lists.forEach(list => {
		List(list)
	})
}
