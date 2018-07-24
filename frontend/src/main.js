// Import JavaScript
import './components'

// Import CSS
import './main.scss'

// Import Frond End Styleguide JavaScript and CSS
if (process.env.NODE_ENV === 'development') {
  require('../config/branding.scss')
}
