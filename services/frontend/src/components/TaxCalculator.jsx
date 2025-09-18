import React, { useState } from 'react';
import axios from 'axios';
import TaxInsightsCard from './TaxInsightsCard';
import InsightModal from './InsightModal';

const TaxCalculator = () => {
  const [selectedInsight, setSelectedInsight] = useState(null);

  // Tax Insights Data with Detailed Content
  const taxInsights = [
    {
      icon: "📊",
      title: "Tax Filing Statistics 2025",
      description: "Over 80M Indians filed their taxes in 2025, showing a 15% increase from previous year. Learn about the growing tax compliance.",
      content: (
        <>
          <h4 className="text-xl font-semibold text-blue-400 mb-4">Key Filing Statistics for 2025</h4>
          <ul className="space-y-4">
            <li>• Total Returns Filed: 80.2 Million (+15% YoY)</li>
            <li>• Digital Filing Rate: 98.5%</li>
            <li>• Average Processing Time: 12 days</li>
            <li>• First-time Filers: 12.3 Million</li>
          </ul>
          <h4 className="text-xl font-semibold text-blue-400 mt-6 mb-4">Compliance Improvements</h4>
          <p>The significant increase in tax compliance can be attributed to:</p>
          <ul className="space-y-2 mt-2">
            <li>• Simplified filing procedures</li>
            <li>• Enhanced digital infrastructure</li>
            <li>• Better taxpayer education</li>
            <li>• Streamlined verification process</li>
          </ul>
        </>
      )
    },
    {
      icon: "📝",
      title: "Form 80 Benefits",
      description: "Maximize your tax savings with Form 80. Claim deductions on rent, education, and medical expenses effectively.",
      content: (
        <>
          <h4 className="text-xl font-semibold text-blue-400 mb-4">Key Deductions Under Form 80</h4>
          <ul className="space-y-4">
            <li>
              <strong className="text-blue-300">House Rent Allowance (HRA)</strong>
              <p>Claim up to 50% of basic salary in metros, 40% in non-metros</p>
            </li>
            <li>
              <strong className="text-blue-300">Education Expenses</strong>
              <p>Deduct tuition fees for up to two children</p>
            </li>
            <li>
              <strong className="text-blue-300">Medical Insurance</strong>
              <p>Up to ₹50,000 for self and family, additional for senior citizens</p>
            </li>
          </ul>
          <div className="mt-6">
            <h4 className="text-xl font-semibold text-blue-400 mb-4">Documentation Required</h4>
            <ul className="list-disc pl-4 space-y-2">
              <li>Rent receipts or lease agreement</li>
              <li>Education fee receipts</li>
              <li>Medical insurance premium receipts</li>
              <li>Investment proofs</li>
            </ul>
          </div>
        </>
      )
    },
    {
      icon: "💡",
      title: "Tax Saving Tips",
      description: "Smart strategies to reduce your tax liability through investments, insurance, and other financial instruments.",
      content: (
        <>
          <h4 className="text-xl font-semibold text-blue-400 mb-4">Investment Options</h4>
          <ul className="space-y-4">
            <li>
              <strong className="text-blue-300">Public Provident Fund (PPF)</strong>
              <p>Long-term savings with tax-free returns</p>
            </li>
            <li>
              <strong className="text-blue-300">ELSS Mutual Funds</strong>
              <p>Equity investments with shortest lock-in period</p>
            </li>
            <li>
              <strong className="text-blue-300">National Pension System</strong>
              <p>Additional tax benefit under Section 80CCD(1B)</p>
            </li>
          </ul>
          <h4 className="text-xl font-semibold text-blue-400 mt-6 mb-4">Advanced Strategies</h4>
          <ul className="space-y-2">
            <li>• Salary restructuring</li>
            <li>• Home loan planning</li>
            <li>• Tax-free bonds</li>
            <li>• Health insurance optimization</li>
          </ul>
        </>
      )
    },
    {
      icon: "⚖️",
      title: "Latest Tax Laws",
      description: "Stay updated with the most recent changes in Indian tax laws and how they affect your tax planning.",
      content: (
        <>
          <h4 className="text-xl font-semibold text-blue-400 mb-4">Key Changes in 2025</h4>
          <ul className="space-y-4">
            <li>
              <strong className="text-blue-300">New Tax Regime</strong>
              <p>Simplified structure with modified slabs and no deductions</p>
            </li>
            <li>
              <strong className="text-blue-300">Digital Currency Taxation</strong>
              <p>Updated guidelines for crypto assets and NFTs</p>
            </li>
            <li>
              <strong className="text-blue-300">Green Energy Benefits</strong>
              <p>Additional deductions for renewable energy investments</p>
            </li>
          </ul>
          <div className="mt-6">
            <h4 className="text-xl font-semibold text-blue-400 mb-4">Upcoming Changes</h4>
            <ul className="list-disc pl-4 space-y-2">
              <li>Proposed changes to capital gains taxation</li>
              <li>New deductions for startups</li>
              <li>Digital filing enhancements</li>
            </ul>
          </div>
        </>
      )
    }
  ];
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
    <div className="min-h-screen bg-gradient-to-br from-black to-gray-900 py-8 px-4 relative">
      <div className="max-w-3xl mx-auto mb-24">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-gray-900 rounded-2xl shadow-2xl p-8 border border-gray-800">
            <h2 className="text-3xl font-bold text-white mb-8 text-center">AI Tax Calculator</h2>
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-300 mb-2">
                  Annual Income (₹)
                </label>
                <input
                  type="number"
                  value={formData.income}
                  onChange={(e) => setFormData({...formData, income: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-700 bg-gray-800 text-white rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-lg"
                  placeholder="Enter your annual income"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-300 mb-2">
                  Age
                </label>
                <input
                  type="number"
                  value={formData.age}
                  onChange={(e) => setFormData({...formData, age: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-700 bg-gray-800 text-white rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-lg"
                  placeholder="Enter your age"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-300 mb-2">
                  Tax Regime
                </label>
                <select
                  value={formData.regime}
                  onChange={(e) => setFormData({...formData, regime: e.target.value})}
                  className="w-full px-4 py-3 border-2 border-gray-700 bg-gray-800 text-white rounded-xl focus:border-blue-500 focus:outline-none transition-colors text-lg"
                >
                  <option value="new">✨ New Regime (Recommended)</option>
                  <option value="old">📋 Old Regime</option>
                </select>
              </div>

              <button
                onClick={calculateTax}
                disabled={loading || !formData.income || !formData.age}
                className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all duration-300 mt-8 ${
                  loading || !formData.income || !formData.age
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 transform hover:scale-105 shadow-lg'
                }`}
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                    <span className="text-white">Calculating with AI...</span>
                  </div>
                ) : (
                  <span className="text-white">Calculate Tax with AI Insights</span>
                )}
              </button>
            </div>

            {/* Insights Card Below Button */}
            {result && result.ai_insights && result.ai_insights !== "AI insights temporarily unavailable" && (
              <div className="mt-8">
                <div className="bg-gray-800 border border-blue-700 rounded-2xl shadow-lg p-6">
                  <div className="flex items-center mb-4">
                    <span className="text-2xl mr-3 text-blue-400">🤖</span>
                    <h3 className="text-xl font-bold text-white">AI-Powered Tax Insights</h3>
                  </div>
                  <div 
                    className="prose prose-blue max-w-none text-gray-200 leading-relaxed"
                    dangerouslySetInnerHTML={{
                      __html: `<p class="mb-2">${showFullInsights 
                        ? renderMarkdown(result.ai_insights) 
                        : getInsightsPreview()}</p>`
                    }}
                  />
                  {result.ai_insights.length > 200 && (
                    <button
                      onClick={() => setShowFullInsights(!showFullInsights)}
                      className="mt-4 px-6 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 transition-colors font-semibold"
                    >
                      {showFullInsights ? '📖 Read Less' : '📚 Read Full Analysis'}
                    </button>
                  )}
                </div>
              </div>
            )}
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

            {/* Remove Ready to Calculate message for clean UI */}
          </div>
        </div>

        {/* Tax Insights Cards */}
        <div className="mt-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">
            <span className="bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">Latest Tax Insights</span>
          </h2>
          <div className="tax-insights-grid">
            {taxInsights.map((insight, index) => (
              <TaxInsightsCard
                key={index}
                icon={insight.icon}
                title={insight.title}
                description={insight.description}
                onLearnMore={() => setSelectedInsight(insight)}
              />
            ))}
            
            {/* Insight Modal */}
            <InsightModal
              isOpen={selectedInsight !== null}
              onClose={() => setSelectedInsight(null)}
              title={selectedInsight?.title}
              icon={selectedInsight?.icon}
              content={selectedInsight?.content}
            />
          </div>
        </div>

        {/* Enhanced Footer */}
        <footer className="fixed bottom-0 left-0 right-0 bg-black bg-opacity-90 backdrop-blur-sm py-4 px-6 z-50">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <p className="text-sm text-gray-400">
              🇮🇳 Compliant with FY 2025-26 Union Budget | ⚡ Powered by AI Technology
            </p>
            <p className="text-sm font-semibold bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
              Tush develops ™
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default TaxCalculator;

