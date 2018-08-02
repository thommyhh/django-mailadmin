// Import JavaScript
// import './components'
import './application'

// Import CSS
import './main.scss'

// Import Frond End Styleguide JavaScript and CSS
if (process.env.NODE_ENV === 'development') {
	require('../config/branding.scss')
	require('./mocking/fetch')
}
