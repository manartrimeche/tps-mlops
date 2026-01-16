# Étape 1 : Build de l'application React
FROM node:20-alpine AS builder

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

# Build de l'application
RUN npm run build

# Étape 2 : Déploiement avec Nginx
FROM nginx:alpine

# Copier les fichiers buildés depuis l'étape précédente
COPY --from=builder /app/dist /usr/share/nginx/html

# Copier la configuration Nginx personnalisée (optionnel)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80
EXPOSE 80

# Nginx démarre automatiquement
CMD ["nginx", "-g", "daemon off;"]