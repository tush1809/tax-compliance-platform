// src/services/taxServices.js
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

export const calculateTax = async (data) => {
  try {
    // FIXED: Use /api/calculate-tax to match your API Gateway
    const response = await fetch(`${API_URL}/api/calculate-tax`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error calculating tax:', error);
    throw error;
  }
};

