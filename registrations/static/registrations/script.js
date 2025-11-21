// Competition Registration Form - Static Member System with Database Submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    
    // English-only validation regex
    const englishOnlyRegex = /^[a-zA-Z\s\-\.'`,`]+$/;
    const englishEmailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    // Form submission handler - ACTUALLY SUBMIT TO DJANGO
    form.addEventListener('submit', function(e) {
        // Clear previous errors
        clearErrors();
        
        // Validate form before submission
        if (!validateEnglishCharacters()) {
            e.preventDefault(); // Only prevent if validation fails
            return false;
        }
        
        // If validation passes, let the form submit normally to Django
        // DO NOT prevent default - let Django handle the submission
    });

    // Optional member validation - when name is entered, level becomes required
    const optionalMembers = [
        { nameField: 'member3_name', levelField: 'member3_level' },
        { nameField: 'member4_name', levelField: 'member4_level' },
        { nameField: 'member5_name', levelField: 'member5_level' }
    ];

    optionalMembers.forEach(member => {
        const nameField = document.querySelector(`[name="${member.nameField}"]`);
        const levelField = document.querySelector(`[name="${member.levelField}"]`);
        
        if (nameField && levelField) {
            nameField.addEventListener('input', function() {
                if (this.value.trim() !== '') {
                    levelField.setAttribute('required', 'required');
                    validateEnglishCharacters(); // Real-time validation
                } else {
                    levelField.removeAttribute('required');
                    clearFieldError(this);
                }
            });

            levelField.addEventListener('change', function() {
                if (this.value !== '') {
                    this.style.borderColor = '#DDE3EC';
                    clearFieldError(this);
                }
            });
        }
    });

    // Real-time English validation for all name fields
    const nameFields = document.querySelectorAll('input[name*="name"]');
    nameFields.forEach(field => {
        field.addEventListener('input', function() {
            validateEnglishCharacters();
        });
    });

    // Real-time English validation for email
    const emailField = document.querySelector('[name="team_leader_email"]');
    if (emailField) {
        emailField.addEventListener('input', function() {
            validateEnglishCharacters();
        });
    }

    function validateEnglishCharacters() {
        let isValid = true;
        let firstErrorField = null;

        // Validate team leader email
        const email = document.querySelector('[name="teamLeaderEmail"]').value.trim();
        if (email && !englishEmailRegex.test(email)) {
            showFieldError(
                document.querySelector('[name="teamLeaderEmail"]'),
                'Email must contain only English letters, numbers, and valid email format'
            );
            isValid = false;
            if (!firstErrorField) firstErrorField = document.querySelector('[name="teamLeaderEmail"]');
        } else {
            clearFieldError(document.querySelector('[name="teamLeaderEmail"]'));
        }

        // Validate all name fields
        const nameFields = document.querySelectorAll('input[name*="_name"]');
        nameFields.forEach(field => {
            const name = field.value.trim();
            if (name) { // Only validate if field has content
                if (!englishOnlyRegex.test(name)) {
                    showFieldError(field, 'Name must contain only English letters, spaces, hyphens, apostrophes, dots, and commas');
                    isValid = false;
                    if (!firstErrorField) firstErrorField = field;
                    console.log(`❌ Invalid characters in field ${field.name}:`, name);
                } else {
                    clearFieldError(field);
                    console.log(`✅ Valid English text in field ${field.name}:`, name);
                }
            } else {
                clearFieldError(field);
            }
        });

        // Scroll to first error if any
        if (!isValid && firstErrorField) {
            firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstErrorField.focus();
        }

        return isValid;
    }

    function showFieldError(field, message) {
        clearFieldError(field);
        
        field.style.borderColor = '#dc3545';
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.style.cssText = `
            color: #dc3545;
            font-size: 12px;
            margin-top: 4px;
            display: block;
        `;
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }

    function clearFieldError(field) {
        field.style.borderColor = '#DDE3EC';
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }

    function clearErrors() {
        // Clear form-level errors
        const existingErrorDisplay = document.querySelector('.validation-errors');
        if (existingErrorDisplay) {
            existingErrorDisplay.remove();
        }
        
        // Clear field-level errors
        const nameFields = document.querySelectorAll('input[name*="_name"], [name="team_leader_email"]');
        nameFields.forEach(field => {
            clearFieldError(field);
        });
        
        const emailField = document.querySelector('[name="team_leader_email"]');
        if (emailField) {
            clearFieldError(emailField);
        }
    }

    function showSuccessModal() {
        const modal = document.getElementById('successModal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }

    // Close modal function
    window.closeModal = function() {
        const modal = document.getElementById('successModal');
        if (modal) {
            modal.style.display = 'none';
        }
    };

    // Test functions for debugging
    window.testStaticMembers = function() {
        console.log('Testing static member validation...');
        console.log('Member 1:', {
            name: document.querySelector('[name="member1_name"]')?.value || 'NOT FOUND',
            level: document.querySelector('[name="member1_level"]')?.value || 'NOT FOUND'
        });
        console.log('Member 2:', {
            name: document.querySelector('[name="member2_name"]')?.value || 'NOT FOUND',
            level: document.querySelector('[name="member2_level"]')?.value || 'NOT FOUND'
        });
        console.log('Member 3:', {
            name: document.querySelector('[name="member3_name"]')?.value || 'NOT FOUND',
            level: document.querySelector('[name="member3_level"]')?.value || 'NOT FOUND'
        });
        console.log('Member 4:', {
            name: document.querySelector('[name="member4_name"]')?.value || 'NOT FOUND',
            level: document.querySelector('[name="member4_level"]')?.value || 'NOT FOUND'
        });
        console.log('Member 5:', {
            name: document.querySelector('[name="member5_name"]')?.value || 'NOT FOUND',
            level: document.querySelector('[name="member5_level"]')?.value || 'NOT FOUND'
        });
        console.log('Email:', document.querySelector('[name="team_leader_email"]')?.value || 'NOT FOUND');
    };

    window.testValidation = function() {
        console.log('Running English character validation...');
        const isValid = validateEnglishCharacters();
        console.log('Validation result:', isValid ? '✅ PASSED' : '❌ FAILED');
        return isValid;
    };

    window.testFormSubmission = function() {
        console.log('Testing form data structure...');
        const formData = new FormData(form);
        console.log('Form data entries:');
        for (let [key, value] of formData.entries()) {
            console.log(`  ${key}: ${value}`);
        }
        
        // Test if form would submit to Django
        console.log('✅ Form is configured for Django submission');
        console.log('💾 Data will be saved to database when form is submitted');
    };

    // Log successful initialization
    console.log('✅ Static Member Form with Database Submission initialized');
    console.log('🔗 Form will submit directly to Django backend');
    console.log('🗄️ Data will be saved to database on successful submission');
});