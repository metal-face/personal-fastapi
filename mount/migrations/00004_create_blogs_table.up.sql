CREATE TABLE blogs (
    rec_id SERIAL NOT NULL PRIMARY KEY,
    blog_id UUID NOT NULL UNIQUE,
    blog_post TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NOT NULL FOREIGN KEY
        REFERENCES accounts (account_id)
);