# Machine Learning Interview Preparation Trainer

## TODO
    - [X] arrumar problema com o filtro de assunto
    - fazer um split q pegue os headers do html, mas que seja de um tamanho razoalvelmente bom


## Views

CREATE VIEW get_topic_descriptions AS
SELECT DISTINCT topic_description FROM questions;


CREATE VIEW get_subject_matter_1s AS
SELECT DISTINCT subject_matter_1 FROM questions;

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
    WHERE qf.subject_matter_1 IS NOT NULL 
    AND q.level = 'beginner'
) AS q
LEFT JOIN answers AS a ON q.id = a.question_id
WHERE a.question_id IS NULL
    AND q.show_again = TRUE
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
    WHERE qf.subject_matter_1 IS NOT NULL 
    AND q.level = 'intermediate'
) AS q
LEFT JOIN answers AS a ON q.id = a.question_id
WHERE a.question_id IS NULL
    AND q.show_again = TRUE
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
    WHERE qf.subject_matter_1 IS NOT NULL 
    AND q.level = 'hard'
) AS q
LEFT JOIN answers AS a ON q.id = a.question_id
WHERE a.question_id IS NULL
    AND q.show_again = TRUE
ORDER BY RANDOM()
LIMIT 1;
