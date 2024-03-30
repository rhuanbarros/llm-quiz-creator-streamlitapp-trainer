# Machine Learning Interview Preparation Trainer


# Views

-- DROP VIEW get_question;

CREATE VIEW get_question AS
SELECT q.*
FROM questions AS q
LEFT JOIN answers AS a ON q.id = a.question_id
-- WHERE a.question_id IS NULL
--   AND q.show_again = TRUE
-- LIMIT 1;


CREATE VIEW get_topic_descriptions AS
SELECT DISTINCT topic_description FROM questions;



CREATE VIEW get_subject_matter_1s AS
SELECT DISTINCT subject_matter_1 FROM questions;
