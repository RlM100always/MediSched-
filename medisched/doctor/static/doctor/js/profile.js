// Example: preview image before upload
const profileInput = document.querySelector('input[name="profile_image"]');
const profileImg = document.querySelector('.profile-img');

profileInput?.addEventListener('change', e => {
    const file = e.target.files[0];
    if (file) {
        profileImg.src = URL.createObjectURL(file);
    }
});
