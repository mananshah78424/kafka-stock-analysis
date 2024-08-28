# Use the official Node.js image with Alpine for a smaller size
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port Vite runs on (default is 5173)
EXPOSE 5173

# Start the Vite development server with hot-reloading
CMD ["npm", "run", "dev"]
