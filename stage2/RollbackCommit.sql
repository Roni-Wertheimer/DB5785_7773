--ROLLBACK
BEGIN;

UPDATE Room
SET CleaningStatus = 'Under Inspection'
WHERE RoomId IN (
    SELECT RoomId
    FROM Housekeeping
    WHERE TaskDate = CURRENT_DATE
);

SELECT RoomNumber, CleaningStatus
FROM Room
WHERE CleaningStatus = 'Under Inspection';

ROLLBACK;

SELECT RoomNumber, CleaningStatus
FROM Room
WHERE CleaningStatus = 'Under Inspection';

--COMMIT
BEGIN;

UPDATE Room
SET AvailabilityStatus = 'Reserved'
WHERE RoomId IN (
    SELECT RoomId
    FROM MaintenanceRequest
    WHERE Status = 'Pending'
);

SELECT RoomNumber, AvailabilityStatus
FROM Room
WHERE AvailabilityStatus = 'Reserved';

COMMIT;

SELECT RoomNumber, AvailabilityStatus
FROM Room
WHERE AvailabilityStatus = 'Reserved';

