SELECT
    a.artist_name,
    s.start_time
FROM grooveapi_artist a 
JOIN grooveapi_show s ON a.id = s.artist_id
WHERE s.date BETWEEN '2022-10-21' AND '2022-10-22'
WHERE s.start_time ON '2022-10-22' < '11:00:00'