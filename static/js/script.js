// Form validation and interactivity
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');
    const togglePassword = document.getElementById('togglePassword');
    const loginBtn = loginForm.querySelector('.login-btn');

    // Password toggle functionality
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // Animate the icon
        this.style.transform = 'scale(0.8)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });

    // Real-time validation for username
    usernameInput.addEventListener('input', function() {
        validateUsername();
    });

    usernameInput.addEventListener('blur', function() {
        validateUsername();
    });

    // Real-time validation for password
    passwordInput.addEventListener('input', function() {
        validatePassword();
    });

    passwordInput.addEventListener('blur', function() {
        validatePassword();
    });

    // Username validation
    function validateUsername() {
        const username = usernameInput.value.trim();
        
        if (username === '') {
            setError(usernameInput, usernameError, 'Username is required');
            return false;
        } else if (username.length < 3) {
            setError(usernameInput, usernameError, 'Username must be at least 3 characters');
            return false;
        } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            setError(usernameInput, usernameError, 'Username can only contain letters, numbers, and underscores');
            return false;
        } else {
            setSuccess(usernameInput, usernameError);
            return true;
        }
    }

    // Password validation
    function validatePassword() {
        const password = passwordInput.value;
        
        if (password === '') {
            setError(passwordInput, passwordError, 'Password is required');
            return false;
        } else if (password.length < 6) {
            setError(passwordInput, passwordError, 'Password must be at least 6 characters');
            return false;
        } else {
            setSuccess(passwordInput, passwordError);
            return true;
        }
    }

    // Set error state
    function setError(input, errorElement, message) {
        input.classList.remove('valid');
        input.classList.add('invalid');
        errorElement.textContent = message;
        
        // Shake animation
        input.style.animation = 'shake 0.3s';
        setTimeout(() => {
            input.style.animation = '';
        }, 300);
    }

    // Set success state
    function setSuccess(input, errorElement) {
        input.classList.remove('invalid');
        input.classList.add('valid');
        errorElement.textContent = '';
    }

    // Form submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate all fields
        const isUsernameValid = validateUsername();
        const isPasswordValid = validatePassword();
        
        if (isUsernameValid && isPasswordValid) {
            // Add loading state
            loginBtn.classList.add('loading');
            
            // Simulate API call delay (remove in production)
            setTimeout(() => {
                // Submit the form
                loginForm.submit();
            }, 800);
        } else {
            // Focus on first invalid field
            if (!isUsernameValid) {
                usernameInput.focus();
            } else if (!isPasswordValid) {
                passwordInput.focus();
            }
        }
    });

    // Add shake animation to CSS dynamically
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
    `;
    document.head.appendChild(style);

    // Add floating label effect
    const inputs = [usernameInput, passwordInput];
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
            this.parentElement.style.transition = 'transform 0.2s';
        });

        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });

    // Social button interactions
    const socialButtons = document.querySelectorAll('.social-btn');
    socialButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.background = 'rgba(102, 126, 234, 0.5)';
            ripple.style.borderRadius = '50%';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s ease-out';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
            
            // Show alert
            alert(`${this.textContent.trim()} login is not implemented in this demo`);
        });
    });

    // Add ripple animation
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);

    // Forgot password link
    const forgotPasswordLink = document.querySelector('.forgot-password');
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Password reset functionality is not implemented in this demo');
        });
    }

    // Sign up link
    const signupLink = document.querySelector('.signup-link a');
    if (signupLink) {
        signupLink.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Sign up functionality is not implemented in this demo');
        });
    }

    // Remember me checkbox animation
    const rememberCheckbox = document.getElementById('remember');
    if (rememberCheckbox) {
        rememberCheckbox.addEventListener('change', function() {
            const checkmark = this.nextElementSibling;
            if (this.checked) {
                checkmark.style.animation = 'checkPop 0.3s ease-out';
            }
            setTimeout(() => {
                checkmark.style.animation = '';
            }, 300);
        });
    }

    // Add check pop animation
    const checkPopStyle = document.createElement('style');
    checkPopStyle.textContent = `
        @keyframes checkPop {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
    `;
    document.head.appendChild(checkPopStyle);

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideUp 0.4s ease-out reverse';
            setTimeout(() => {
                alert.remove();
            }, 400);
        }, 5000);
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Alt + U to focus username
        if (e.altKey && e.key === 'u') {
            e.preventDefault();
            usernameInput.focus();
        }
        // Alt + P to focus password
        if (e.altKey && e.key === 'p') {
            e.preventDefault();
            passwordInput.focus();
        }
    });

    // Add entrance animation to form elements
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        setTimeout(() => {
            group.style.transition = 'all 0.5s ease-out';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, 100 * index);
    });

    // Prevent form submission on Enter in social buttons
    document.querySelectorAll('.social-btn').forEach(btn => {
        btn.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.click();
            }
        });
    });

    // Add focus trap for accessibility
    const focusableElements = loginForm.querySelectorAll(
        'input, button, a, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    loginForm.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusable) {
                    e.preventDefault();
                    lastFocusable.focus();
                }
            } else {
                if (document.activeElement === lastFocusable) {
                    e.preventDefault();
                    firstFocusable.focus();
                }
            }
        }
    });

    // Console easter egg
    console.log('%c🎨 Beautiful Login Page', 'font-size: 20px; color: #667eea; font-weight: bold;');
    console.log('%cDemo Credentials:', 'font-size: 14px; color: #764ba2; font-weight: bold;');
    console.log('%cUsername: admin | Password: admin123', 'font-size: 12px; color: #666;');
    console.log('%cUsername: user | Password: user123', 'font-size: 12px; color: #666;');
});
