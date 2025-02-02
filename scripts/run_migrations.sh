set -e

# Upgrade DB
docker exec -it backend alembic upgrade head
