-- RoomType
INSERT INTO RoomType (RoomTypeId, TypeName, MaxOccupancy, BasePrice) VALUES (401, 'Single', 1, 100.00);
INSERT INTO RoomType (RoomTypeId, TypeName, MaxOccupancy, BasePrice) VALUES (402, 'Double', 2, 150.00);
INSERT INTO RoomType (RoomTypeId, TypeName, MaxOccupancy, BasePrice) VALUES (403, 'Suite', 4, 300.00);

-- Staff
INSERT INTO Staff (StaffId, FirstName, LastName, Role, PhoneNumber, EmploymentDate, IsActive) VALUES (401, 'John', 'Doe', 'Cleaner', '0501234567', '2022-01-15', TRUE);
INSERT INTO Staff (StaffId, FirstName, LastName, Role, PhoneNumber, EmploymentDate, IsActive) VALUES (402, 'Jane', 'Smith', 'Technician', '0529876543', '2021-06-10', TRUE);
INSERT INTO Staff (StaffId, FirstName, LastName, Role, PhoneNumber, EmploymentDate, IsActive) VALUES (403, 'Mike', 'Brown', 'Manager', '0534567890', '2020-03-01', TRUE);

-- InventoryUsage
INSERT INTO InventoryUsage (UsageId, ItemName, Quantity) VALUES (401, 'Soap', 30);
INSERT INTO InventoryUsage (UsageId, ItemName, Quantity) VALUES (402, 'Shampoo', 20);
INSERT INTO InventoryUsage (UsageId, ItemName, Quantity) VALUES (403, 'Lightbulb', 5);

-- Room
INSERT INTO Room (RoomId, RoomNumber, PricePerNight, AvailabilityStatus, CleaningStatus, Floor, RoomTypeId) VALUES (401, 101, 120.00, 'Available', 'Clean', 1, 401);
INSERT INTO Room (RoomId, RoomNumber, PricePerNight, AvailabilityStatus, CleaningStatus, Floor, RoomTypeId) VALUES (402, 202, 150.00, 'Occupied', 'Dirty', 2, 402);
INSERT INTO Room (RoomId, RoomNumber, PricePerNight, AvailabilityStatus, CleaningStatus, Floor, RoomTypeId) VALUES (403, 303, 320.00, 'Available', 'Clean', 3, 403);

-- Housekeeping
INSERT INTO Housekeeping (TaskID, TaskDate, Status, RoomId) VALUES (401, '2025-04-01', 'Completed', 401);
INSERT INTO Housekeeping (TaskID, TaskDate, Status, RoomId) VALUES (402, '2025-04-02', 'Pending', 402);
INSERT INTO Housekeeping (TaskID, TaskDate, Status, RoomId) VALUES (403, '2025-04-03', 'InProgress', 403);

-- MaintenanceRequest
INSERT INTO MaintenanceRequest (RequestId, IssueDescription, RequestDate, Status, RoomId) VALUES (401, 'Air conditioner not working', '2025-04-01', 'Open', 402);
INSERT INTO MaintenanceRequest (RequestId, IssueDescription, RequestDate, Status, RoomId) VALUES (402, 'Leaky faucet', '2025-04-02', 'InProgress', 403);
INSERT INTO MaintenanceRequest (RequestId, IssueDescription, RequestDate, Status, RoomId) VALUES (403, 'Broken window', '2025-04-03', 'Resolved', 401);

-- AssignKeepingStaff
INSERT INTO AssignKeepingStaff (TaskID, StaffId) VALUES (401, 401);
INSERT INTO AssignKeepingStaff (TaskID, StaffId) VALUES (402, 401);
INSERT INTO AssignKeepingStaff (TaskID, StaffId) VALUES (403, 403);

-- AssignMaintenanceStaff
INSERT INTO AssignMaintenanceStaff (RequestId, StaffId) VALUES (401, 402);
INSERT INTO AssignMaintenanceStaff (RequestId, StaffId) VALUES (402, 402);
INSERT INTO AssignMaintenanceStaff (RequestId, StaffId) VALUES (403, 403);

-- MaintenanceInventory
INSERT INTO MaintenanceInventory (RequestId, UsageId) VALUES (401, 403);
INSERT INTO MaintenanceInventory (RequestId, UsageId) VALUES (402, 403);
INSERT INTO MaintenanceInventory (RequestId, UsageId) VALUES (403, 403);

-- KeepingInventory
INSERT INTO KeepingInventory (UsageId, TaskID) VALUES (401, 401);
INSERT INTO KeepingInventory (UsageId, TaskID) VALUES (402, 402);
INSERT INTO KeepingInventory (UsageId, TaskID) VALUES (401, 403);
