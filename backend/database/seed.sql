INSERT INTO users (full_name, email, password_hash, role, status) VALUES
    ('Admin User', 'admin@pentecostchurch.org', '$2b$12$T.Yzp.wIMRRuvkdAmXtHPOMBMXGNL1UdEyPjqYXffA3jJrzd.i5jS', 'admin', 'active'),
    ('Grace Thompson', 'grace@example.com', '$2b$12$0DMsvd.kVumQFap9R.aE0eoWaYvkGuw/rTEtcpAvu5On4PdLrpWCy', 'member', 'active'),
    ('Pastor David', 'pastor@example.com', '$2b$12$0DMsvd.kVumQFap9R.aE0eoWaYvkGuw/rTEtcpAvu5On4PdLrpWCy', 'pastor', 'active');

INSERT INTO members (user_id, phone, address, birthday, member_number, join_date, ministry) VALUES
    (2, '+233 24 000 0000', 'Accra, Ghana', '1995-06-15', 'PCM-001', '2020-01-10', 'Women Ministry'),
    (3, '+233 24 111 1111', 'Tema, Ghana', '1985-08-22', 'PCP-001', '2015-03-05', 'Leadership');

INSERT INTO pastors (name, title, bio, email, phone) VALUES
    ('Pastor David Mensah', 'Senior Pastor', 'Pastor David leads the church with a heart for worship, discipleship, and community outreach.', 'pastor@example.com', '+233 24 111 1111');

INSERT INTO ministries (name, tagline, description, details, image_url) VALUES
    ('Youth Ministry', 'Raising the next generation in faith.', 'The Youth Ministry helps young people grow spiritually, socially, and academically.', 'Weekly youth meetings, mentorship, and outreach programs.', 'pic/Praise-and-Worship-58b5c8ba5f9b586046caf1fa.jpg'),
    ('Women Ministry', 'Empowering women in faith and service.', 'The Women Ministry supports women with prayer, discipleship, and care.', 'Monthly prayer meetings and support groups.', 'pic/terren-hurst-KU66acygwIY-unsplash-1-scaled.webp');

INSERT INTO services (name, service_day, service_time, description, location) VALUES
    ('Sunday Worship', 'Sunday', '8:00 AM', 'A joyful worship service with praise, preaching, and prayer.', 'Main Auditorium'),
    ('Midweek Prayer', 'Wednesday', '6:00 PM', 'A gathering of prayer, testimony, and Bible study.', 'Prayer Hall');

INSERT INTO sermons (title, preacher, sermon_date, bible_scripture, description, category, notes) VALUES
    ('Walking by Faith', 'Pastor David Mensah', '2026-09-12', '2 Corinthians 5:7', 'A sermon on trusting God even when the path is unclear.', 'Faith', 'Outline and prayer points included.'),
    ('Power in Prayer', 'Pastor David Mensah', '2026-09-05', 'James 5:16', 'A practical teaching on persistent and effective prayer.', 'Prayer', 'Includes prayer notes and reflection questions.');

INSERT INTO events (title, description, event_date, event_time, location, category) VALUES
    ('Sunday Worship', 'A time of praise, prayer, and preaching.', '2026-09-20', '8:00 AM', 'Main Auditorium', 'Worship'),
    ('Prayer Meeting', 'Midweek prayer gathering for the church family.', '2026-09-23', '6:00 PM', 'Prayer Hall', 'Prayer');

INSERT INTO bible_verses (verse_text, reference, theme, verse_date) VALUES
    ('The Lord is my shepherd; I shall not want.', 'Psalm 23:1', 'Trust', '2026-09-14'),
    ('Be strong and courageous. Do not be afraid; do not be discouraged.', 'Joshua 1:9', 'Courage', '2026-09-13');

INSERT INTO daily_quotes (quote_text, author, quote_date, category, status) VALUES
    ('Faith moves mountains.', 'Pastor David Mensah', '2026-09-14', 'Faith', 'published'),
    ('Prayer is the bridge between panic and peace.', 'Grace Thompson', '2026-09-13', 'Prayer', 'published');

INSERT INTO prayer_requests (full_name, email, phone, category, prayer_message, is_private, status) VALUES
    ('Grace Thompson', 'grace@example.com', '+233 24 000 0000', 'Family', 'Please pray for my family and work guidance.', 0, 'pending'),
    ('Anonymous Member', 'anonymous@example.com', '+233 24 111 1111', 'Health', 'Please pray for healing and strength.', 1, 'approved');

INSERT INTO offerings (offering_type, amount, donor_name, email, payment_method, description, status) VALUES
    ('Tithe', 200.00, 'Grace Thompson', 'grace@example.com', 'Mobile Money', 'Monthly tithe offering.', 'completed'),
    ('General Offering', 120.00, 'Anonymous Member', 'anonymous@example.com', 'Bank Transfer', 'General church support.', 'completed');

INSERT INTO announcements (title, content, publish_date, status) VALUES
    ('Midweek Prayer Service', 'Join us for a powerful evening of prayer and worship this Wednesday.', '2026-09-16', 'published'),
    ('Mission Outreach', 'We are preparing for a community outreach and prayer walk this weekend.', '2026-09-18', 'published');

INSERT INTO gallery (title, image_url, description, category) VALUES
    ('Sunday Worship', 'pic/serene-church-service-stockcake.jpg', 'A joyful Sunday worship gathering.', 'Worship'),
    ('Youth Event', 'pic/Praise-and-Worship-58b5c8ba5f9b586046caf1fa.jpg', 'Youth ministry fellowship event.', 'Ministry');

INSERT INTO contacts (name, phone, email, address, opening_hours, sunday_service_times, map_url, message) VALUES
    ('Pentecost Church', '+233 24 555 1234', 'hello@pentecostchurch.org', '123 Church Road, Accra, Ghana', 'Mon-Sat: 8:00 AM - 5:00 PM', 'Sunday: 8:00 AM, 10:00 AM, 6:00 PM', 'https://maps.google.com', 'We are happy to connect with you.');

INSERT INTO notifications (user_id, title, message, type) VALUES
    (2, 'Welcome', 'Welcome to the Pentecost Church member portal.', 'welcome'),
    (2, 'Prayer Reminder', 'Your prayer request is being reviewed by the church team.', 'prayer');
