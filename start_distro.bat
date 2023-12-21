@echo off

echo Stopping the application...
docker-compose -f docker-compose.yml stop web > NUL
docker-compose -f docker-compose.yml stop rq-dashboard > NUL
docker-compose -f docker-compose.yml stop redis > NUL

echo Pulling...
git pull

echo Deleting old images...
docker image prune -a

echo Rebuilding the image...
docker-compose -f docker-compose.yml up -d --no-deps --build web > NUL
docker-compose -f docker-compose.yml up -d --no-deps --build rq-dashboard > NUL
docker-compose -f docker-compose.yml up -d --no-deps --build redis > NUL

echo Waiting 20 seconds to do the migrations...
timeout /t 20 /nobreak

docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput > NUL
echo Migrations applied.

echo Update finished, the application is running!

pause