//Header js for landing page
document.addEventListener('DOMContentLoaded', () => {
        const themeToggleButton = document.getElementById('theme-toggle-button');
        const themeIcon = document.getElementById('theme-icon');
        const body = document.body;

        const themeToggleButtonMobile = document.getElementById('theme-toggle-button-mobile');
        const themeIconMobile = document.getElementById('theme-icon-mobile');

        const hamburgerIcon = document.querySelector('.hamburger-icon');
        const mobileMenu = document.getElementById('mobile-menu');
        const closeMenu = document.querySelector('.close-menu');

        const accountIcon = document.getElementById('account-icon');
        const accountSettings = document.getElementById('account-settings');
        const accountIconMobile = document.getElementById('account-icon-mobile');
        const accountSettingsMobile = document.getElementById('account-settings-mobile');

        themeToggleButton.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            themeIcon.textContent = body.classList.contains('dark-mode') ? 'dark_mode' : 'light_mode';
        });

        themeToggleButtonMobile.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            themeIconMobile.textContent = body.classList.contains('dark-mode') ? 'dark_mode' : 'light_mode';
        });

        hamburgerIcon.addEventListener('click', () => {
            mobileMenu.classList.toggle('open');
        });

        closeMenu.addEventListener('click', () => {
            mobileMenu.classList.remove('open');
        });

        accountIcon.addEventListener('click', () => {
            accountSettings.style.display = accountSettings.style.display === 'block' ? 'none' : 'block';
        });

        accountIconMobile.addEventListener('click', () => {
            accountSettingsMobile.style.display = accountSettingsMobile.style.display === 'block' ? 'none' : 'block';
        });
    });

//