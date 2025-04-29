--prepering the DATABASE
UPDATE Housekeeping
SET TaskDate = TaskDate + INTERVAL '2 months';

-- AssignKeepingStaff.taskid → Housekeeping.taskid
ALTER TABLE AssignKeepingStaff
DROP CONSTRAINT assignkeepingstaff_taskid_fkey;

ALTER TABLE AssignKeepingStaff
ADD CONSTRAINT assignkeepingstaff_taskid_fkey
FOREIGN KEY (TaskID) REFERENCES Housekeeping(TaskID) ON DELETE CASCADE;

-- AssignKeepingStaff.staffid → Staff.staffid
ALTER TABLE AssignKeepingStaff
DROP CONSTRAINT assignkeepingstaff_staffid_fkey;

ALTER TABLE AssignKeepingStaff
ADD CONSTRAINT assignkeepingstaff_staffid_fkey
FOREIGN KEY (StaffId) REFERENCES Staff(StaffId) ON DELETE CASCADE;

-- AssignMaintenanceStaff.requestid → MaintenanceRequest.requestid
ALTER TABLE AssignMaintenanceStaff
DROP CONSTRAINT assignmaintenancestaff_requestid_fkey;

ALTER TABLE AssignMaintenanceStaff
ADD CONSTRAINT assignmaintenancestaff_requestid_fkey
FOREIGN KEY (RequestId) REFERENCES MaintenanceRequest(RequestId) ON DELETE CASCADE;

-- AssignMaintenanceStaff.staffid → Staff.staffid
ALTER TABLE AssignMaintenanceStaff
DROP CONSTRAINT assignmaintenancestaff_staffid_fkey;

ALTER TABLE AssignMaintenanceStaff
ADD CONSTRAINT assignmaintenancestaff_staffid_fkey
FOREIGN KEY (StaffId) REFERENCES Staff(StaffId) ON DELETE CASCADE;

-- KeepingInventory.taskid → Housekeeping.taskid
ALTER TABLE KeepingInventory
DROP CONSTRAINT keepinginventory_taskid_fkey;

ALTER TABLE KeepingInventory
ADD CONSTRAINT keepinginventory_taskid_fkey
FOREIGN KEY (TaskID) REFERENCES Housekeeping(TaskID) ON DELETE CASCADE;

-- KeepingInventory.usageid → InventoryUsage.usageid
ALTER TABLE KeepingInventory
DROP CONSTRAINT keepinginventory_usageid_fkey;

ALTER TABLE KeepingInventory
ADD CONSTRAINT keepinginventory_usageid_fkey
FOREIGN KEY (UsageId) REFERENCES InventoryUsage(UsageId) ON DELETE CASCADE;

-- MaintenanceInventory.requestid → MaintenanceRequest.requestid
ALTER TABLE MaintenanceInventory
DROP CONSTRAINT maintenanceinventory_requestid_fkey;

ALTER TABLE MaintenanceInventory
ADD CONSTRAINT maintenanceinventory_requestid_fkey
FOREIGN KEY (RequestId) REFERENCES MaintenanceRequest(RequestId) ON DELETE CASCADE;

-- MaintenanceInventory.usageid → InventoryUsage.usageid
ALTER TABLE MaintenanceInventory
DROP CONSTRAINT maintenanceinventory_usageid_fkey;

ALTER TABLE MaintenanceInventory
ADD CONSTRAINT maintenanceinventory_usageid_fkey
FOREIGN KEY (UsageId) REFERENCES InventoryUsage(UsageId) ON DELETE CASCADE;

-- Housekeeping.roomid → Room.roomid
ALTER TABLE Housekeeping
DROP CONSTRAINT housekeeping_roomid_fkey;

ALTER TABLE Housekeeping
ADD CONSTRAINT housekeeping_roomid_fkey
FOREIGN KEY (RoomId) REFERENCES Room(RoomId) ON DELETE CASCADE;

-- MaintenanceRequest.roomid → Room.roomid
ALTER TABLE MaintenanceRequest
DROP CONSTRAINT maintenancerequest_roomid_fkey;

ALTER TABLE MaintenanceRequest
ADD CONSTRAINT maintenancerequest_roomid_fkey
FOREIGN KEY (RoomId) REFERENCES Room(RoomId) ON DELETE CASCADE;

-- Room.roomtypeid → RoomType.roomtypeid
ALTER TABLE Room
DROP CONSTRAINT room_roomtypeid_fkey;

ALTER TABLE Room
ADD CONSTRAINT room_roomtypeid_fkey
FOREIGN KEY (RoomTypeId) REFERENCES RoomType(RoomTypeId) ON DELETE CASCADE;


--select queries
SELECT 
    R.RoomNumber,
    R.CleaningStatus,
    RT.TypeName,
    H.TaskDate
FROM Room R
JOIN RoomType RT ON R.RoomTypeId = RT.RoomTypeId
JOIN Housekeeping H ON R.RoomId = H.RoomId
WHERE H.TaskDate = CURRENT_DATE
  AND H.status = 'Pending';


SELECT 
    EXTRACT(MONTH FROM H.TaskDate) AS Month,
    EXTRACT(YEAR FROM H.TaskDate) AS Year,
    IU.ItemName,
    SUM(IU.Quantity) AS TotalUsed
FROM KeepingInventory KI
JOIN InventoryUsage IU ON KI.UsageId = IU.UsageId
JOIN Housekeeping H ON KI.TaskID = H.TaskID
GROUP BY Month, Year, IU.ItemName
ORDER BY Year, Month;


SELECT 
    R.RoomNumber,
    COUNT(M.RequestId) AS OpenRequests
FROM Room R
LEFT JOIN MaintenanceRequest M ON R.RoomId = M.RoomId AND (M.Status = 'Pending' OR M.Status = 'In Progress')
GROUP BY R.RoomNumber
ORDER BY OpenRequests DESC;


SELECT 
    S.FirstName || ' ' || S.LastName AS FullName,
    COUNT(AM.RequestId) AS AssignedRequests
FROM AssignMaintenanceStaff AM
JOIN Staff S ON AM.StaffId = S.StaffId
JOIN MaintenanceRequest MR ON AM.RequestId = MR.RequestId
WHERE EXTRACT(MONTH FROM MR.RequestDate) = EXTRACT(MONTH FROM CURRENT_DATE)
  AND EXTRACT(YEAR FROM MR.RequestDate) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY FullName
HAVING COUNT(AM.RequestId) > 0;

SELECT 
    R.RoomNumber,
    R.Floor,
    R.CleaningStatus
FROM Room R
LEFT JOIN Housekeeping H ON R.RoomId = H.RoomId AND H.TaskDate > CURRENT_DATE - INTERVAL '7 days'
WHERE H.TaskID IS NULL;

SELECT 
    H.TaskID,
    H.TaskDate,
    EXTRACT(MONTH FROM H.TaskDate) AS Month,
    EXTRACT(YEAR FROM H.TaskDate) AS Year,
    R.RoomNumber,
    R.Floor,
    RT.TypeName AS RoomType,
    H.Status AS TaskStatus,
    S.FirstName || ' ' || S.LastName AS StaffName
FROM Housekeeping H
JOIN Room R ON H.RoomId = R.RoomId
JOIN RoomType RT ON R.RoomTypeId = RT.RoomTypeId
JOIN AssignKeepingStaff AK ON H.TaskID = AK.TaskID
JOIN Staff S ON AK.StaffId = S.StaffId
WHERE H.TaskDate >= CURRENT_DATE - INTERVAL '3 months'
ORDER BY H.TaskDate DESC, R.RoomNumber;

SELECT 
    R.RoomNumber,
    R.PricePerNight,
    RT.BasePrice,
    RT.TypeName
FROM Room R
JOIN RoomType RT ON R.RoomTypeId = RT.RoomTypeId
WHERE R.PricePerNight > RT.BasePrice;

SELECT 
    RT.TypeName,
    AVG(IU.Quantity) AS AvgUsage
FROM Room R
JOIN RoomType RT ON R.RoomTypeId = RT.RoomTypeId
JOIN Housekeeping H ON R.RoomId = H.RoomId
JOIN KeepingInventory KI ON H.TaskID = KI.TaskID
JOIN InventoryUsage IU ON KI.UsageId = IU.UsageId
GROUP BY RT.TypeName;

--delete queries
DELETE FROM Housekeeping
WHERE TaskDate < CURRENT_DATE - INTERVAL '1 year';

DELETE FROM AssignMaintenanceStaff
WHERE StaffId IN (
    SELECT StaffId FROM Staff WHERE IsActive = FALSE
);

DELETE FROM InventoryUsage
WHERE UsageId NOT IN (
    SELECT UsageId FROM KeepingInventory
    UNION
    SELECT UsageId FROM MaintenanceInventory
);

--update queries
UPDATE Room
SET CleaningStatus = 'Clean'
WHERE RoomId IN (
    SELECT RoomId
    FROM Housekeeping
    WHERE TaskDate >= CURRENT_DATE - INTERVAL '3 days'
);

UPDATE Room
SET AvailabilityStatus = 'Unavailable'
WHERE RoomId IN (
    SELECT RoomId
    FROM MaintenanceRequest
    WHERE Status = 'In Progress'
      AND RequestDate >= CURRENT_DATE - INTERVAL '7 days'
);

UPDATE Staff
SET IsActive = FALSE
WHERE StaffId NOT IN (
    SELECT DISTINCT StaffId
    FROM AssignKeepingStaff AK
    JOIN Housekeeping H ON AK.TaskID = H.TaskID
    WHERE H.TaskDate >= CURRENT_DATE - INTERVAL '30 days'
);
