-- PROCEDURE: public.process_maintenance_and_report()

-- DROP PROCEDURE IF EXISTS public.process_maintenance_and_report();

CREATE OR REPLACE PROCEDURE public.process_maintenance_and_report(
	)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    total_bad_rooms INTEGER;
BEGIN
    -- Call the maintenance analysis procedure
    CALL analyze_and_schedule_maintenance();

    -- Get the number of problematic rooms (assumes count_problematic_rooms() function exists and returns integer)
    total_bad_rooms := count_problematic_rooms();

    -- Output the number of problematic rooms
    RAISE NOTICE 'Current number of problematic rooms: %', total_bad_rooms;
END;
$BODY$;
ALTER PROCEDURE public.process_maintenance_and_report()
    OWNER TO postgres;

-----------------------------------------------


-- PROCEDURE: public.prepare_and_assign_cleaner(integer)

-- DROP PROCEDURE IF EXISTS public.prepare_and_assign_cleaner(integer);

CREATE OR REPLACE PROCEDURE public.prepare_and_assign_cleaner(
	IN p_room_id integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    task_id INTEGER;
    staff_id INTEGER;
    cleaner_cursor REFCURSOR;
    cleaner_record RECORD;
BEGIN
    -- Step 1: Prepare the room (creates a cleaning task if needed)
    CALL prepare_room_for_reservation(p_room_id);

    -- Step 2: Check if a cleaning task was created today for the room
    SELECT hk.TaskID INTO task_id
    FROM Housekeeping hk
    WHERE hk.RoomId = p_room_id
      AND hk.TaskDate = CURRENT_DATE
      AND hk.Status = 'pending'
    ORDER BY hk.TaskID DESC
    LIMIT 1;

    IF task_id IS NULL THEN
        RAISE NOTICE 'No cleaning task created for room %. Nothing to assign.', p_room_id;
        RETURN;
    END IF;

    -- Step 3: Get the available cleaners (least number of pending tasks)
    cleaner_cursor := get_available_cleaners();

    -- Step 4: Fetch the first available cleaner
    FETCH cleaner_cursor INTO cleaner_record;

    IF FOUND THEN
        staff_id := cleaner_record.StaffId;

        -- Step 5: Assign the cleaner to the task
        INSERT INTO AssignKeepingStaff(TaskID, StaffId)
        VALUES (task_id, staff_id);

        RAISE NOTICE 'Assigned staff (ID: %) to cleaning task (TaskID: %).', staff_id, task_id;
    ELSE
        RAISE NOTICE 'No available cleaning staff. Manual assignment required for TaskID %.', task_id;
    END IF;

    -- Step 6: Close the cursor
    CLOSE cleaner_cursor;
END;
$BODY$;
ALTER PROCEDURE public.prepare_and_assign_cleaner(integer)
    OWNER TO postgres;
