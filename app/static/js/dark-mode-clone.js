// Select elements correctly using querySelectorAll for icons
var themeToggleBtns = document.querySelectorAll('.theme-toggle'); // Menggunakan querySelectorAll untuk memilih semua elemen dengan kelas theme-toggle

// Function to update icons based on current theme
function updateIcons() {
    themeToggleBtns.forEach(function(themeToggleBtn) {
        var darkIcon = themeToggleBtn.querySelector('#theme-toggle-dark-icon');
        var lightIcon = themeToggleBtn.querySelector('#theme-toggle-light-icon');

        if (localStorage.getItem('color-theme') === 'dark' || (!localStorage.getItem('color-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            lightIcon.classList.add('hidden');
            darkIcon.classList.remove('hidden');
        } else {
            lightIcon.classList.remove('hidden');
            darkIcon.classList.add('hidden');
        }
    });
}

// Initialize icon visibility based on current theme
updateIcons();

// Add event listener to each toggle button
themeToggleBtns.forEach(function(themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function() {
        // Toggle icons inside button
        var darkIcon = themeToggleBtn.querySelector('#theme-toggle-dark-icon');
        var lightIcon = themeToggleBtn.querySelector('#theme-toggle-light-icon');
        
        darkIcon.classList.toggle('hidden');
        lightIcon.classList.toggle('hidden');

        // Toggle dark mode class on <html> element
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }

        // Update icons across all theme-toggle elements
        updateIcons();
    });
});
