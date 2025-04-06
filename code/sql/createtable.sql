CREATE TABLE RoomType (
    RoomTypeId INTEGER PRIMARY KEY,
    TypeName VARCHAR(50) NOT NULL,
    MaxOccupancy INTEGER NOT NULL,
    BasePrice NUMERIC(10, 2) NOT NULL
);

CREATE TABLE Staff (
    StaffId INTEGER PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    EmploymentDate DATE NOT NULL,
    IsActive BOOLEAN NOT NULL
);

CREATE TABLE InventoryUsage (
    UsageId INTEGER PRIMARY KEY,
    ItemName VARCHAR(50) NOT NULL,
    Quantity INTEGER NOT NULL
);

CREATE TABLE Room (
    RoomId INTEGER PRIMARY KEY,
    RoomNumber INTEGER NOT NULL,
    PricePerNight NUMERIC(10, 2) NOT NULL,
    AvailabilityStatus VARCHAR(20) NOT NULL,
    CleaningStatus VARCHAR(20) NOT NULL,
    Floor INTEGER NOT NULL,
    RoomTypeId INTEGER NOT NULL,
    FOREIGN KEY (RoomTypeId) REFERENCES RoomType(RoomTypeId)
);

CREATE TABLE Housekeeping (
    TaskID INTEGER PRIMARY KEY,
    TaskDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL,
    RoomId INTEGER NOT NULL,
    FOREIGN KEY (RoomId) REFERENCES Room(RoomId)
);

CREATE TABLE MaintenanceRequest (
    RequestId INTEGER PRIMARY KEY,
    IssueDescription TEXT NOT NULL,
    RequestDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL,
    RoomId INTEGER NOT NULL,
    FOREIGN KEY (RoomId) REFERENCES Room(RoomId)
);

CREATE TABLE AssignKeepingStaff (
    TaskID INTEGER NOT NULL,
    StaffId INTEGER NOT NULL,
    PRIMARY KEY (TaskID, StaffId),
    FOREIGN KEY (TaskID) REFERENCES Housekeeping(TaskID),
    FOREIGN KEY (StaffId) REFERENCES Staff(StaffId)
);

CREATE TABLE AssignMaintenanceStaff (
    RequestId INTEGER NOT NULL,
    StaffId INTEGER NOT NULL,
    PRIMARY KEY (RequestId, StaffId),
    FOREIGN KEY (RequestId) REFERENCES MaintenanceRequest(RequestId),
    FOREIGN KEY (StaffId) REFERENCES Staff(StaffId)
);

CREATE TABLE MaintenanceInventory (
    RequestId INTEGER NOT NULL,
    UsageId INTEGER NOT NULL,
    PRIMARY KEY (RequestId, UsageId),
    FOREIGN KEY (RequestId) REFERENCES MaintenanceRequest(RequestId),
    FOREIGN KEY (UsageId) REFERENCES InventoryUsage(UsageId)
);

CREATE TABLE KeepingInventory (
    UsageId INTEGER NOT NULL,
    TaskID INTEGER NOT NULL,
    PRIMARY KEY (UsageId, TaskID),
    FOREIGN KEY (UsageId) REFERENCES InventoryUsage(UsageId),
    FOREIGN KEY (TaskID) REFERENCES Housekeeping(TaskID)
);
