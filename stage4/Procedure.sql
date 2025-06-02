CREATE OR REPLACE PROCEDURE public.analyze_and_schedule_maintenance()
LANGUAGE plpgsql
AS $$
DECLARE
    room_rec RECORD;
    has_open_issue BOOLEAN;
    task_id INT;
    new_request_id INT;
BEGIN
    FOR room_rec IN
        SELECT r.RoomId, r.RoomNumber, r.CleaningStatus
        FROM Room r
        WHERE NOT EXISTS (
            SELECT 1
            FROM Reservation res
            WHERE res.roomId = r.RoomId
              AND res.start_date > CURRENT_DATE - INTERVAL '60 days'
        )
    LOOP
        -- Check if there is already an open maintenance issue
        SELECT EXISTS (
            SELECT 1
            FROM MaintenanceRequest mr
            WHERE mr.RoomId = room_rec.RoomId AND mr.Status != 'closed'
        )
        INTO has_open_issue;

        -- If the room is dirty or has no bookings recently or needs attention
        IF room_rec.CleaningStatus != 'clean' OR NOT has_open_issue THEN

		            -- Schedule housekeeping task if the room is dirty
            IF room_rec.CleaningStatus != 'clean' THEN
                SELECT COALESCE(MAX(TaskID), 0) + 1 INTO task_id FROM Housekeeping;

				INSERT INTO Housekeeping(TaskID, TaskDate, Status, RoomId)
				VALUES (task_id, CURRENT_DATE, 'pending', room_rec.RoomId);


                RAISE NOTICE 'Housekeeping task scheduled for Room % (TaskID: %)', room_rec.RoomNumber, task_id;

            -- Create maintenance request if none exists
            ELSE
                -- Generate next available RequestId
                SELECT COALESCE(MAX(RequestId), 0) + 1
                INTO new_request_id
                FROM MaintenanceRequest;

                INSERT INTO MaintenanceRequest(RequestId, IssueDescription, RequestDate, Status, RoomId)
                VALUES (
                    new_request_id,
                    'Auto-detected unbooked room for over 60 days',
                    CURRENT_DATE,
                    'open',
                    room_rec.RoomId
                );

                RAISE NOTICE 'Maintenance request created for Room % (RequestID: %)', room_rec.RoomNumber, new_request_id;
            END IF;


            -- Update room note
            UPDATE Room
            SET MaintenanceNote = CONCAT(
                'Room unused for over 60 days. Auto-scheduled maintenance and cleaning on ',
                CURRENT_DATE
            )
            WHERE RoomId = room_rec.RoomId;

            RAISE NOTICE 'Room % marked for maintenance and/or cleaning.', room_rec.RoomNumber;
        END IF;
    END LOOP;

EXCEPTION
    WHEN OTHERS THEN
        RAISE WARNING 'Error during maintenance analysis: %', SQLERRM;
END;
$$;

ALTER PROCEDURE public.analyze_and_schedule_maintenance()
    OWNER TO postgres;
------------------------------------------------------

CREATE OR REPLACE PROCEDURE public.prepare_room_for_reservation(
	IN p_room_id integer)
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    is_dirty BOOLEAN;
    has_open_issue BOOLEAN;
    task_id INTEGER;
    staff_id INTEGER;
BEGIN
    -- Check if the room needs cleaning
    SELECT (CleaningStatus != 'clean') INTO is_dirty
    FROM Room
    WHERE RoomId = p_room_id;

    -- Check if there are open maintenance issues
    SELECT EXISTS (
        SELECT 1 FROM MaintenanceRequest
        WHERE RoomId = p_room_id AND Status != 'closed'
    ) INTO has_open_issue;

    -- Create cleaning task if needed
    IF is_dirty THEN
        -- Find next TaskID
        SELECT COALESCE(MAX(TaskID), 0) + 1 INTO task_id FROM Housekeeping;

        -- Insert new housekeeping task with calculated TaskID
        INSERT INTO Housekeeping(TaskID, TaskDate, Status, RoomId)
        VALUES (task_id, CURRENT_DATE, 'pending', p_room_id);

        RAISE NOTICE 'Cleaning task created for room % (TaskID: %)', p_room_id, task_id;
    END IF;

    -- Notify about open issues
    IF has_open_issue THEN
        RAISE NOTICE 'Room % has an open maintenance issue. Action required before guest arrival.', p_room_id;
    END IF;

    -- Update room maintenance note
    IF is_dirty OR has_open_issue THEN
        UPDATE Room
        SET MaintenanceNote = CONCAT('Rebooked on ', CURRENT_DATE,
                                     CASE WHEN is_dirty THEN '. Cleaning required' ELSE '' END,
                                     CASE WHEN has_open_issue THEN '. Open maintenance issue' ELSE '' END)
        WHERE RoomId = p_room_id;
    END IF;
END;
$BODY$;
