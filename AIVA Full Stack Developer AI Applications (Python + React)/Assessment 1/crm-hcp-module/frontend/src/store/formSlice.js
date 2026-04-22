import { createSlice } from '@reduxjs/toolkit';

/**
 * Redux Slice for Form State Management
 * Handles form data synchronization and validation
 */
const initialState = {
  formData: {
    hcpInfo: {
      hcpName: '',
      specialization: '',
      licenseNumber: '',
      email: '',
      phone: '',
    },
    interactionInfo: {
      hcpId: '',
      interactionType: '',
      notes: '',
      sentiment: 'neutral',
      samplesDiscussed: '',
    },
  },
  isLoading: false,
  error: null,
  lastSubmitted: null,
};

const formSlice = createSlice({
  name: 'form',
  initialState,
  reducers: {
    /**
     * Update a specific form field
     */
    updateFormField: (state, action) => {
      const { section, field, value } = action.payload;
      if (state.formData[section]) {
        state.formData[section][field] = value;
      }
      state.error = null;
    },

    /**
     * Update entire form section
     */
    updateFormSection: (state, action) => {
      const { section, data } = action.payload;
      if (state.formData[section]) {
        state.formData[section] = { ...state.formData[section], ...data };
      }
      state.error = null;
    },

    /**
     * Set complete form data
     */
    setFormData: (state, action) => {
      state.formData = action.payload;
      state.error = null;
    },

    /**
     * Reset form to initial state
     */
    resetForm: (state) => {
      state.formData = initialState.formData;
      state.error = null;
      state.isLoading = false;
      state.lastSubmitted = null;
    },

    /**
     * Reset specific form section
     */
    resetFormSection: (state, action) => {
      const section = action.payload;
      if (state.formData[section]) {
        state.formData[section] = initialState.formData[section];
      }
    },

    /**
     * Set loading state
     */
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },

    /**
     * Set error state
     */
    setError: (state, action) => {
      state.error = action.payload;
      state.isLoading = false;
    },

    /**
     * Set last submitted data
     */
    setLastSubmitted: (state, action) => {
      state.lastSubmitted = action.payload;
      state.isLoading = false;
    },

    /**
     * Clear error
     */
    clearError: (state) => {
      state.error = null;
    },
  },
});

export const {
  updateFormField,
  updateFormSection,
  setFormData,
  resetForm,
  resetFormSection,
  setLoading,
  setError,
  setLastSubmitted,
  clearError,
} = formSlice.actions;

export default formSlice.reducer;