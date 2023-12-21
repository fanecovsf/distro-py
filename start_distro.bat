@echo off

set /p confirm=Do you want to delete the old version and start the application? (yes/no): 

if /i "%confirm%"=="yes" (
    echo Deleting old version...
    docker-compose down -v > NUL

    echo Starting application...
    docker-compose -f docker-compose.yml up -d --build > NUL
    echo Application started successfully.

    echo Waiting 20 seconds to do the migrations...
    timeout /t 20 /nobreak

    docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput > NUL
    echo Migrations applied.

    echo Finished, application should be running!
) else (
    echo Operation canceled.
)

pause