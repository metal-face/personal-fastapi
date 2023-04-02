CREATE TABLE accounts(
    rec_id SERIAL NOT NULL PRIMARY KEY,
    account_id UUID NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX accounts_username ON accounts (username);
CREATE INDEX account_email on accounts (email);
