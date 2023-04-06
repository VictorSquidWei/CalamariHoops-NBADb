-- Testing for setting the start year of undrafted players
-- SELECT distinct p.PERSON_ID, p.DISPLAY_FIRST_LAST, p.DRAFT_YEAR, SUBSTRING(b.season, 1, 4) as START_YEAR FROM players as p
-- INNER JOIN basic_stats as b on b.PLAYER_ID = p.PERSON_ID
-- WHERE p.DRAFT_YEAR = 'Undrafted';
-- 


-- Setting the start year of undrafted players
-- update 
--     players
-- set 
--     DRAFT_YEAR = 
--     (select SUBSTRING(basic_stats.SEASON, 1, 4) from basic_stats where basic_stats.PLAYER_ID = players.PERSON_ID)
-- WHERE players.DRAFT_YEAR = 'Undrafted';


-- Updating the players who have missing HEIGHT and WEIGHT columns
-- UPDATE players
-- set HEIGHT = 'N/A'
-- WHERE
--     HEIGHT = '';
--     
-- UPDATE players
-- SET WEIGHT = 'N/A'
-- where
--     WEIGHT = '';


-- Testing for updating the CAREER_YEAR column to include the years the players played in the league
-- SELECT CAST(SUBSTRING(season, 1, 4) as INT), p.DRAFT_YEAR, (CAST(SUBSTRING(season, 1, 4) as INT) - CAST(p.DRAFT_YEAR as INT) + 1) as CAREER
-- FROM adv_stats as a
-- INNER JOIN players as p on a.PLAYER_ID = p.PERSON_ID;


-- Adding the CAREER_YEAR column to adv and basic stats table
-- alter table adv_stats add CAREER_YEAR INT;
-- alter table basic_stats add CAREER_YEAR INT;


-- Updates the CAREER_YEAR column of adv_stats and basic_stats table to include the years a player as played in the league for that specific season
-- UPDATE adv_stats
-- SET CAREER_YEAR = (SELECT (CAST(SUBSTRING(season, 1, 4) as INT) - CAST(players.DRAFT_YEAR as INT) + 1) from players
--                     where adv_stats.PLAYER_ID = players.PERSON_ID);
-- UPDATE basic_stats
-- SET CAREER_YEAR = (SELECT (CAST(SUBSTRING(basic_stats.season, 1, 4) as INT) - CAST(players.DRAFT_YEAR as INT) + 1) from players
--                    where basic_stats.PLAYER_ID = players.PERSON_ID); 
                                  


