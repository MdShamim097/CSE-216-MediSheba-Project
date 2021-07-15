create or replace PROCEDURE update_cabin_count_in_hospital(id in MEDI_SHEBA.HOSPITAL.HOSPITAL_ID%TYPE, c in NUMBER) IS
    amount NUMBER;
    BEGIN
        amount := c;
        UPDATE MEDI_SHEBA.HOSPITAL SET AVAILABLE_CABIN = amount WHERE HOSPITAL_ID = id;
        commit ;
    end;
