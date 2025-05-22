#!/bin/bash
set -e

# Create iop_db database
createdb -U "$POSTGRES_USER" iop_db

# Grant privileges
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -c "
    GRANT ALL PRIVILEGES ON DATABASE iop_db TO $POSTGRES_USER;
"

# Create extensions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "iop_db" -c "
    CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";
    CREATE EXTENSION IF NOT EXISTS \"pgcrypto\";
" 