create or replace function insert_into_doctor_schedule( id IN  NUMBER)
RETURN VARCHAR2
IS MSG VARCHAR2(100);
BEGIN
    INSERT INTO MEDI_SHEBA.DOCTOR_SCHEDULE(DOCTOR_ID) VALUES (id);
    COMMIT ;
    MSG:='OK INSERTED';
    RETURN MSG;
end;
/