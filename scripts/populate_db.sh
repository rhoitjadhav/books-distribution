set -e

# Populate DB
docker exec -it backend python populate_db.py
