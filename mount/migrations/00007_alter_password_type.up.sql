ALTER TABLE accounts
    ALTER COLUMN password TYPE BYTEA
    USING password::bytea;