# API Documentation - SpaceHack2

## Table des matières
- [Authentification](#authentification)
- [Gestion des utilisateurs](#gestion-des-utilisateurs)
- [Plantes](#plantes)
- [Sols](#sols)
- [Relations Plantes-Sols](#relations-plantes-sols)

---

## Authentification

### Inscription d'un utilisateur
**POST** `/users/register/`

**Description :** Crée un nouveau compte utilisateur

**Corps de la requête :**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "motdepasse123",
    "password2": "motdepasse123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+33123456789",
    "date_of_birth": "1990-01-01"
}
```

**Réponse (201 Created) :**
```json
{
    "message": "Utilisateur créé avec succès",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+33123456789",
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

### Connexion utilisateur
**POST** `/users/login/`

**Description :** Authentifie un utilisateur et retourne les tokens JWT

**Corps de la requête :**
```json
{
    "email": "john@example.com",
    "password": "motdepasse123"
}
```

**Réponse (200 OK) :**
```json
{
    "message": "Connexion réussie",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+33123456789",
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

### Déconnexion
**POST** `/users/logout/`

**Description :** Déconnecte l'utilisateur en invalidant le token de rafraîchissement

**Headers requis :**
```
Authorization: Bearer <access_token>
```

**Corps de la requête :**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Réponse (200 OK) :**
```json
{
    "message": "Déconnexion réussie"
}
```

### Rafraîchissement du token
**POST** `/users/token/refresh/`

**Description :** Génère un nouveau token d'accès à partir du token de rafraîchissement

**Corps de la requête :**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Réponse (200 OK) :**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## Gestion des utilisateurs

### Profil utilisateur
**GET** `/users/profile/`

**Description :** Récupère le profil de l'utilisateur connecté

**Headers requis :**
```
Authorization: Bearer <access_token>
```

**Réponse (200 OK) :**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+33123456789",
    "date_of_birth": "1990-01-01",
    "is_verified": false,
    "created_at": "2024-01-01T12:00:00Z"
}
```

**PUT** `/users/profile/`

**Description :** Met à jour le profil de l'utilisateur connecté

**Headers requis :**
```
Authorization: Bearer <access_token>
```

**Corps de la requête :**
```json
{
    "first_name": "John",
    "last_name": "Smith",
    "phone_number": "+33987654321"
}
```

### Informations utilisateur
**GET** `/users/user-info/`

**Description :** Récupère les informations de l'utilisateur connecté

**Headers requis :**
```
Authorization: Bearer <access_token>
```

**Réponse (200 OK) :**
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+33123456789",
    "date_of_birth": "1990-01-01",
    "is_verified": false,
    "created_at": "2024-01-01T12:00:00Z"
}
```

### Demande de réinitialisation de mot de passe
**POST** `/users/password/reset/`

**Description :** Envoie un email de réinitialisation de mot de passe

**Corps de la requête :**
```json
{
    "email": "john@example.com"
}
```

**Réponse (200 OK) :**
```json
{
    "message": "Un email de réinitialisation a été envoyé à votre adresse email."
}
```

### Confirmation de réinitialisation de mot de passe
**POST** `/users/password/reset/confirm/`

**Description :** Confirme la réinitialisation du mot de passe avec le token reçu

**Corps de la requête :**
```json
{
    "token": "abc123def456...",
    "new_password": "nouveaumotdepasse123",
    "new_password2": "nouveaumotdepasse123"
}
```

**Réponse (200 OK) :**
```json
{
    "message": "Mot de passe mis à jour avec succès."
}
```

### Changement de mot de passe
**POST** `/users/password/change/`

**Description :** Change le mot de passe de l'utilisateur connecté

**Headers requis :**
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

**Réponse (200 OK) :**
```json
{
    "message": "Mot de passe modifié avec succès."
}
```

---

## Plantes

### Liste des plantes
**GET** `/api/plants/`

**Description :** Récupère la liste de toutes les plantes avec un aperçu des sols compatibles

**Réponse (200 OK) :**
```json
[
    {
        "id": 1,
        "name": "Tomate",
        "image": "/media/image/plant/tomate.jpg",
        "description": "Plante annuelle de la famille des Solanacées",
        "soils_count": 3
    },
    {
        "id": 2,
        "name": "Carotte",
        "image": "/media/image/plant/carotte.jpg",
        "description": "Légume racine de la famille des Apiacées",
        "soils_count": 2
    }
]
```

### Détails d'une plante
**GET** `/api/plants/{id}/`

**Description :** Récupère les détails complets d'une plante spécifique

**Paramètres :**
- `id` (integer) : ID de la plante

**Réponse (200 OK) :**
```json
{
    "id": 1,
    "name": "Tomate",
    "image": "/media/image/plant/tomate.jpg",
    "description": "Plante annuelle de la famille des Solanacées, cultivée pour ses fruits comestibles. Elle nécessite un sol bien drainé et riche en matière organique."
}
```

---

## Sols

### Liste des sols
**GET** `/api/soils/`

**Description :** Récupère la liste de tous les sols avec un aperçu des plantes cultivables

**Réponse (200 OK) :**
```json
[
    {
        "id": 1,
        "name": "Terreau universel",
        "image": "/media/image/soil/terreau.jpg",
        "description": "Mélange équilibré pour la plupart des plantes",
        "plants_count": 5
    },
    {
        "id": 2,
        "name": "Terre de bruyère",
        "image": "/media/image/soil/bruyere.jpg",
        "description": "Sol acide pour plantes acidophiles",
        "plants_count": 3
    }
]
```

### Détails d'un sol
**GET** `/api/soils/{id}/`

**Description :** Récupère les détails complets d'un sol spécifique avec toutes les plantes cultivables

**Paramètres :**
- `id` (integer) : ID du sol

**Réponse (200 OK) :**
```json
{
    "id": 1,
    "name": "Terreau universel",
    "image": "/media/image/soil/terreau.jpg",
    "description": "Mélange équilibré composé de tourbe, de compost et de sable. Idéal pour la plupart des plantes d'intérieur et de jardin.",
    "plants": [
        {
            "id": 1,
            "name": "Tomate",
            "image": "/media/image/plant/tomate.jpg",
            "description": "Plante annuelle de la famille des Solanacées"
        },
        {
            "id": 2,
            "name": "Carotte",
            "image": "/media/image/plant/carotte.jpg",
            "description": "Légume racine de la famille des Apiacées"
        }
    ]
}
```

---

## Relations Plantes-Sols

### Plantes cultivables dans un sol
**GET** `/api/soils/{soil_id}/plants/`

**Description :** Récupère toutes les plantes qui peuvent être cultivées dans un sol spécifique

**Paramètres :**
- `soil_id` (integer) : ID du sol

**Réponse (200 OK) :**
```json
{
    "soil": {
        "id": 1,
        "name": "Terreau universel"
    },
    "plants": [
        {
            "id": 1,
            "name": "Tomate",
            "image": "/media/image/plant/tomate.jpg",
            "description": "Plante annuelle de la famille des Solanacées"
        },
        {
            "id": 2,
            "name": "Carotte",
            "image": "/media/image/plant/carotte.jpg",
            "description": "Légume racine de la famille des Apiacées"
        }
    ],
    "count": 2
}
```

### Sols compatibles pour une plante
**GET** `/api/plants/{plant_id}/soils/`

**Description :** Récupère tous les sols compatibles pour cultiver une plante spécifique

**Paramètres :**
- `plant_id` (integer) : ID de la plante

**Réponse (200 OK) :**
```json
{
    "plant": {
        "id": 1,
        "name": "Tomate"
    },
    "soils": [
        {
            "id": 1,
            "name": "Terreau universel",
            "image": "/media/image/soil/terreau.jpg",
            "description": "Mélange équilibré pour la plupart des plantes",
            "plants_count": 5
        },
        {
            "id": 3,
            "name": "Terreau potager",
            "image": "/media/image/soil/potager.jpg",
            "description": "Spécialement formulé pour les légumes",
            "plants_count": 4
        }
    ],
    "count": 2
}
```

---

## Codes d'erreur

### Erreurs d'authentification
- **401 Unauthorized** : Token d'accès manquant ou invalide
- **403 Forbidden** : Permissions insuffisantes

### Erreurs de validation
- **400 Bad Request** : Données de requête invalides
- **404 Not Found** : Ressource non trouvée

### Erreurs serveur
- **500 Internal Server Error** : Erreur interne du serveur

---

## Exemples d'utilisation

### Authentification complète
```bash
# 1. Inscription
curl -X POST http://localhost:8000/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'

# 2. Connexion
curl -X POST http://localhost:8000/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# 3. Utilisation du token
curl -X GET http://localhost:8000/users/profile/ \
  -H "Authorization: Bearer <access_token>"
```

### Consultation des plantes et sols
```bash
# Liste des plantes
curl -X GET http://localhost:8000/api/plants/

# Détails d'une plante
curl -X GET http://localhost:8000/api/plants/1/

# Sols compatibles pour une plante
curl -X GET http://localhost:8000/api/plants/1/soils/

# Plantes cultivables dans un sol
curl -X GET http://localhost:8000/api/soils/1/plants/
```

---

## Notes importantes

1. **Authentification** : Les endpoints d'authentification ne nécessitent pas de token
2. **Permissions** : Les APIs de plantes et sols sont publiques (pas d'authentification requise)
3. **Images** : Les URLs des images sont relatives au domaine de l'API
4. **Pagination** : Les listes ne sont pas paginées pour le moment
5. **Filtrage** : Aucun filtre n'est disponible actuellement
6. **Tri** : Les résultats sont triés par ordre d'ID croissant 