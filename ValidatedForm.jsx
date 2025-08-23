import React, { useState, useCallback, useEffect } from 'react';

const ValidatedForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  const [errors, setErrors] = useState({});
  const [debouncedValues, setDebouncedValues] = useState(formData);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Debounce hook implementation
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValues(formData);
    }, 500); // 500ms debounce delay

    return () => clearTimeout(timer);
  }, [formData]);

  // Validation rules
  const validateField = useCallback((name, value) => {
    const newErrors = { ...errors };

    switch (name) {
      case 'email':
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!value) {
          newErrors.email = 'Email is required';
        } else if (!emailRegex.test(value)) {
          newErrors.email = 'Please enter a valid email address';
        } else {
          delete newErrors.email;
        }
        break;

      case 'password':
        if (!value) {
          newErrors.password = 'Password is required';
        } else if (value.length < 8) {
          newErrors.password = 'Password must be at least 8 characters';
        } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
          newErrors.password = 'Password must contain uppercase, lowercase, and number';
        } else {
          delete newErrors.password;
        }
        break;

      case 'confirmPassword':
        if (!value) {
          newErrors.confirmPassword = 'Please confirm your password';
        } else if (value !== debouncedValues.password) {
          newErrors.confirmPassword = 'Passwords do not match';
        } else {
          delete newErrors.confirmPassword;
        }
        break;

      default:
        break;
    }

    return newErrors;
  }, [errors, debouncedValues.password]);

  // Run validation when debounced values change
  useEffect(() => {
    let newErrors = {};
    
    Object.keys(debouncedValues).forEach(field => {
      if (debouncedValues[field]) { // Only validate if field has been touched
        newErrors = { ...newErrors, ...validateField(field, debouncedValues[field]) };
      }
    });

    setErrors(newErrors);
  }, [debouncedValues, validateField]);

  // Handle input changes
  const handleInputChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  }, []);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Final validation
    let finalErrors = {};
    Object.keys(formData).forEach(field => {
      finalErrors = { ...finalErrors, ...validateField(field, formData[field]) };
    });

    if (Object.keys(finalErrors).length > 0) {
      setErrors(finalErrors);
      setIsSubmitting(false);
      return;
    }

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log('Form submitted:', formData);
      alert('Form submitted successfully!');
      
      // Reset form
      setFormData({ email: '', password: '', confirmPassword: '' });
      setErrors({});
    } catch (error) {
      setErrors({ submit: 'Submission failed. Please try again.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  // Input component with error display
  const FormInput = ({ name, type = 'text', placeholder, label }) => (
    <div className="form-group">
      <label htmlFor={name}>{label}</label>
      <input
        id={name}
        name={name}
        type={type}
        value={formData[name]}
        onChange={handleInputChange}
        placeholder={placeholder}
        className={`form-input ${errors[name] ? 'error' : ''}`}
        aria-invalid={!!errors[name]}
        aria-describedby={errors[name] ? `${name}-error` : undefined}
      />
      {errors[name] && (
        <span id={`${name}-error`} className="error-message" role="alert">
          {errors[name]}
        </span>
      )}
    </div>
  );

  const isFormValid = Object.keys(errors).length === 0 && 
                     Object.values(formData).every(value => value.trim() !== '');

  return (
    <div className="validated-form-container">
      <h2>User Registration</h2>
      
      <form onSubmit={handleSubmit} noValidate>
        <FormInput
          name="email"
          type="email"
          label="Email Address"
          placeholder="Enter your email"
        />

        <FormInput
          name="password"
          type="password"
          label="Password"
          placeholder="Enter your password"
        />

        <FormInput
          name="confirmPassword"
          type="password"
          label="Confirm Password"
          placeholder="Confirm your password"
        />

        {errors.submit && (
          <div className="error-message submit-error" role="alert">
            {errors.submit}
          </div>
        )}

        <button
          type="submit"
          disabled={!isFormValid || isSubmitting}
          className="submit-button"
        >
          {isSubmitting ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      {/* Real-time validation status */}
      <div className="validation-status">
        <h3>Validation Status:</h3>
        <ul>
          <li className={formData.email && !errors.email ? 'valid' : 'invalid'}>
            ✓ Valid email address
          </li>
          <li className={formData.password && !errors.password ? 'valid' : 'invalid'}>
            ✓ Strong password
          </li>
          <li className={formData.confirmPassword && !errors.confirmPassword ? 'valid' : 'invalid'}>
            ✓ Passwords match
          </li>
        </ul>
      </div>
    </div>
  );
};

export default ValidatedForm;