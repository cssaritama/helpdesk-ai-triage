FROM node:20-alpine

WORKDIR /app
COPY package.json /app/package.json
RUN npm install

COPY vite.config.ts tsconfig.json /app/
COPY src /app/src

EXPOSE 5173
CMD ["npm", "run", "dev"]
