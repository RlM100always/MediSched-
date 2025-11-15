// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Hamburger menu toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });
}

// Modal Functions
function openModal(type) {
    document.getElementById(type + 'Modal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(type) {
    document.getElementById(type + 'Modal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function switchModal(from, to) {
    closeModal(from);
    setTimeout(() => openModal(to), 300);
}

// Close modal on outside click
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show Alert
function showAlert(type, elementId, message) {
    const alert = document.getElementById(elementId);
    alert.className = 'alert show alert-' + type;
    alert.textContent = message;
    setTimeout(() => {
        alert.classList.remove('show');
    }, 5000);
}

// Handle Sign In
async function handleSignin(event) {
    event.preventDefault();
    const form = event.target;
    const formData = {
        username: form.username.value,
        password: form.password.value
    };

    try {
        const response = await fetch(signinUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            showAlert('success', 'signinAlert', data.message);
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1000);
        } else {
            showAlert('error', 'signinAlert', data.message);
        }
    } catch (error) {
        showAlert('error', 'signinAlert', 'An error occurred. Please try again.');
    }
}

// Handle Sign Up
async function handleSignup(event) {
    event.preventDefault();
    const form = event.target;
    const formData = {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value,
        user_type: form.user_type.value
    };

    try {
        const response = await fetch(signupUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            showAlert('success', 'signupAlert', data.message);
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1000);
        } else {
            showAlert('error', 'signupAlert', data.message);
        }
    } catch (error) {
        showAlert('error', 'signupAlert', 'An error occurred. Please try again.');
    }
}

// Scroll Animation
const fadeElements = document.querySelectorAll('.fade-in');
const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.1
});
fadeElements.forEach(element => {
    fadeObserver.observe(element);
});

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});
