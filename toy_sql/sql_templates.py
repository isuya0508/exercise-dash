german_lines = [
    'SELECT c.name, l.name AS langauge, c.population',
    'FROM country c JOIN language l',
    '    ON c.language_id = l.id',
    '    AND l.name = "German"',
    'ORDER BY c.population DESC',
]

count_by_religion_lines = [
    'SELECT r.name, COUNT(c.name) AS count',
    'FROM country c JOIN religion r ',
    '    ON c.religion_id = r.id',
    'GROUP BY r.name'
]

contain_j_lines = [
    'SELECT name, area, population',
    'FROM country',
    'WHERE name LIKE "%j%"'
]
