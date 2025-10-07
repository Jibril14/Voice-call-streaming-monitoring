# Step 1: Build the React (Vite) app
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Build the app for production (Vite will output to /dist)
RUN npm run build

# Step 2: Serve with Nginx
FROM nginx:alpine

# Remove the default Nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy the Vite build output (dist folder)
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
