let gulp = require('gulp')
let svgSprite = require('gulp-svg-sprites')

gulp.task('svg-sprite', function() {
	return gulp.src('src/components/icons/*.svg')
		.pipe(svgSprite({
			mode: 'symbols',
			svgId: '%f-icon',
			svg: {
				symbols: 'icons.svg'
			}
		}))
		.pipe(gulp.dest('src/assets/'))
})
