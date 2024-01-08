CREATE TABLE researched_table (
    id SERIAL PRIMARY KEY NOT NULL,
    year VARCHAR(10) NOT NULL,
    month VARCHAR(10) NOT NULL,
    day VARCHAR(10) NOT NULL,
    url VARCHAR(999) NOT NULL
);

CREATE TABLE articles_table (
  id SERIAL PRIMARY KEY NOT NULL,
  author TEXT NOT NULL,
  text_article TEXT NOT NULL
);