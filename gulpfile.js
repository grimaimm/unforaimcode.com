const gulp = require('gulp');
const htmlmin = require('gulp-htmlmin');
const uglify = require('gulp-uglify');
const cleanCSS = require('gulp-clean-css');
const concat = require('gulp-concat');
const postcss = require('gulp-postcss');
const tailwindcss = require('tailwindcss');

// Task untuk minifikasi HTML
gulp.task('minify-html', function() {
    return gulp.src('app/templates/**/*.html') // Ubah path sesuai struktur template Anda
        .pipe(htmlmin({ collapseWhitespace: true }))
        .pipe(gulp.dest('dist/templates')); // Simpan file hasil minifikasi ke direktori dist/templates
});

// Task untuk minifikasi JavaScript
// gulp.task('minify-js', function() {
//     return gulp.src('app/static/js/**/*.js') // Ubah path sesuai struktur file JavaScript Anda
//         .pipe(uglify())
//         .pipe(concat('app.min.js')) // Gabung semua file JavaScript menjadi satu file (opsional)
//         .pipe(gulp.dest('dist/static/js')); // Simpan file hasil minifikasi ke direktori dist/static/js
// });

// Task untuk minifikasi CSS
// gulp.task('minify-css', function() {
//     return gulp.src('app/static/css/*.css') // Ubah path sesuai struktur file CSS Anda
//         .pipe(cleanCSS())
//         .pipe(concat('styles.min.css')) // Gabung semua file CSS menjadi satu file (opsional)
//         .pipe(gulp.dest('dist/static/css')); // Simpan file hasil minifikasi ke direktori dist/static/css
// });

// Task untuk minifikasi CSS dengan Tailwind CSS
gulp.task('minify-css', function() {
  return gulp.src('app/static/css/*.css')
      .pipe(postcss([
          tailwindcss(),
          require('autoprefixer'),
      ]))
      .pipe(cleanCSS())
      .pipe(concat('styles.min.css'))
      .pipe(gulp.dest('dist/static/css'));
});

// Task default untuk menjalankan semua task minifikasi
gulp.task('minify-all', gulp.parallel('minify-html', 'minify-css'));

// Export task default agar bisa dijalankan dari command line
exports.default = gulp.series('minify-all');