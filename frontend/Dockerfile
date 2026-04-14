# ---------- BUILD STAGE ----------
FROM node:18 AS builder

WORKDIR /app

# Copy package files first (for caching)
COPY package*.json ./

RUN npm install

# Copy rest of code
COPY . .

# Build Next.js app
RUN npm run build


# ---------- PRODUCTION STAGE ----------
FROM node:18-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app ./

# Expose Next.js port
EXPOSE 3000

# Start production server
CMD ["npm", "start"]