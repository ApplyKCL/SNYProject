# Author: Shaonan Hu
# Class that used to define the parameters


class device:
    def __init__(self, dev_id: int, device_name: str, product_id: str):
        self.id: int = dev_id
        self.device_name: str = device_name
        self.product_id: str = product_id

class comp:
    def __init__(self, comp_id: int, comp_name: str, component_id: str, required_amount: int):
        self.id: int = comp_id
        self.name: str = comp_name
        self.component_id: str = component_id
        self.required_amount: int = required_amount

class inst:
    def __init__(self, inst_id: int, inst_name: str,
                 inst_repeat_times: int, previous_inst: int, next_inst: int, start: bool):
        self.id: int = inst_id
        self.name: str = inst_name
        self.repeat_times: str = inst_repeat_times
        self.previous: int = previous_inst
        self.next: int = next_inst
        self.start: bool = start


class step:
    def __init__(self, step_id: int, step_name: str, step_repeat_times: int,
                 previous: int, next: int, start: bool, sub: bool, sub_id: int):
        self.id: int = step_id
        self.name: str = step_name
        self.repeat_times: int = step_repeat_times
        self.previous: int = previous
        self.next: int = next
        self.start: bool = start
        self.sub: bool = sub
        self.sub_id: int = sub_id







