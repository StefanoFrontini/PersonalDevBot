DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS tweets;
DROP TABLE IF EXISTS new_phrases;
DROP TABLE IF EXISTS users;

CREATE TABLE author(
            first_name VARCHAR(30) NOT NULL,
            last_name VARCHAR(30) NOT NULL,
            date_entered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            author_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE tweets(
            tweet_phrase VARCHAR(140) NOT NULL,
            tweet_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            author_id INT UNSIGNED NOT NULL,
            tweet_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE new_phrases(
            new_phrase VARCHAR(140) NOT NULL,
            new_phrase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            author_id INT UNSIGNED NOT NULL,
            new_phrase_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY);
CREATE TABLE users(
            username VARCHAR(30) NOT NULL,
            password VARCHAR(100) NOT NULL,
            date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY);
ALTER TABLE new_phrases
            DEFAULT CHARACTER SET utf8mb4,
            MODIFY new_phrase VARCHAR(280)
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;
ALTER TABLE tweets
            DEFAULT CHARACTER SET utf8mb4,
            MODIFY tweet_phrase VARCHAR(280)
            CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;