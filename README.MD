# Machine Learning Interview Preparation Trainer

## Install
    poetry install --no-root

## Run
    poetry run streamlit run ./src/streamlit_app/main.py

## TODO
    - [X] arrumar problema com o filtro de assunto
    - criar filtro por level pq tem assuntos que só tem questoes de um level.
        - na verdade fazer o sistema verificar se a quantidade de questoes em cada nivel, se nao tiver nenhuma nem começa, se tiver apresenta só as do tipo q tem
    - fazer um split q pegue os headers do html, mas que seja de um tamanho razoalvelmente bom


## Views

CREATE VIEW get_topic_descriptions AS
SELECT DISTINCT topic_description FROM questions;
--------

-- DROP VIEW get_question_beginner;

CREATE VIEW get_question_beginner AS
SELECT q.*,
    a.id AS answer_id,
    a.created_at AS answer_created_at,
    a.correct_answer AS correct_answer
FROM (
    SELECT q.*
    FROM questions q
    LEFT JOIN question_filters qf ON q.subject_matter_1 = qf.subject_matter_1
    WHERE 
    (qf.subject_matter_1 IS NOT NULL AND qf.id IS NOT NULL) OR -- Filters present in question_filters
    (NOT EXISTS (SELECT 1 FROM question_filters) ) 
) AS q
LEFT JOIN answers AS a ON q.id = a.question_id
WHERE a.question_id IS NULL
    AND q.show_again = TRUE
    AND q.level = 'beginner'
ORDER BY RANDOM()
LIMIT 1;









-- DROP VIEW get_question_intermediate;

CREATE VIEW get_question_intermediate AS
SELECT q.*,
    a.id AS answer_id,
    a.created_at AS answer_created_at,
    a.correct_answer AS correct_answer
FROM (
    SELECT q.*
    FROM questions q
    LEFT JOIN question_filters qf ON q.subject_matter_1 = qf.subject_matter_1
    WHERE 
    (qf.subject_matter_1 IS NOT NULL AND qf.id IS NOT NULL) OR -- Filters present in question_filters
    (NOT EXISTS (SELECT 1 FROM question_filters) ) 
) AS q
LEFT JOIN answers AS a ON q.id = a.question_id
WHERE a.question_id IS NULL
    AND q.show_again = TRUE
    AND q.level = 'intermediate'
ORDER BY RANDOM()
LIMIT 1;


-- DROP VIEW get_question_hard;

CREATE VIEW get_question_hard AS
SELECT q.*,
    a.id AS answer_id,
    a.created_at AS answer_created_at,
    a.correct_answer AS correct_answer
FROM (
    SELECT q.*
    FROM questions q
    LEFT JOIN question_filters qf ON q.subject_matter_1 = qf.subject_matter_1
    WHERE 
    (qf.subject_matter_1 IS NOT NULL AND qf.id IS NOT NULL) OR -- Filters present in question_filters
    (NOT EXISTS (SELECT 1 FROM question_filters) ) 
) AS q
LEFT JOIN answers AS a ON q.id = a.question_id
WHERE a.question_id IS NULL
    AND q.show_again = TRUE
    AND q.level = 'hard'
ORDER BY RANDOM()
LIMIT 1;




-----------------------------------

-- DROP VIEW get_count_question_beginner;-- DROP VIEW get_count_question_beginner;

CREATE VIEW get_count_question_beginner AS
select count(*) from get_question_beginner



-- DROP VIEW get_count_question_intermediate;

CREATE VIEW get_count_question_intermediate AS
select count(*) from get_question_intermediate


-- DROP VIEW get_count_question_hard;
CREATE VIEW get_count_question_hard AS
select count(*) from get_question_hard