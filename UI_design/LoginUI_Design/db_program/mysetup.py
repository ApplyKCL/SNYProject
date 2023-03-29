# Author Shaonan Hu
import string


class HappyCat:
    def __init__(self, identifier : int, name : string, food : string):
        self.identifier = identifier
        self.name = name
        self.food = food
        self.happlist = []
        self.list_HappyCat()

    def list_HappyCat(self):
        self.happlist = []
        self.happlist.append(self.identifier)
        self.happlist.append(self.name)
        self.happlist.append(self.food)

    def HappyCat_list(self, tabel_clom : list):
        self.identifier = tabel_clom[0]
        self.name = tabel_clom[1]
        self.food = tabel_clom[2]
        self.list_HappyCat()


happyhappy = HappyCat(1, "MeowMeow", "Jar")
print(happyhappy.happlist)
happyhappy.identifier = 2
happyhappy.list_HappyCat()
print(happyhappy.identifier)
print(happyhappy.happlist)
update_list = [3, "HappyCat", "Milk"]
happyhappy.HappyCat_list(update_list)
print(happyhappy.happlist)


