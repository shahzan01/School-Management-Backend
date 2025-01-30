-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradingCounts AS (
    SELECT teacher_id, COUNT(*) AS grading_count
    FROM assignments
    WHERE grade IS NOT NULL
    GROUP BY teacher_id
    ORDER BY grading_count DESC
    LIMIT 1
)
SELECT COUNT(*) AS grade_A_count
FROM assignments
WHERE grade = 'A' 
AND teacher_id = (SELECT teacher_id FROM TeacherGradingCounts);
