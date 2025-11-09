document.addEventListener('DOMContentLoaded', function() {
    const workingHoursInput = document.getElementById('workingHoursInput');
    const fieldsContainer = document.getElementById('workingHoursFields');
    const daySelect = document.getElementById('daySelect');
    const timeInput = document.getElementById('timeInput');
    const addDayButton = document.getElementById('addDay');
    const addExperienceButton = document.getElementById('addExperience');
    const experienceList = document.getElementById('experienceList');

    function updateJSON() {
        const data = {};
        document.querySelectorAll('.time-input').forEach(input => {
            const day = input.getAttribute('data-day');
            const time = input.value.trim();
            if (day && time) data[day] = time;
        });
        workingHoursInput.value = JSON.stringify(data); 
    }

    function createDayField(day, time) {
        const div = document.createElement('div');
        div.classList.add('col-md-6', 'mb-2', 'day-field');
        div.innerHTML = `
            <div class="input-group">
                <span class="input-group-text">${day}</span>
                <input type="text" class="form-control time-input" data-day="${day}" value="${time}">
                <button type="button" class="btn btn-outline-danger remove-day"><i class="fa fa-trash"></i></button>
            </div>`;
        fieldsContainer.appendChild(div);

        div.querySelector('.time-input').addEventListener('input', updateJSON);
        div.querySelector('.remove-day').addEventListener('click', function(e) {
            e.target.closest('.day-field').remove();
            updateJSON();
        });
    }

    addDayButton.addEventListener('click', () => {
        const day = daySelect.value;
        const time = timeInput.value.trim();
        if (!day || !time) return alert('Select a day and enter working hours.');

        if (document.querySelector(`.time-input[data-day="${day}"]`)) 
            return alert('This day is already added.');

        createDayField(day, time);
        daySelect.value = '';
        timeInput.value = '';
        updateJSON();
    });

    document.querySelectorAll('.time-input').forEach(input => input.addEventListener('input', updateJSON));
    document.querySelectorAll('.remove-day').forEach(btn => btn.addEventListener('click', e => { e.target.closest('.day-field').remove(); updateJSON(); }));
    updateJSON();

    addExperienceButton.addEventListener('click', () => {
        const div = document.createElement('div');
        div.classList.add('experience-card');
        div.innerHTML = `
            <div class="row g-2 align-items-center">
                <div class="col-md-4"><input type="text" class="form-control" name="hospital_name" placeholder="Hospital Name"></div>
                <div class="col-md-4"><input type="text" class="form-control" name="designation" placeholder="Designation"></div>
                <div class="col-md-3"><input type="text" class="form-control" name="department" placeholder="Department (Optional)"></div>
                <div class="col-md-1 text-end"><i class="fa-solid fa-trash remove-exp"></i></div>
            </div>`;
        experienceList.appendChild(div);
        div.querySelector('.remove-exp').addEventListener('click', e => div.remove());
    });

    document.querySelectorAll('.remove-exp').forEach(icon => icon.addEventListener('click', e => e.target.closest('.experience-card').remove()));
});

$(document).ready(function() {
    $('select[name="division"]').change(function() {
        var divisionId = $(this).val();
        var districtSelect = $('select[name="district"]');
        var upazilaSelect = $('select[name="upazila"]');

        districtSelect.html('<option value="">Select District</option>');
        upazilaSelect.html('<option value="">Select Upazila</option>');

        if (divisionId) {
            $.ajax({
                url: loadDistrictsUrl, // ✅ এখানে ভ্যারিয়েবল ব্যবহার করা হচ্ছে
                data: { 'division_id': divisionId },
                success: function(data) {
                    $.each(data, function(index, district) {
                        districtSelect.append(
                            $('<option>', {
                                value: district.id,
                                text: district.district_name
                            })
                        );
                    });
                }
            });
        }
    });

    $('select[name="district"]').change(function() {
        var districtId = $(this).val();
        var upazilaSelect = $('select[name="upazila"]');
        upazilaSelect.html('<option value="">Select Upazila</option>');
        if (districtId) {
            $.ajax({
                url: loadUpazilasUrl,
                data: { 'district_id': districtId },
                success: function(data) {
                    $.each(data, function(index, upz) {
                        upazilaSelect.append(
                            $('<option>', {
                                value: upz.id,
                                text: upz.upazila_name
                            })
                        );
                    });
                }
            });
        }
    });
});


$(document).ready(function() {
    // Departments Select2
    $('.select2-departments').select2({
        placeholder: "Select Departments",
        allowClear: true
    });

    // Symptoms Select2
    $('.select2-symptoms').select2({
        placeholder: "Select Symptoms Expertise",
        allowClear: true
    });
});

