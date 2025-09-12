# Use Node.js 18 Alpine image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies (production only)
RUN npm ci --only=production

# Copy the main index.js and source files
#COPY index.js ./
COPY src/ ./src/

# Expose port
EXPOSE 8080

# Start the application
CMD ["node", "src/app.js"]

