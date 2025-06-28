# API Documentation - Authentification JWT

## Base URL
```
http://localhost:8000/users/
```

## Endpoints

### 1. Inscription (Register)
**POST** `/register/`

**Corps de la requête :**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "motdepasse123",
    "password2": "motdepasse123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-01-01"
}
```

**Réponse :**
```json
{
    "message": "Utilisateur créé avec succès",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+1234567890",
        "date_of_birth": "1990-01-01",
        "is_verified": false,
        "created_at": "2024-01-01T12:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

### 2. Connexion (Login)
**POST** `/login/`

**Corps de la requête :**
```json
{
    "email": "john@example.com",
    "password": "motdepasse123"
}
```

**Réponse :**
```json
{
    "message": "Connexion réussie",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+1234567890",
        "date_of_birth": "1990-01-01",
        "is_verified": false,
        "created_at": "2024-01-01T12:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

### 3. Rafraîchissement du Token
**POST** `/token/refresh/`

**Corps de la requête :**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Réponse :**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 4. Déconnexion (Logout)
**POST** `/logout/`

**Headers :**
```
Authorization: Bearer <access_token>
```

**Corps de la requête :**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Réponse :**
```json
{
    "message": "Déconnexion réussie"
}
```

### 5. Profil Utilisateur
**GET** `/profile/`

**Headers :**
```
Authorization: Bearer <access_token>
```

**Réponse :**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-01-01",
    "is_verified": false,
    "created_at": "2024-01-01T12:00:00Z"
}
```

**PUT/PATCH** `/profile/`

**Headers :**
```
Authorization: Bearer <access_token>
```

**Corps de la requête :**
```json
{
    "first_name": "John Updated",
    "phone_number": "+1234567891"
}
```

### 6. Informations Utilisateur
**GET** `/user-info/`

**Headers :**
```
Authorization: Bearer <access_token>
```

**Réponse :** (même format que le profil)

### 7. Demande de Réinitialisation de Mot de Passe
**POST** `/password/reset/`

**Corps de la requête :**
```json
{
    "email": "john@example.com"
}
```

**Réponse :**
```json
{
    "message": "Un email de réinitialisation a été envoyé à votre adresse email."
}
```

### 8. Confirmation de Réinitialisation de Mot de Passe
**POST** `/password/reset/confirm/`

**Corps de la requête :**
```json
{
    "token": "abc123def456...",
    "new_password": "nouveaumotdepasse123",
    "new_password2": "nouveaumotdepasse123"
}
```

**Réponse :**
```json
{
    "message": "Mot de passe mis à jour avec succès."
}
```

### 9. Changement de Mot de Passe
**POST** `/password/change/`

**Headers :**
```
Authorization: Bearer <access_token>
```

**Corps de la requête :**
```json
{
    "old_password": "ancienmotdepasse",
    "new_password": "nouveaumotdepasse123",
    "new_password2": "nouveaumotdepasse123"
}
```

**Réponse :**
```json
{
    "message": "Mot de passe modifié avec succès."
}
```

## Utilisation des Tokens JWT

### Authentification
Pour les endpoints protégés, incluez le token d'accès dans l'en-tête :
```
Authorization: Bearer <access_token>
```

### Durée de vie des tokens
- **Access Token** : 60 minutes
- **Refresh Token** : 24 heures

### Gestion des erreurs
Les erreurs communes incluent :
- `400 Bad Request` : Données invalides
- `401 Unauthorized` : Token manquant ou invalide
- `403 Forbidden` : Permissions insuffisantes
- `404 Not Found` : Ressource non trouvée

## Test avec curl

### Inscription
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Connexion
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Accès au profil (avec token)
```bash
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <access_token>"
```

## Configuration Email

Pour la production, configurez les paramètres SMTP dans `settings.py` :

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

## Sécurité

- Les mots de passe sont hashés avec bcrypt
- Les tokens JWT sont signés avec HS256
- Les tokens de récupération expirent après 24 heures
- CORS est configuré pour le développement (à ajuster pour la production) 