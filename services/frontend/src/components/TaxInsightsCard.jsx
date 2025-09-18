import React from 'react';

const TaxInsightsCard = ({ title, description, icon, onLearnMore }) => (
  <div className="transform hover:scale-105 transition-transform duration-300">
    <div className="bg-gray-900 rounded-2xl shadow-xl p-6 border border-gray-800 hover:border-blue-500 h-full flex flex-col">
      <div className="flex items-start mb-4">
        <span className="text-3xl mr-3">{icon}</span>
        <h3 className="text-xl font-bold text-white">{title}</h3>
      </div>
      <p className="text-gray-300 mb-6 flex-grow">{description}</p>
      <button
        onClick={onLearnMore}
        className="inline-flex items-center text-blue-400 hover:text-blue-300 font-medium transition-colors duration-200"
      >
        Learn More
        <span className="ml-2">→</span>
      </button>
    </div>
  </div>
);

export default TaxInsightsCard;