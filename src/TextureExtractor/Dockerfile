FROM node:lts-alpine

# Node environment settings
ENV NODE_ENV=production

# Set workdir name and copy content
WORKDIR /TextureExtractor
# COPY . .

# Install necessary packages for Node
COPY ["package.json", "package-lock.json*", "./"]
RUN npm install --production --silent

# Expose port of docker for connection
EXPOSE 8000

# Set previleges for node
RUN chown -R node /TextureExtractor
USER node

# Start server
WORKDIR /TextureExtractor/app
CMD ["node", "nodeServer.js"]