"use strict";

// Load plugins
const gulp = require('gulp');
const sass = require('gulp-sass');
const clean_css = require('gulp-clean-css');
const rename = require('gulp-rename');
const plumber = require('gulp-plumber');
const concat = require('gulp-concat');
const terser = require('gulp-terser');
const size = require('gulp-size');


// Variables
const boostrap_bower_path = 'bower_components/bootstrap/scss';
const main_app_css_path = 'apps/main/static/css';
const main_app_js_path = 'apps/main/static/js';
const main_app_extra_js_path = 'apps/main/static/js/extras';
const main_app_scss_src = 'apps/main/static/scss/**/*.scss';
const main_app_scss_root = 'apps/main/static/scss/';


// Main app styles task
function main_app_styles() {
  return gulp.src([main_app_scss_src])
  .pipe(plumber({
    errorHandler: function (err) {
      console.log(err);
      this.emit('end');
    }
  }))
  .pipe(sass({
    includePaths: [boostrap_bower_path]
  }))
  .pipe(size({
    showFiles: true,
    showTotal: false
  }))
  .pipe(clean_css({
    level: {1: {specialComments: false}},
  }))
  .pipe(rename({suffix: '.min'}))
  .pipe(size({
    showFiles: true,
    showTotal: false
  }))
  .pipe(gulp.dest(main_app_css_path));
}


// Main app scripts task
function main_app_scripts() {
  return gulp.src(main_app_js_path + '/_*.js')
  .pipe(plumber({
    errorHandler: function (err) {
      console.log(err);
      this.emit('end');
    }
  }))
  .pipe(concat('app.js'))
  .pipe(size({
    showFiles: true,
    showTotal: false
  }))
  .pipe(terser())
  .pipe(rename({suffix: '.min'}))
  .pipe(size({
    showFiles: true,
    showTotal: false
  }))
  .pipe(gulp.dest(main_app_js_path));
}


// Main app extra scripts task
function main_app_scripts_extra() {
  return gulp.src([main_app_extra_js_path + '/*.js', '!' + main_app_extra_js_path + '/*.min.js'])
  .pipe(plumber({
    errorHandler: function (err) {
      console.log(err);
      this.emit('end');
    }
  }))
  .pipe(size({
    showFiles: true,
    showTotal: false
  }))
  .pipe(terser())
  .pipe(rename({suffix: '.min'}))
  .pipe(rename(function(opt) {
    opt.basename = opt.basename.replace(/^_/, '');
    return opt;
  }))
  .pipe(size({
    showFiles: true,
    showTotal: false
  }))
  .pipe(gulp.dest(main_app_extra_js_path));
}


// Watch task
function watch() {
  gulp.watch(main_app_scss_src, main_app_styles)
  .on('change', function (file) {
    console.log('File ' + file + ' was modified, runnning tasks ...');
  });
  gulp.watch(main_app_js_path + '/_*.js', main_app_scripts)
  .on('change', function (file) {
    console.log('File ' + file + ' was modified, runnning tasks ...');
  });
  gulp.watch(main_app_extra_js_path + '/_*.js', main_app_scripts_extra)
  .on('change', function (file) {
    console.log('File ' + file + ' was modified, runnning tasks ...');
  });
}
gulp.task('watch', gulp.series(watch));
// Default task
gulp.task('default', gulp.series('watch'));
gulp.task('styles', gulp.series(main_app_styles));
gulp.task('scripts', gulp.series(main_app_scripts_extra));
gulp.task('scripts_extras', gulp.series(main_app_scripts_extra));
