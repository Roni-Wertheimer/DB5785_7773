ALTER TABLE InventoryUsage
ADD CONSTRAINT chk_quantity_positive
CHECK (Quantity > 0);

ALTER TABLE MaintenanceRequest
ALTER COLUMN Status SET DEFAULT 'Pending';

ALTER TABLE Staff
ALTER COLUMN IsActive SET DEFAULT TRUE;
