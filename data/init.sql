CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE topics (
    id bigserial PRIMARY KEY,  
    -- 768 dimensions pour correspondre au modèle Ollama "nomic-embed-text"
    embedding VECTOR(768), 
    title TEXT,
    subtitle TEXT,
    content TEXT,
    url TEXT UNIQUE
);

CREATE INDEX idx_topics_embedding ON topics USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
