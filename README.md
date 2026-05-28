# RAPH BRAIN Mobile

PWA iPhone — générateur de contenu LinkedIn.

## Déploiement GitHub Pages

### 1. Générer les icônes (une seule fois)

```bash
cd raph-brain-mobile
python3 create_icons.py
```

### 2. Créer le repo GitHub

```bash
cd raph-brain-mobile
git init
git add .
git commit -m "init: RAPH BRAIN Mobile PWA"
gh repo create raph-brain-mobile --public --source=. --push
```

### 3. Activer GitHub Pages

```
GitHub → repo → Settings → Pages
Source : Deploy from a branch
Branch : main / (root)
```

L'app sera dispo sur : `https://<username>.github.io/raph-brain-mobile/`

---

## Installation sur iPhone

1. Ouvrir l'URL dans **Safari**
2. Partager → **Sur l'écran d'accueil**
3. L'app se lance en mode standalone (plein écran, sans barre Safari)

## Fonctionnalités

| Tab | Feature |
|-----|---------|
| ⚡ Générer | Un post via `POST /linkedin/generate` |
| 📋 Batch | 5/10/20 posts via `POST /linkedin/generate/batch` |
| ▦ Bibliothèque | `GET /linkedin` avec filtres draft/publié/planifié |

## Mise à jour du cache PWA

Incrémenter la version dans `sw.js` :

```js
const CACHE = 'raph-brain-v2'; // ← bump
```
