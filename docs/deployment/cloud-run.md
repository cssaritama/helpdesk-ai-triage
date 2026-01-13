# Deployment: Google Cloud Run (Backend) + Static Frontend

This guide provides a repeatable path to deploy the system. The repository also contains GitHub Actions workflows for CI and CD.

## Prerequisites
- A GCP project
- gcloud CLI installed and authenticated
- Artifact Registry enabled
- A Postgres database (recommended: managed provider such as Neon/Supabase/Cloud SQL)
- (Optional) LLM provider key for real AI mode

## Backend: Cloud Run
1. Set project
   - `gcloud config set project YOUR_PROJECT_ID`

2. Build and push image
   - `gcloud builds submit --tag REGION-docker.pkg.dev/YOUR_PROJECT_ID/helpdesk/backend:latest ./backend`

3. Deploy to Cloud Run
   - `gcloud run deploy helpdesk-backend --image REGION-docker.pkg.dev/YOUR_PROJECT_ID/helpdesk/backend:latest --region REGION --platform managed --allow-unauthenticated --set-env-vars DATABASE_URL=...,LLM_MODE=real,EMBEDDINGS_MODE=real,OPENAI_API_KEY=...`

4. Verify
   - `curl https://YOUR_CLOUD_RUN_URL/health`

## Frontend: static hosting
Options:
- Cloud Storage static site
- Vercel / Netlify
- Cloud Run (serve built assets)

Set `VITE_API_BASE_URL` to the deployed backend URL.

## Proof of deployment
After deployment, add a screenshot showing a successful request to the deployed endpoint:
- `docs/deployment/cloud-run-proof.png`

Suggested command:
- `curl https://YOUR_CLOUD_RUN_URL/health`
