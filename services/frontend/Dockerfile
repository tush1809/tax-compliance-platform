# Use Node 20 LTS (Latest stable as of 2025)
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies first (for better caching)
COPY package*.json ./
RUN npm install

# Copy the rest of the application
COPY . .

# Add node_modules/.bin to PATH
ENV PATH /app/node_modules/.bin:$PATH

# Expose Vite dev server port
EXPOSE 3000

# Set environment variables for Vite
ENV NODE_ENV=development
ENV VITE_HOST=0.0.0.0
ENV VITE_PORT=3000

# Start Vite dev server
CMD ["npm", "run", "dev"]

