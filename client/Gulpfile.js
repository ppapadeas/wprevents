var gulp = require('gulp');
var browserify = require('gulp-browserify');
var sass = require('gulp-ruby-sass');
var size = require('gulp-size');


var staticDir = '../mozcal/base/static';

function logError(error) {
  console.error('\nError:', error.plugin);
  console.error(error.message);
}

function onChange(event) {
  console.log('File', event.type +':', event.path);
}

gulp.task('scripts', function() {
  gulp.src('js/app.js')
    .pipe(browserify({
      debug: true
    }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/js'));

  gulp.src('js/admin.js')
    .pipe(browserify({
      debug: true
    }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/js'));
});

gulp.task('sass', function() {
  gulp.src('scss/main.scss')
    .pipe(sass({
      sourcemap: true
    }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/css'));

  gulp.src('scss/admin.scss')
    .pipe(sass({
      sourcemap: true
    }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/css'));
});

gulp.task('watch', function() {
  gulp.watch('js/**/*', ['scripts'])
    .on('change', onChange);

  gulp.watch('scss/**/*', ['sass'])
    .on('change', onChange);
});

gulp.task('default', ['dev']);

gulp.task('dev', ['build', 'watch']);

gulp.task('build', ['scripts', 'sass']);