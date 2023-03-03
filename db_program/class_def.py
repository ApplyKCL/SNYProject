# Author: Shaonan Hu
# Class that used to define the parameters
class Parameter:
    def __init__(self, parameter_id, parameter_name, parameter_value, parameter_upper, parameter_lower):
        self.id = parameter_id
        self.name = parameter_name
        self.value = parameter_value
        self.up = parameter_upper
        self.low = parameter_lower


# Class of Components
class Components:
    def __init__(self, comp_id, required_amount, next_comp, comp_name, parameters=[]):
        self.comp_id = comp_id
        self. required_amount = required_amount
        self. next_comp = next_comp
        self.comp_name = comp_name
        self.parameters = parameters


# Class of Employee
class Employee:
    def __init__(self, user_name, user_id, job, component=[]):
        self.name = user_name
        self.id = user_id
        self.job = job
        self.component = component

    def employee_op(self, operation_type):
        print(self.name)
        print(self.component[0].parameter[0].name)


class Administer(Employee):
    def admin_op(self):
        print(self.name)
