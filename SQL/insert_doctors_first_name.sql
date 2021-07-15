create or replace function insert_doctors_first_name(id IN MEDI_SHEBA.DOCTOR.DOCTOR_ID%TYPE, first_name IN MEDI_SHEBA.DOCTOR.FIRST_NAME%TYPE)
return  VARCHAR2
AS
   MSG VARCHAR2(100);
BEGIN
    MSG:= first_name;
    UPDATE MEDI_SHEBA.DOCTOR SET FIRST_NAME = MSG WHERE DOCTOR_ID = id;
    commit ;
    MSG:='First name inserted';
    RETURN MSG;
end;