-- FUNCTION: public.count_problematic_rooms()

-- DROP FUNCTION IF EXISTS public.count_problematic_rooms();

CREATE OR REPLACE FUNCTION public.count_problematic_rooms(
	)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    total INTEGER;
BEGIN
    SELECT COUNT(*) INTO total
    FROM Room
    WHERE MaintenanceNote IS NOT NULL
      AND (CleaningStatus != 'clean'
           OR EXISTS (
                SELECT 1 FROM MaintenanceRequest
                WHERE RoomId = Room.RoomId AND Status != 'closed'
           ));

    RETURN total;
END;
$BODY$;

ALTER FUNCTION public.count_problematic_rooms()
    OWNER TO postgres;

-------------------------------------------------

CREATE OR REPLACE FUNCTION public.get_available_cleaners()
RETURNS refcursor
LANGUAGE plpgsql
AS $$
DECLARE
    cleaner_cursor REFCURSOR;
BEGIN
    OPEN cleaner_cursor FOR
        SELECT s.StaffId, s.FirstName, s.LastName,
               COUNT(hk.TaskID) AS pending_tasks
        FROM Staff s
        LEFT JOIN AssignKeepingStaff aks ON aks.StaffId = s.StaffId
        LEFT JOIN Housekeeping hk ON hk.TaskID = aks.TaskID
                                    AND hk.Status != 'Completed'
                                    AND hk.TaskDate = CURRENT_DATE
        WHERE s.Role = 'cleaner' AND s.IsActive = TRUE
        GROUP BY s.StaffId, s.FirstName, s.LastName
        HAVING COUNT(hk.TaskID) = 0 
        ORDER BY s.LastName, s.FirstName;

    RETURN cleaner_cursor;
END;
$$;
