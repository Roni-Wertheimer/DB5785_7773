CREATE VIEW Housekeeping_Tasks_Details AS
SELECT 
    hk.TaskID,
    hk.TaskDate,
    hk.Status AS TaskStatus,
    r.RoomNumber,
    r.Floor,
    s.FirstName || ' ' || s.LastName AS StaffName,
    s.Role,
    s.IsActive
FROM Housekeeping hk
JOIN Room r ON hk.RoomId = r.RoomId
JOIN AssignKeepingStaff aks ON hk.TaskID = aks.TaskID
JOIN Staff s ON aks.StaffId = s.StaffId;

SELECT TaskID, TaskDate, RoomNumber, Floor, StaffName
FROM Housekeeping_Tasks_Details
WHERE TaskStatus <> 'Completed'
ORDER BY TaskDate DESC;

SELECT StaffName, COUNT(*) AS TaskCount
FROM Housekeeping_Tasks_Details
WHERE IsActive = TRUE
GROUP BY StaffName
ORDER BY TaskCount DESC;

---------------------------------
CREATE VIEW Reservation_With_Guest_And_Room AS
SELECT 
    rv.reservation_id,
    g.full_name AS GuestName,
    g.email,
    rv.start_date,
    rv.end_date,
    rv.status AS ReservationStatus,
    r.RoomNumber,
    r.Floor,
    r.AvailabilityStatus,
    r.CleaningStatus
FROM Reservations rv
JOIN Guests g ON rv.guest_id = g.guest_id
JOIN Room r ON rv.roomId = r.RoomId;

SELECT ReservationStatus, COUNT(*) AS Total
FROM Reservation_With_Guest_And_Room
GROUP BY ReservationStatus;

SELECT 
    GuestName,
    RoomNumber,
    start_date,
    end_date,
    AvailabilityStatus,
    CleaningStatus
FROM Reservation_With_Guest_And_Room
WHERE start_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
ORDER BY start_date;
