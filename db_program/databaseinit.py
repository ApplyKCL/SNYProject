class db_init:
    def __init__(self, db_cursor, db_name):
        self.db_cursor = db_cursor
        self.db_name = db_name

    def init_databases(self):
        cmd_str = "create database if not exists "
        cmd_str = cmd_str + self.db_name
        print("Database Inited")
        self.db_cursor.execute(cmd_str)

    def init_tb(self):
        cmd_str = """
                   create table if not exists employee(
                   id int auto_increment primary key unique,
                   account_number char(13),
                   name varchar(255),
                   password varchar(255),
                   job varchar(255),
                   entry_date date
                   )
                   """
        self.db_cursor.execute(cmd_str)
        cmd_str = """
                   create table if not exists component(
                   id int auto_increment primary key unique,
                   name varchar(255) not null,
                   require_amount int,
                   next_comp int null
                   )
           """
        self.db_cursor.execute(cmd_str)
        cmd_str = """
                   create table if not exists proceeding(
                   id int auto_increment primary key unique,
                   name varchar(255),
                   start_date date,
                   end_date date,
                   status bit
                   )
           """
        self.db_cursor.execute(cmd_str)

        cmd_str = """
                   create table if not exists aso_tb_pro(
                   id int auto_increment primary key unique,
                   employee_id int,
                   component_id int,
                   proceeding_id int,
                   constraint fk_emp_pro foreign key (employee_id) references employee(id),
                   constraint fk_comp_pro foreign key (component_id) references component(id),
                   constraint fk_pro_pro foreign key (proceeding_id) references proceeding(id)
                   )
           """
        self.db_cursor.execute(cmd_str)
        cmd_str = """
                   create table if not exists param(
                   id int auto_increment primary key unique,
                   name varchar(255),
                   value int,
                   upperbound int,
                   lowerbound int
                   )
           """
        self.db_cursor.execute(cmd_str)
        cmd_str = """
                   create table if not exists promopt(
                   id int auto_increment primary key unique,
                   name varchar(255),
                   content varchar(255)
                   )
           """
        self.db_cursor.execute(cmd_str)
        cmd_str = """
                   create table if not exists Aso_tb_com(
                   id int auto_increment primary key unique,
                   comp_id int,
                   promopt_id int,
                   paramter_id int,
                   constraint fk_comp_com foreign key(comp_id) references component(id),
                   constraint fk_prm_com foreign key(promopt_id) references promopt(id),
                   constraint fk_para_com foreign key(paramter_id) references param(id)
                   )
           """
        self.db_cursor.execute(cmd_str)
        print("Done Initialization")








