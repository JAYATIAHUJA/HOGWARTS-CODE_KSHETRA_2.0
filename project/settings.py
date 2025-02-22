INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # your core app
    'events',  # your events app
    'artisans.apps.ArtisansConfig',  # Update this line
    # ... your other apps ...
] 