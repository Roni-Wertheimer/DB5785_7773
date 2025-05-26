INSERT INTO Room (RoomId, RoomNumber, PricePerNight, AvailabilityStatus, CleaningStatus, Floor, RoomTypeId)
SELECT 
    room_id,
    room_number::INTEGER,
    round((random() * (800 - 200) + 200)::numeric, 2) AS PricePerNight,
    (ARRAY['Available', 'Occupied', 'Maintenance'])[floor(random() * 3 + 1)] AS AvailabilityStatus,
    (ARRAY['Clean', 'Dirty', 'In Progress'])[floor(random() * 3 + 1)] AS CleaningStatus,
    floor,
    (
        SELECT RoomTypeId
        FROM RoomType
        ORDER BY random()
        LIMIT 1
    ) AS RoomTypeId
FROM  external_rooms
WHERE room_id NOT IN (SELECT RoomId FROM Room);

ALTER TABLE reservation
RENAME COLUMN room_id TO roomid;
