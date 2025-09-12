import React, { useState } from 'react';
import axios from 'axios';

const TaxCalculator = () => {
  const [formData, setFormData] = useState({
    income: '',
    age: '',
    regime: 'new'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const calculateTax = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/api/calculate-tax', formData);
      setResult(response.data);
    } catch (error) {
      console.error('Error calculating tax:', error);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Tax Calculator</h2>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Annual Income (₹)
          </label>
          <input
            type="number"
            value={formData.income}
            onChange={(e) => setFormData({...formData, income: e.target.value})}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Age</label>
          <input
            type="number"
            value={formData.age}
            onChange={(e) => setFormData({...formData, age: e.target.value})}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Tax Regime</label>
          <select
            value={formData.regime}
            onChange={(e) => setFormData({...formData, regime: e.target.value})}
            className="mt-1 block w-full border-gray-300 rounded-md shadow-sm"
          >
            <option value="new">New Regime</option>
            <option value="old">Old Regime</option>
          </select>
        </div>
        
        <button
          onClick={calculateTax}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Calculating...' : 'Calculate Tax'}
        </button>
      </div>
      
      {result && (
        <div className="mt-6 p-4 bg-green-50 rounded-md">
          <h3 className="font-semibold text-green-800">Tax Calculation Result</h3>
          <p className="text-green-700">Tax Amount: ₹{result.taxAmount}</p>
          {result.aiInsights && (
            <div className="mt-2">
              <p className="text-sm text-green-600">{result.aiInsights}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TaxCalculator;
