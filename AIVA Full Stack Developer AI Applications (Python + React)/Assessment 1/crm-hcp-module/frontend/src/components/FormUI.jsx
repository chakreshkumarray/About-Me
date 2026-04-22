import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  updateFormField,
  updateFormSection,
  resetFormSection,
  setLoading,
  setError,
  setLastSubmitted,
} from '../store/formSlice';
import axios from 'axios';
import './FormUI.css';

/**
 * FormUI Component - Left-side structured form interface
 * Handles HCP info and interaction logging
 */
const FormUI = () => {
  const dispatch = useDispatch();
  const { formData, isLoading, error } = useSelector((state) => state.form);
  const [activeTab, setActiveTab] = useState('hcpInfo');

  /**
   * Handle form field change
   */
  const handleFieldChange = (section, field, value) => {
    dispatch(updateFormField({ section, field, value }));
  };

  /**
   * Handle form section reset
   */
  const handleResetSection = () => {
    dispatch(resetFormSection(activeTab));
  };

  /**
   * Handle form submission
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    dispatch(setLoading(true));

    try {
      const response = await axios.post('http://localhost:8000/api/forms/submit', {
        user_id: 'user_123', // Replace with actual user ID
        form_type: activeTab,
        data: formData[activeTab],
      });

      dispatch(setLastSubmitted({
        type: activeTab,
        data: formData[activeTab],
        timestamp: new Date().toISOString(),
      }));

      alert(`${activeTab} submitted successfully!`);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'An error occurred';
      dispatch(setError(errorMessage));
      console.error('Submission error:', err);
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <div className="form-container">
      <h2>Form Management</h2>

      {/* Tabs for different form sections */}
      <div className="form-tabs">
        <button
          className={`tab-button ${activeTab === 'hcpInfo' ? 'active' : ''}`}
          onClick={() => setActiveTab('hcpInfo')}
        >
          HCP Info
        </button>
        <button
          className={`tab-button ${activeTab === 'interactionInfo' ? 'active' : ''}`}
          onClick={() => setActiveTab('interactionInfo')}
        >
          Log Interaction
        </button>
      </div>

      {/* Error display */}
      {error && <div className="error-message">{error}</div>}

      {/* Form content */}
      <form onSubmit={handleSubmit} className="form-content">
        {activeTab === 'hcpInfo' && (
          <div className="form-section">
            <h3>HCP Information</h3>
            <div className="form-group">
              <label htmlFor="hcp-name">HCP Name</label>
              <input
                id="hcp-name"
                type="text"
                value={formData.hcpInfo.hcpName}
                onChange={(e) =>
                  handleFieldChange('hcpInfo', 'hcpName', e.target.value)
                }
                placeholder="Enter HCP name"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="specialization">Specialization</label>
              <input
                id="specialization"
                type="text"
                value={formData.hcpInfo.specialization}
                onChange={(e) =>
                  handleFieldChange('hcpInfo', 'specialization', e.target.value)
                }
                placeholder="e.g., Cardiology"
              />
            </div>

            <div className="form-group">
              <label htmlFor="license">License Number</label>
              <input
                id="license"
                type="text"
                value={formData.hcpInfo.licenseNumber}
                onChange={(e) =>
                  handleFieldChange('hcpInfo', 'licenseNumber', e.target.value)
                }
                placeholder="MD123456"
              />
            </div>

            <div className="form-group">
              <label htmlFor="hcp-email">Email</label>
              <input
                id="hcp-email"
                type="email"
                value={formData.hcpInfo.email}
                onChange={(e) =>
                  handleFieldChange('hcpInfo', 'email', e.target.value)
                }
                placeholder="hcp@hospital.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="hcp-phone">Phone</label>
              <input
                id="hcp-phone"
                type="tel"
                value={formData.hcpInfo.phone}
                onChange={(e) =>
                  handleFieldChange('hcpInfo', 'phone', e.target.value)
                }
                placeholder="987-654-3210"
              />
            </div>
          </div>
        )}

        {activeTab === 'interactionInfo' && (
          <div className="form-section">
            <h3>Log Interaction</h3>
            <div className="form-group">
              <label htmlFor="hcp-id">HCP ID</label>
              <input
                id="hcp-id"
                type="text"
                value={formData.interactionInfo.hcpId}
                onChange={(e) =>
                  handleFieldChange('interactionInfo', 'hcpId', e.target.value)
                }
                placeholder="Enter HCP ID"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="interaction-type">Interaction Type</label>
              <select
                id="interaction-type"
                value={formData.interactionInfo.interactionType}
                onChange={(e) =>
                  handleFieldChange('interactionInfo', 'interactionType', e.target.value)
                }
              >
                <option value="">Select type</option>
                <option value="meeting">Meeting</option>
                <option value="call">Call</option>
                <option value="email">Email</option>
                <option value="webinar">Webinar</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="notes">Notes</label>
              <textarea
                id="notes"
                value={formData.interactionInfo.notes}
                onChange={(e) =>
                  handleFieldChange('interactionInfo', 'notes', e.target.value)
                }
                placeholder="Enter interaction notes"
                rows="4"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="sentiment">Sentiment</label>
              <select
                id="sentiment"
                value={formData.interactionInfo.sentiment}
                onChange={(e) =>
                  handleFieldChange('interactionInfo', 'sentiment', e.target.value)
                }
              >
                <option value="neutral">Neutral</option>
                <option value="positive">Positive</option>
                <option value="negative">Negative</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="samples">Samples Discussed (comma-separated)</label>
              <input
                id="samples"
                type="text"
                value={formData.interactionInfo.samplesDiscussed}
                onChange={(e) =>
                  handleFieldChange('interactionInfo', 'samplesDiscussed', e.target.value)
                }
                placeholder="e.g., Drug A, Drug B"
              />
            </div>
          </div>
        )}

        {/* Form buttons */}
        <div className="form-buttons">
          <button
            type="reset"
            className="reset-button"
            onClick={handleResetSection}
            disabled={isLoading}
          >
            Reset Form
          </button>
          <button
            type="submit"
            className="submit-button"
            disabled={isLoading}
          >
            {isLoading ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FormUI;
