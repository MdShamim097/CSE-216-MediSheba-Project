create or replace PROCEDURE update_a_pos_blood(id in MEDI_SHEBA.BLOOD_BANK.BLOOD_BANK_ID%TYPE, a_pos in MEDI_SHEBA.BLOOD_BANK.A_POS%TYPE) IS
    amount NUMBER;
    BEGIN
        amount := a_pos;
        UPDATE MEDI_SHEBA.BLOOD_BANK SET A_POS = amount WHERE BLOOD_BANK_ID = id;
        commit ;
    end;
