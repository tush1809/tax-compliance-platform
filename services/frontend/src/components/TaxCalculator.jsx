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
  const [error, setError] = useState(null);
  const [showFullInsights, setShowFullInsights] = useState(false);

  const calculateTax = async () => {
    setLoading(true);
    setError(null);
    setShowFullInsights(false);
    
    try {
      const response = await axios.post('/api/calculate-tax', {
        income: parseFloat(formData.income),
        age: parseInt(formData.age),
        regime: formData.regime,
        is_salaried: true
      });
      
      setResult(response.data);
    } catch (error) {
      setError('Failed to calculate tax. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Simple markdown to HTML converter for AI insights
  const renderMarkdown = (text) => {
    if (!text) return '';
    
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold
      .replace(/\*(.*?)\*/g, '<em>$1</em>')              // Italic
      .replace(/### (.*?)\n/g, '<h3 class="font-semibold text-lg mt-4 mb-2 text-blue-800">$1</h3>')  // H3
      .replace(/## (.*?)\n/g, '<h2 class="font-bold text-xl mt-4 mb-3 text-blue-900">$1</h2>')       // H2
      .replace(/# (.*?)\n/g, '<h1 class="font-bold text-2xl mt-4 mb-3 text-blue-900">$1</h1>')       // H1
      .replace(/\n\n/g, '</p><p class="mb-2">')          // Paragraphs
      .replace(/\n/g, '<br/>')                           // Line breaks
      .replace(/- (.*?)(?=\n|$)/g, '<li class="ml-4 list-disc">$1</li>'); // Lists
  };

  const getInsightsPreview = () => {
    if (!result?.ai_insights) return '';
    const preview = result.ai_insights.substring(0, 200) + '...';
    return renderMarkdown(preview);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🧮 AI-Powered Tax Calculator
          </h1>
          <p className="text-lg text-gray-600">FY 2025-26 | Union Budget Compliant</p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              📊 Tax Information
            </h2>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Annual Income (₹)
                </label>
                <input
                  type="number"
                  value={formData.income}
                  onChange={(e) => setFormData({...formData, income: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-lg"
                  placeholder="Enter your annual income"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Age
                </label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={(e) => setFormData({...formData, age: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-lg"
                  placeholder="Enter your age"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Tax Regime
                </label>
                <select
                  value={formData.regime}
                  onChange={(e) => setFormData({...formData, regime: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-lg bg-white"
                >
                  <option value="new">✨ New Regime (Recommended)</option>
                  <option value="old">📋 Old Regime</option>
                </select>
              </div>

              <button
                onClick={calculateTax}
                disabled={loading || !formData.income || !formData.age}
                className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-300 ${
                  loading || !formData.income || !formData.age
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 shadow-lg'
                }`}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                    Calculating with AI...
                  </div>
                ) : (
                  '🚀 Calculate Tax with AI Insights'
                )}
              </button>
            </div>
          </div>

          {/* Results */}
          <div className="space-y-6">
            {error && (
              <div className="bg-red-50 border-l-4 border-red-400 p-6 rounded-xl">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">❌</span>
                  <p className="text-red-700 font-medium">{error}</p>
                </div>
              </div>
            )}

            {result && (
              <>
                {/* Tax Summary */}
                <div className="bg-white rounded-2xl shadow-xl p-8">
                  <h3 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
                    🎯 Tax Calculation Results
                  </h3>

                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div className="bg-blue-50 p-4 rounded-xl">
                      <p className="text-sm text-blue-600 font-semibold">Gross Income</p>
                      <p className="text-2xl font-bold text-blue-800">
                        ₹{result.gross_income?.toLocaleString('en-IN')}
                      </p>
                    </div>
                    
                    <div className={`p-4 rounded-xl ${result.final_tax === 0 ? 'bg-green-50' : 'bg-orange-50'}`}>
                      <p className={`text-sm font-semibold ${result.final_tax === 0 ? 'text-green-600' : 'text-orange-600'}`}>
                        Final Tax
                      </p>
                      <p className={`text-2xl font-bold ${result.final_tax === 0 ? 'text-green-800' : 'text-orange-800'}`}>
                        ₹{result.final_tax?.toLocaleString('en-IN')}
                      </p>
                    </div>

                    <div className="bg-indigo-50 p-4 rounded-xl">
                      <p className="text-sm text-indigo-600 font-semibold">Effective Rate</p>
                      <p className="text-2xl font-bold text-indigo-800">
                        {result.effective_rate?.toFixed(2)}%
                      </p>
                    </div>

                    <div className="bg-purple-50 p-4 rounded-xl">
                      <p className="text-sm text-purple-600 font-semibold">Regime</p>
                      <p className="text-2xl font-bold text-purple-800">
                        {result.regime?.toUpperCase()}
                      </p>
                    </div>
                  </div>

                  {result.final_tax === 0 && (
                    <div className="bg-gradient-to-r from-green-400 to-emerald-500 text-white p-6 rounded-xl text-center">
                      <div className="text-3xl mb-2">🎉</div>
                      <p className="text-xl font-bold">Congratulations!</p>
                      <p className="text-lg">You pay ZERO tax due to Budget 2025 benefits!</p>
                    </div>
                  )}
                </div>

                {/* AI Insights */}
                {result.ai_insights && result.ai_insights !== "AI insights temporarily unavailable" && (
                  <div className="bg-white rounded-2xl shadow-xl p-8">
                    <div className="flex items-center mb-6">
                      <span className="text-2xl mr-3">🤖</span>
                      <h3 className="text-2xl font-bold text-gray-800">AI-Powered Tax Insights</h3>
                    </div>

                    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-xl border-l-4 border-blue-500">
                      <div 
                        className="prose prose-blue max-w-none text-gray-700 leading-relaxed"
                        dangerouslySetInnerHTML={{
                          __html: `<p class="mb-2">${showFullInsights 
                            ? renderMarkdown(result.ai_insights) 
                            : getInsightsPreview()}</p>`
                        }}
                      />
                      
                      {result.ai_insights.length > 200 && (
                        <button
                          onClick={() => setShowFullInsights(!showFullInsights)}
                          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
                        >
                          {showFullInsights ? '📖 Read Less' : '📚 Read Full Analysis'}
                        </button>
                      )}
                    </div>

                    <div className="mt-4 text-xs text-gray-500 text-center">
                      ✨ Powered by Claude AI | FY 2025-26 Budget Compliant
                    </div>
                  </div>
                )}

                {/* Tax Breakdown */}
                {result.breakdown && result.breakdown.length > 0 && (
                  <div className="bg-white rounded-2xl shadow-xl p-8">
                    <h4 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                      📋 Tax Slab Breakdown
                    </h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-left border-collapse">
                        <thead>
                          <tr className="bg-gray-50">
                            <th className="p-3 font-semibold text-gray-700 border-b">Income Slab</th>
                            <th className="p-3 font-semibold text-gray-700 border-b">Rate</th>
                            <th className="p-3 font-semibold text-gray-700 border-b text-right">Taxable Amount</th>
                            <th className="p-3 font-semibold text-gray-700 border-b text-right">Tax</th>
                          </tr>
                        </thead>
                        <tbody>
                          {result.breakdown.map((slab, index) => (
                            <tr key={index} className="hover:bg-gray-50">
                              <td className="p-3 border-b">{slab.slab}</td>
                              <td className="p-3 border-b font-semibold text-blue-600">{slab.rate}</td>
                              <td className="p-3 border-b text-right">₹{slab.taxable_amount?.toLocaleString('en-IN')}</td>
                              <td className="p-3 border-b text-right font-semibold">₹{slab.tax?.toLocaleString('en-IN')}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </>
            )}

            {!result && !loading && !error && (
              <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
                <div className="text-6xl mb-4">🧮</div>
                <h3 className="text-xl font-semibold text-gray-700 mb-2">Ready to Calculate!</h3>
                <p className="text-gray-500">Enter your details and get instant tax calculations with AI insights</p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500">
          <p className="text-sm">
            🇮🇳 Compliant with FY 2025-26 Union Budget | ⚡ Powered by AI Technology
          </p>
        </div>
      </div>
    </div>
  );
};

export default TaxCalculator;

