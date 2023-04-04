# Author: Shaonan Hu
# Class that used to define the parameters

class Device:
    def __init__(self, dev_id: int = None,
                 device_name: str = None,
                 product_id: str = None):
        self.id: int = dev_id
        self.device_name: str = device_name
        self.product_id: str = product_id
        self.length = 3
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.device_name)
        self.elements_list.append(self.product_id)

    def update_elements_list(self, table_colm):
        """
        :param table_colm: The Updated Value for the list
        :return:
        """
        # Check if the colm length is equal to the correct length
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.device_name = table_colm[1]
        self.product_id = table_colm[2]
        # Function Call to list the variables
        self.list_elements()


class Comp:
    def __init__(self, comp_id: int = None,
                 comp_name: str = None,
                 component_id: str = None,
                 required_amount: int = 1):
        self.id: int = comp_id
        self.name: str = comp_name
        self.component_id: str = component_id
        self.required_amount: int = required_amount
        self.length = 4
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.name)
        self.elements_list.append(self.component_id)
        self.elements_list.append(self.required_amount)

    def update_elements_list(self, table_colm):
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.name = table_colm[1]
        self.component_id = table_colm[2]
        self.required_amount = table_colm[3]
        self.list_elements()


class Inst:
    def __init__(self, inst_id: int = None,
                 inst_name: str = None,
                 inst_repeat_times: int = 1,
                 previous_inst: int = 0,
                 next_inst: int = 0,
                 ):
        self.id: int = inst_id
        self.name: str = inst_name
        self.repeat_times: int = inst_repeat_times
        self.previous: int = previous_inst
        self.next: int = next_inst
        self.length = 5
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.name)
        self.elements_list.append(self.repeat_times)
        self.elements_list.append(self.previous)
        self.elements_list.append(self.next)

    def update_elements_list(self, table_colm):
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.name = table_colm[1]
        self.repeat_times = table_colm[2]
        self.previous = table_colm[3]
        self.next = table_colm[4]
        self.list_elements()


class Step:
    def __init__(self, step_id: int = None, step_name: str = None, step_repeat_times: int = 1,
                 previous_step: int = 0, next_step: int = 0):
        self.id: int = step_id
        self.name: str = step_name
        self.repeat_times: int = step_repeat_times
        self.previous: int = previous_step
        self.next: int = next_step
        self.length = 5
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.name)
        self.elements_list.append(self.repeat_times)
        self.elements_list.append(self.previous)
        self.elements_list.append(self.next)

    def update_elements_list(self, table_colm):
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.name = table_colm[1]
        self.repeat_times = table_colm[2]
        self.previous = table_colm[3]
        self.next = table_colm[4]
        self.list_elements()


class Param:
    def __init__(self, param_id: int = None, param_name: str = None, previous_param: int = 0,
                 next_param: int = 0):
        self.id: int = param_id
        self.param_name: str = param_name
        self.previous: int = previous_param
        self.next: int = next_param
        self.length = 4
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.param_name)
        self.elements_list.append(self.previous)
        self.elements_list.append(self.next)

    def update_elements_list(self, table_colm):
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.param_name = table_colm[1]
        self.previous = table_colm[2]
        self.next = table_colm[3]
        self.list_elements()


class DeviceContext:
    def __init__(self, context_id: int = None, device_class: Device = Device(),
                 comp_class: Comp = Comp(), inst_class: Inst = Inst(),
                 step_class: Step = Step(), param_class: Param = Param()):
        self.id: int = context_id
        self.DeviceClass: Device = device_class
        self.CompClass: Comp = comp_class
        self.InstClass: Inst = inst_class
        self.StepClass: Step = step_class
        self.ParamClass: Param = param_class
        self.length = 6
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.DeviceClass)
        self.elements_list.append(self.CompClass)
        self.elements_list.append(self.InstClass)
        self.elements_list.append(self.StepClass)
        self.elements_list.append(self.ParamClass)

    def update_elements_list(self, table_colm):
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.DeviceClass = table_colm[1]
        self.CompClass = table_colm[2]
        self.InstClass = table_colm[3]
        self.StepClass = table_colm[4]
        self.ParamClass = table_colm[5]
        self.list_elements()


class Process:
    def __init__(self, process_id: int = None, barcode: str = None, device_class: Device = Device(),
                 comp_class: Comp = Comp(),
                 status: bool = 0):
        self.id: int = process_id
        self.barcode: str = barcode
        self.DeviceClass: Device = device_class
        self.CompClass: Comp = comp_class
        self.status: bool = status
        self.length = 5
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.DeviceClass.id)
        self.elements_list.append(self.CompClass.id)
        self.elements_list.append(self.barcode)
        self.elements_list.append(self.status)

    def update_elements_list(self, table_colm):
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.DeviceClass.id = table_colm[1]
        self.CompClass.id = table_colm[2]
        self.barcode = table_colm[3]
        self.status = table_colm[4]
        self.list_elements()


class Data:
    def __init__(self, data_id: int = None, inst_class: Inst = Inst(), step_class: Step = Step(), param_class: Param = Param(),
                 step_repeated: int = 0, data: str = None):
        self.id = data_id,
        self.InstClass: Inst = inst_class
        self.StepClass: Step = step_class
        self.ParamClass: Param = param_class
        self.StepRepeat: int = step_repeated
        self.Data: str = data
        self.length = 6
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.InstClass.id)
        self.elements_list.append(self.StepClass.id)
        self.elements_list.append(self.ParamClass.id)
        self.elements_list.append(self.StepRepeat)
        self.elements_list.append(self.Data)

    def update_elements_list(self, table_colm):
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.InstClass.id = table_colm[1]
        self.StepClass.id = table_colm[2]
        self.ParamClass.id = table_colm[3]
        self.StepRepeat = table_colm[4]
        self.Data = table_colm[5]
        self.list_elements()


class ProcessContext:
    def __init__(self, context_id: int = None, process_class: Process = Process(), data_class: Data = Data()):
        self.id: int = context_id
        self.ProcessClass: Process = process_class
        self.DataClass: Data = data_class
        self.length = 3
        self.elements_list = []
        self.list_elements()

    def list_elements(self):
        self.elements_list = []
        self.elements_list.append(self.id)
        self.elements_list.append(self.ProcessClass.id)
        self.elements_list.append(self.DataClass.id)

    def update_elements_list(self, table_colm):
        if len(table_colm) != self.length:
            return None
        self.id = table_colm[0]
        self.ProcessClass.id = table_colm[1]
        self.DataClass.id = table_colm[2]
        self.list_elements()
