# Deployment Guide for Fly.io

## Prerequisites

1. Install Fly.io CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Login to Fly.io: `fly auth login`
3. Ensure you're in the project root directory

## Initial Setup (First Time Only)

### 1. Launch the application

```bash
fly launch
```

When prompted:
- Choose app name: `wingz-ride-management` (or your preferred name)
- Choose region: `sjc` (or your preferred region)
- **Do NOT deploy yet** - choose "No" when asked to deploy
- **Create PostgreSQL database**: Choose "Yes"
  - Select development configuration or production as needed
  - Note the database connection string

### 2. Set environment secrets

```bash
# Generate a secure secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Set the secret key
fly secrets set SECRET_KEY="your-generated-secret-key-here"
```

### 3. Update fly.toml

If `fly launch` created or modified `fly.toml`, make sure it matches the configuration we created. The key settings are:
- `dockerfile = 'Dockerfile.production'`
- `DJANGO_SETTINGS_MODULE = 'config.settings_production'`
- App name should match what you chose

### 4. Deploy the application

```bash
fly deploy --dockerfile Dockerfile.production
```

This will:
- Build the Docker image (Vue.js + Django)
- Run database migrations
- Deploy to Fly.io

### 5. Open your application

```bash
fly open
```

## Subsequent Deployments

For future deployments after making changes:

```bash
fly deploy --dockerfile Dockerfile.production
```

## Useful Commands

### View logs
```bash
fly logs
```

### SSH into the container
```bash
fly ssh console
```

### Check app status
```bash
fly status
```

### Scale the application
```bash
# Increase memory
fly scale memory 1024

# Add more machines
fly scale count 2
```

### Database commands

```bash
# Connect to PostgreSQL
fly postgres connect -a <your-db-app-name>

# View database info
fly postgres db list -a <your-db-app-name>
```

### Restart the application
```bash
fly apps restart wingz-ride-management
```

## Troubleshooting

### Build fails
- Check that all dependencies are in `requirements/base.txt`
- Verify Docker build locally: `docker build -f Dockerfile.production -t test-build .`

### Database connection issues
- Verify DATABASE_URL is set: `fly secrets list`
- Check database app is running: `fly status -a <your-db-app-name>`

### Static files not loading
- Ensure collectstatic ran during build
- Check STATIC_ROOT and STATICFILES_DIRS in settings_production.py
- Verify whitenoise is in MIDDLEWARE

### API endpoints not working
- Check logs: `fly logs`
- Verify ALLOWED_HOSTS includes your app URL
- Check CORS and CSRF settings

### Frontend routes return 404
- Ensure the catch-all route is configured in config/urls.py
- Check that Vue.js build output is in frontend/dist/

## Environment Variables

Set additional environment variables as needed:

```bash
fly secrets set CUSTOM_DOMAIN="yourdomain.com"
```

## Custom Domain Setup

1. Add your custom domain to Fly.io:
```bash
fly certs add yourdomain.com
```

2. Update ALLOWED_HOSTS in settings_production.py (already configured to read from CUSTOM_DOMAIN env var)

3. Point your domain's DNS to Fly.io (follow their instructions)

## Database Backups

Fly.io PostgreSQL has automated backups. To create a manual backup:

```bash
fly postgres backup create -a <your-db-app-name>
```

## Monitoring

View metrics in the Fly.io dashboard:
```bash
fly dashboard
```

## Cost Optimization

- Use `auto_stop_machines` and `auto_start_machines` to reduce costs when idle
- Start with shared-cpu-1x and 512MB RAM
- Scale up only if needed

---

## Quick Reference

```bash
# Deploy
fly deploy --dockerfile Dockerfile.production

# View logs
fly logs

# SSH
fly ssh console

# Restart
fly apps restart

# Status
fly status
```
