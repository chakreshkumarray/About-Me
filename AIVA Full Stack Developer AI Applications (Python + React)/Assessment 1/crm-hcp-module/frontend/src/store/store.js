import { configureStore } from '@reduxjs/toolkit';
import formReducer from './formSlice';

/**
 * Redux Store Configuration
 * Manages global state for the CRM-HCP application
 */
export const store = configureStore({
  reducer: {
    form: formReducer,
    // Add more reducers here as needed
    // chat: chatReducer,
    // patient: patientReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['form/setFormData'],
        ignoredPaths: ['form.data'],
      },
    }),
});

export default store;