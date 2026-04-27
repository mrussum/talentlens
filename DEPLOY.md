# Deploying TalentLens — Fly.io (backend) + Vercel (frontend)

This walks you through a production deploy. ~15 minutes if you already have Fly + Vercel accounts.

## Prerequisites

- A [Fly.io](https://fly.io) account and the `flyctl` CLI installed
  (Windows: `iwr https://fly.io/install.ps1 -useb | iex`)
- A [Vercel](https://vercel.com) account (free tier is fine)
- An Anthropic API key with billing set up

## 1. Deploy the backend to Fly

From the repo root:

```bash
cd backend
fly auth login
```

The repo ships a ready-made `fly.toml` set up for app name `talentlens-api` in
region `lhr`. If that name is taken, edit the `app =` line at the top of
`backend/fly.toml` first (or run `fly launch --no-deploy` to do it
interactively — say "no" when it asks to overwrite the existing fly.toml, or
"yes" and then re-edit).

Create the app (one-off):

```bash
fly apps create talentlens-api   # skip if you used `fly launch`
```

Set your secrets (NOT in `fly.toml`):

```bash
fly secrets set ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
# CORS — set to a placeholder for now; we'll update once we have the Vercel URL
fly secrets set CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Deploy:

```bash
fly deploy
```

After a couple of minutes you should be able to hit:

```bash
curl https://talentlens-api.fly.dev/api/health
# -> {"status":"ok","version":"1.0.0"}
```

Keep this URL handy — you'll need it for Vercel.

## 2. Deploy the frontend to Vercel

You can do this from the dashboard or CLI. Dashboard is simpler the first time.

### Dashboard

1. Go to <https://vercel.com/new> and import the GitHub repo.
2. **Root directory** — set this to `frontend`. This is the most common
   mistake; Vercel needs to know the React app lives in a subdirectory.
3. **Framework preset** — Vite should be auto-detected (the `vercel.json` in
   `frontend/` confirms this).
4. **Build command / output directory** — leave defaults (already set in
   `vercel.json`: `npm run build`, `dist`).
5. **Environment variables** — add one:
   - Name: `VITE_API_BASE`
   - Value: `https://talentlens-api.fly.dev/api` (replace with your Fly URL)
   - Apply to: Production + Preview + Development
6. Click **Deploy**.

### CLI alternative

```bash
cd frontend
npx vercel
# Set the root directory to the current dir when prompted
npx vercel env add VITE_API_BASE   # paste the Fly URL when prompted
npx vercel --prod
```

You'll get a URL like `https://talentlens-mrussum.vercel.app`.

## 3. Wire CORS — point Fly at the Vercel URL

Now that you know the Vercel domain, tell the backend to trust it:

```bash
fly secrets set CORS_ALLOWED_ORIGINS=https://talentlens-mrussum.vercel.app,http://localhost:5173 -a talentlens-api
```

Setting a secret triggers a redeploy automatically.

If you use Vercel preview deployments (each PR gets its own URL like
`talentlens-git-feature-x-mrussum.vercel.app`), either:
- add each preview URL to the secret, or
- temporarily allow `https://*.vercel.app` (less safe — only do this if it's a
  private or unimportant project).

## 4. Smoke-test end to end

1. Open your Vercel URL.
2. Click "Senior Product Manager" under Quick-start scenarios.
3. Click "Generate Report".
4. You should get a structured report back in 3–5 seconds.

If you get a CORS error in the browser console, double-check step 3.
If you get a 500 from `/api/generate`, check `fly logs -a talentlens-api`
— most often it's a missing or invalid `ANTHROPIC_API_KEY`.

## Updating

- **Backend changes** → `cd backend && fly deploy`
- **Frontend changes** → `git push` (Vercel auto-deploys on push to main)

## Costs (rough order of magnitude)

- Fly: free allowance covers a `shared-cpu-1x` 512mb machine that
  auto-stops when idle. Realistic cost for low-volume use: $0–5/month.
- Vercel: free Hobby plan handles this easily.
- Anthropic: pay-per-token. A typical TalentLens report uses ~3-4k input +
  1-2k output tokens, so roughly $0.02-0.04 per report at current
  Sonnet 4 pricing.
