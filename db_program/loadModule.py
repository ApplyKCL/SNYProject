import string_function


def load_emp(db_cursor, mydb):
    cmd_str = """
            alter table employee auto_increment = 1;
        """
    db_cursor.execute(cmd_str)
    cmd_str = """
                insert into employee (name, account_number, password, job, entry_date) values 
                ('Boss Boss', '{}', '000000', 'Boss', current_date()),
                ('Shaonan Hu', '{}', '111111', 'Engineer', current_date()),
                ('Jiahao Chen', '{}', '222222', 'Engineer', current_date()),
                ('Jiawei Yang', '{}', '333333', 'Engineer', current_date()),
                ('Yilun Peng', '{}', '555555', 'Engineer', current_date())
    """
    cmd_str = string_function.fill_string(string=cmd_str)
    db_cursor.execute(cmd_str)
    mydb.commit()


def load_comp(db_cursor, mydb):
    cmd_str = """
            alter table component auto_increment = 1;
    """
    db_cursor.execute(cmd_str)
    cmd_str = """
            insert into component (name, require_amount, next_comp) values 
            ('Lens-V2-2020', '1', '2'),
            ('CEX-2022', '2', '3'),
            ('CPU-i9', '4', null)
    """
    db_cursor.execute(cmd_str)
    mydb.commit()


def load_prompt(db_cursor, mydb):
    cmd_str = """
            alter table promopt auto_increment = 1;
    """
    db_cursor.execute(cmd_str)
    cmd_str = """
            insert into promopt (name, content) values
            ('ST-00', 'Project Started, the first part to build is Lens-V2-2020.'),
            ('ST-01', 'To build this, please hold the bread and assemble is to the coffee.'),
            ('ST-02', null),
            ('ST-03', null),
            ('ST-04', null),
            ('ED-00', null),
            ('ED-01', null),
            ('ED-02', null),
            ('ED-03', null),
            ('ED-04', 'Project Ended, the Assessment will be displayed.'),
            ('ED-LV2', 'Lens-V2-2022 has finished, proceed to CEX-2022.'),
            ('ED-C2', 'CEX-2022 has finished, proceed to ED-C2.'),
            ('ED-CI', 'GoodJob.')
    """
    db_cursor.execute(cmd_str)
    mydb.commit()


def load_param(db_cursor, mydb):
    cmd_str = """
        alter table param auto_increment = 1;
        """
    db_cursor.execute(cmd_str)
    cmd_str = """
        insert into param (name, value, upperbound, lowerbound) values
        ('Lens-V2-2020-param_1', null, '20', '40'),
        ('Lens-V2-2020-param_2', null, '10', '30'),
        ('CEX-2022-param_1', '30', '20', '40'),
        ('CEX-2022-param-2', '40', '20', '40'),
        ('CPU-i9', '30', '20', '40'),
        ('CPU-i9', '40', '20', '40'),
        ('CPU-i9', '50', '20', '40')
    """
    db_cursor.execute(cmd_str)
    mydb.commit()


def load_com_table(db_cursor, mydb):
    cmd_str = """
            alter table aso_tb_com auto_increment = 1;
            """
    db_cursor.execute(cmd_str)
    cmd_str = """
    insert into aso_tb_com (comp_id, promopt_id, paramter_id) values 
    ('1', '11', '1'),
    ('1', '11', '2'),
    ('2', '12', '3'),
    ('2', '12', '4'),
    ('3', '13', '5'),
    ('3', '13', '7')
    """
    db_cursor.execute(cmd_str)
    mydb.commit()
