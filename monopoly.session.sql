ALTER TABLE games ADD COLUMN current_turn INTEGER DEFAULT 0;


-- ALTER TABLE players ADD COLUMN is_active BOOLEAN DEFAULT true;


-- INSERT INTO board (position, name, type) VALUES
--   (0, 'Go', 'go'),
--   (1, 'Mediterranean Avenue', 'property'),
--   (2, 'Community Chest', 'community_chest'),
--   (3, 'Baltic Avenue', 'property'),
--   (4, 'Income Tax', 'tax'),
--   (5, 'Reading Railroad', 'railroad'),
--   (6, 'Oriental Avenue', 'property'),
--   (7, 'Chance', 'chance'),
--   (8, 'Vermont Avenue', 'property'),
--   (9, 'Connecticut Avenue', 'property'),
--   (10, 'Jail / Just Visiting', 'jail'),
--   (11, 'St. Charles Place', 'property'),
--   (12, 'Electric Company', 'utility'),
--   (13, 'States Avenue', 'property'),
--   (14, 'Virginia Avenue', 'property'),
--   (15, 'Pennsylvania Railroad', 'railroad'),
--   (16, 'St. James Place', 'property'),
--   (17, 'Community Chest', 'community_chest'),
--   (18, 'Tennessee Avenue', 'property'),
--   (19, 'New York Avenue', 'property'),
--   (20, 'Free Parking', 'free_parking'),
--   (21, 'Kentucky Avenue', 'property'),
--   (22, 'Chance', 'chance'),
--   (23, 'Indiana Avenue', 'property'),
--   (24, 'Illinois Avenue', 'property'),
--   (25, 'B&O Railroad', 'railroad'),
--   (26, 'Atlantic Avenue', 'property'),
--   (27, 'Ventnor Avenue', 'property'),
--   (28, 'Water Works', 'utility'),
--   (29, 'Marvin Gardens', 'property'),
--   (30, 'Go To Jail', 'go_to_jail'),
--   (31, 'Pacific Avenue', 'property'),
--   (32, 'North Carolina Avenue', 'property'),
--   (33, 'Community Chest', 'community_chest'),
--   (34, 'Pennsylvania Avenue', 'property'),
--   (35, 'Short Line', 'railroad'),
--   (36, 'Chance', 'chance'),
--   (37, 'Park Place', 'property'),
--   (38, 'Luxury Tax', 'tax'),
--   (39, 'Boardwalk', 'property');



-- INSERT INTO community_chest_cards (description) VALUES
--   ('Advance to Go (Collect $200)'),
--   ('Bank error in your favor. Collect $200'),
--   ('Doctors fees. Pay $50'),
--   ('From sale of stock you get $50'),
--   ('Get Out of Jail Free. This card may be kept until needed or sold'),
--   ('Go to Jail. Go directly to Jail, do not pass Go, do not collect $200'),
--   ('Grand Opera Night. Collect $50 from every player for opening night seats'),
--   ('Holiday Fund matures. Receive $100'),
--   ('Income tax refund. Collect $20'),
--   ('It is your birthday. Collect $10 from every player'),
--   ('Life insurance matures. Collect $100'),
--   ('Hospital Fees. Pay $100'),
--   ('School fees. Pay $50'),
--   ('Receive $25 consultancy fee'),
--   ('You are assessed for street repairs: Pay $40 per house and $115 per hotel'),
--   ('You have won second prize in a beauty contest. Collect $10'),
--   ('You inherit $100');










-- INSERT INTO properties (name, price, position, owner_id, rent)
-- VALUES
-- -- Brown
-- ('Mediterranean Avenue', 60, 1, NULL, 2),
-- ('Baltic Avenue', 60, 3, NULL, 4),

-- -- Light Blue
-- ('Oriental Avenue', 100, 6, NULL, 6),
-- ('Vermont Avenue', 100, 8, NULL, 6),
-- ('Connecticut Avenue', 120, 9, NULL, 8),

-- -- Pink
-- ('St. Charles Place', 140, 11, NULL, 10),
-- ('States Avenue', 140, 13, NULL, 10),
-- ('Virginia Avenue', 160, 14, NULL, 12),

-- -- Orange
-- ('St. James Place', 180, 16, NULL, 14),
-- ('Tennessee Avenue', 180, 18, NULL, 14),
-- ('New York Avenue', 200, 19, NULL, 16),

-- -- Red
-- ('Kentucky Avenue', 220, 21, NULL, 18),
-- ('Indiana Avenue', 220, 23, NULL, 18),
-- ('Illinois Avenue', 240, 24, NULL, 20),

-- -- Yellow
-- ('Atlantic Avenue', 260, 26, NULL, 22),
-- ('Ventnor Avenue', 260, 27, NULL, 22),
-- ('Marvin Gardens', 280, 29, NULL, 24),

-- -- Green
-- ('Pacific Avenue', 300, 31, NULL, 26),
-- ('North Carolina Avenue', 300, 32, NULL, 26),
-- ('Pennsylvania Avenue', 320, 34, NULL, 28),

-- -- Dark Blue
-- ('Park Place', 350, 37, NULL, 35),
-- ('Boardwalk', 400, 39, NULL, 50),

-- -- Railroads
-- ('Reading Railroad', 200, 5, NULL, 25),
-- ('Pennsylvania Railroad', 200, 15, NULL, 25),
-- ('B&O Railroad', 200, 25, NULL, 25),
-- ('Short Line', 200, 35, NULL, 25),

-- -- Utilities
-- ('Electric Company', 150, 12, NULL, 4),
-- ('Water Works', 150, 28, NULL, 4);

-- INSERT INTO chance_cards (description) VALUES
--   ('Advance to Go (Collect $200)'),
--   ('Advance to Illinois Avenue'),
--   ('Advance to St. Charles Place'),
--   ('Advance token to nearest Utility. If unowned, you may buy it.'),
--   ('Advance token to the nearest Railroad and pay owner twice the rental to which they are otherwise entitled.'),
--   ('Bank pays you dividend of $50'),
--   ('Get Out of Jail Free. This card may be kept until needed or sold.'),
--   ('Go Back 3 Spaces'),
--   ('Go to Jail. Go directly to Jail, do not pass Go, do not collect $200'),
--   ('Make general repairs on all your property: For each house pay $25, For each hotel pay $100'),
--   ('Pay poor tax of $15'),
--   ('Take a trip to Reading Railroad. If you pass Go, collect $200'),
--   ('Take a walk on the Boardwalk. Advance token to Boardwalk.'),
--   ('You have been elected Chairman of the Board. Pay each player $50'),
--   ('Your building loan matures. Collect $150'),
--   ('You have won a crossword competition. Collect $100');