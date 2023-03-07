# Author: Shaonan Hu
# Class that used to define the parameters


class Device:
    def __init__(self, dev_id: int, device_name: str, product_id: str):
        self.id: int = dev_id
        self.device_name: str = device_name
        self.product_id: str = product_id


class Comp:
    def __init__(self, comp_id: int, comp_name: str, component_id: str, required_amount: int):
        self.id: int = comp_id
        self.name: str = comp_name
        self.component_id: str = component_id
        self.required_amount: int = required_amount


class Inst:
    def __init__(self, inst_id: int, inst_name: str,
                 inst_repeat_times: int, previous_inst: int, next_inst: int, start: bool):
        self.id: int = inst_id
        self.name: str = inst_name
        self.repeat_times: int = inst_repeat_times
        self.previous: int = previous_inst
        self.next: int = next_inst
        self.start: bool = start


class Step:
    def __init__(self, step_id: int, step_name: str, step_repeat_times: int,
                 previous_step: int, next_step: int, start: bool, sub: bool, sub_id: int):
        self.id: int = step_id
        self.name: str = step_name
        self.repeat_times: int = step_repeat_times
        self.previous: int = previous_step
        self.next: int = next_step
        self.start: bool = start
        self.sub: bool = sub
        self.sub_id: int = sub_id


class Param:
    def __init__(self, param_id: int, param_name: str, data_status: bool,
                 initial_status: bool, sub: bool, sub_id: int, value: float,
                 upper_bound: float, lower_bound: float):
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
    def __init__(self, context_id: int, device_class: Device = None,
                 comp_class: Comp = None, inst_class: Inst = None,
                 step_class: Step = None, param_class: Param = None):
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
