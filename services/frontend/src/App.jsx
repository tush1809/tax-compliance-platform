import React from 'react';
import TaxCalculator from './components/TaxCalculator';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-3xl font-bold text-center">
          AI-Powered Tax Compliance Platform
        </h1>
        <p className="text-center mt-2">Intelligent Tax Planning with AWS Bedrock</p>
      </header>
      
      <main className="container mx-auto px-4 py-8">
        <TaxCalculator />
      </main>
    </div>
  );
}

export default App;
