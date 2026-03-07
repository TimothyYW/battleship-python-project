FROM node:18-alpine

# Install dependencies needed for node-pty
RUN apk add --no-cache python3 make g++ bash

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy app source
COPY . .

# Railway injects PORT automatically
ENV PORT=3000

EXPOSE 3000

CMD ["node", "index.js"]
