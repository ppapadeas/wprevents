var gulp = require('gulp');
var browserify = require('gulp-browserify');
var sass = require('gulp-ruby-sass');
var size = require('gulp-size');
var uglify = require('gulp-uglify');


var staticDir = '../wprevents/base/static';

function logError(error) {
  console.error('\nError:', error.plugin);
  console.error(error.message);
}

function onChange(event) {
  console.log('File', event.type +':', event.path);
}

// JavaScript
gulp.task('scripts-prod', function() {
  gulp.src('js/app.js')
    .pipe(browserify())
    .pipe(uglify())
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/js'));

  gulp.src('js/admin.js')
    .pipe(browserify())
    .pipe(uglify())
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/js'));
});

gulp.task('scripts-dev', function() {
  gulp.src('js/app.js')
    .pipe(browserify({ debug: true }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/js'));

  gulp.src('js/admin.js')
    .pipe(browserify({ debug: true }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/js'));
});

// CSS
gulp.task('sass-prod', function() {
  gulp.src('scss/main.scss')
    .pipe(sass({ sourcemap: false }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/css'));

  gulp.src('scss/admin.scss')
    .pipe(sass({ sourcemap: false }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/css'));
});

gulp.task('sass-dev', function() {
  gulp.src('scss/main.scss')
    .pipe(sass({ sourcemap: true }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/css'));

  gulp.src('scss/admin.scss')
    .pipe(sass({ sourcemap: true }))
    .on('error', logError)
    .pipe(size({ showFiles: true }))
    .pipe(gulp.dest(staticDir + '/css'));
});

// Watchers
gulp.task('watch', function() {
  gulp.watch('js/**/*', ['scripts-dev'])
    .on('change', onChange);

  gulp.watch('scss/**/*', ['sass-dev'])
    .on('change', onChange);
});

gulp.task('default', ['dev']);

gulp.task('dev', ['build-dev', 'watch']);

gulp.task('build-prod', ['scripts-prod', 'sass-prod']);

gulp.task('build-dev', ['scripts-dev', 'sass-dev']);
