CREATE OR REPLACE FUNCTION update_room_cleaning_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Status = 'Completed' THEN
        UPDATE Room
        SET CleaningStatus = 'Clean'
        WHERE RoomId = NEW.RoomId;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_cleaning_status
AFTER UPDATE OF Status ON Housekeeping
FOR EACH ROW
WHEN (NEW.Status = 'Completed')
EXECUTE FUNCTION update_room_cleaning_status();

-----------------------------------------------------------------

CREATE OR REPLACE FUNCTION prevent_double_booking()
RETURNS TRIGGER AS $$
DECLARE
    overlapping_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO overlapping_count
    FROM Reservation
    WHERE roomId = NEW.roomId
      AND status = 'booked'
      AND NEW.start_date < end_date
      AND NEW.end_date > start_date
      AND (reservation_id IS DISTINCT FROM NEW.reservation_id);

    IF overlapping_count > 0 THEN
        RAISE EXCEPTION 'Room % is already booked in the selected date range.', NEW.roomId;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_double_booking
BEFORE INSERT OR UPDATE ON Reservation
FOR EACH ROW
EXECUTE FUNCTION prevent_double_booking();
