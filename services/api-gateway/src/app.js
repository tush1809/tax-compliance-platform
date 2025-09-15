const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 8080;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

// Service URLs
const services = {
    aiService: process.env.AI_SERVICE_URL || 'http://localhost:8000',
    taxEngine: process.env.TAX_ENGINE_URL || 'http://localhost:5000'
};

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'healthy', service: 'api-gateway' });
});

// Tax calculation endpoint
app.post('/api/calculate-tax', async (req, res) => {
    try {
        console.log('Tax calculation request:', req.body);

        // Forward request to AI service correct endpoint
        const response = await axios.post(
            `${services.aiService}/api/v1/tax/calculate`,
            req.body,
            { timeout: 30000 }
        );

        res.json(response.data);
    } catch (error) {
        console.error('Error calling AI service:', error.message);
        res.status(500).json({
            error: 'Tax calculation failed',
            details: error.message
        });
    }
});

// Compare regimes endpoint
app.post('/api/compare-regimes', async (req, res) => {
    try {
        console.log('Compare regimes request:', req.body);

        const response = await axios.post(
            `${services.aiService}/api/v1/tax/compare-regimes`,
            req.body,
            { timeout: 30000 }
        );

        res.json(response.data);
    } catch (error) {
        console.error('Error calling AI service:', error.message);
        res.status(500).json({
            error: 'Comparison failed',
            details: error.message
        });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`API Gateway running on port ${PORT}`);
    console.log('Service URLs:', services);
});

