FROM node:lts-alpine

# Node environment settings
ENV NODE_ENV=production

# Set workdir name
WORKDIR /TextureExtractor

# Install necessary packages for Node
COPY ["app/package.json", "app/package-lock.json*", "./"]
RUN npm install --production --silent

# Expose port of docker for connection
EXPOSE 8000

# Set previleges for node
RUN chown -R node /TextureExtractor
USER node

# Start server
WORKDIR /TextureExtractor/app
CMD ["nohup", "node", "nodeServer.js", "&"]