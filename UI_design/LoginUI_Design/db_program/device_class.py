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

class Comp:
    def __init__(self, comp_id: int = None,
                 comp_name: str = None,
                 component_id: str = None,
                 required_amount: int = 1):
        self.id: int = comp_id
        self.name: str = comp_name
        self.component_id: str = component_id
        self.required_amount: int = required_amount


class Inst:
    def __init__(self, inst_id: int = None,
                 inst_name: str = None,
                 inst_repeat_times: int = 1,
                 previous_inst: int = 0,
                 next_inst: int = 0,
                 start: bool = False):
        self.id: int = inst_id
        self.name: str = inst_name
        self.repeat_times: int = inst_repeat_times
        self.previous: int = previous_inst
        self.next: int = next_inst
        self.start: bool = start


class Step:
    def __init__(self, step_id: int = None, step_name: str = None, step_repeat_times: int = 1,
                 previous_step: int = 0, next_step: int = 0, start: bool = False, sub: bool = False,
                 sub_id: int = 0):
        self.id: int = step_id
        self.name: str = step_name
        self.repeat_times: int = step_repeat_times
        self.previous: int = previous_step
        self.next: int = next_step
        self.start: bool = start
        self.sub: bool = sub
        self.sub_id: int = sub_id


class Param:
    def __init__(self, param_id: int = None, param_name: str = None, data_status: bool = False,
                 initial_status: bool = False, sub: bool = False, sub_id: int = 0, value: float = 0,
                 upper_bound: float = 0, lower_bound: float = 0):
        self.id: int = param_id
        self.param_name: str = param_name
        self.data_statue: bool = data_status
        self.initial_status: bool = initial_status
        self.sub: bool = sub
        self.sub_id: int = sub_id
        self.value: float = value
        self.upper_bound: float = upper_bound
        self.lower_bound: float = lower_bound


class DeviceContext:
    def __init__(self, context_id: int, device_class: Device = Device(),
                 comp_class: Comp = Comp(), inst_class: Inst = Inst(),
                 step_class: Step = Step(), param_class: Param = Param()):
        self.id: int = context_id
        self.DeviceClass: Device = device_class
        self.CompClass: Comp = comp_class
        self.InstClass: Inst = inst_class
        self.StepClass: Step = step_class
        self.ParamClass: Param = param_class


class Process:
    def __init__(self, process_id: int, device_class: Device = None,
                 comp_class: Comp = None, last_step: int = None,
                 status: bool = 0):
        self.id: int = process_id
        self.DeviceClass: Device = device_class
        self.CompClass: Comp = comp_class
        self.LastStep: int = last_step
        self.status: bool = status


class Data:
    def __init__(self, data_id: int, inst_class: Inst = None, step_class: Step = None,
                 step_repeated: int = None, status: bool = 0, initial_status: bool = 0,
                 data_status: bool = 0, initial: str = None, data: str = None):
        self.id = data_id,
        self.InstClass: Inst = inst_class
        self.StepClass: Step = step_class
        self.StepRepeat: int = step_repeated
        self.Status: bool = status
        self.InitialStatus: bool = initial_status
        self.DataStatus: bool = data_status
        self.Initial: str = initial
        self.DataIn: str = data


class ProcessContext:
    def __init__(self, context_id: int, process_class: Process = None, data_class: Data = None):
        self.id: int = context_id
        self.ProcessClass: Process = process_class
        self.DataClass: Data = data_class
