# Machine Learning Interview Preparation Trainer


# Views

CREATE VIEW get_question AS
SELECT q.*
FROM questions AS q
LEFT JOIN answers AS a ON q.id = a.question_id
WHERE a.question_id IS NULL
  AND q.show_again = TRUE
LIMIT 1;
