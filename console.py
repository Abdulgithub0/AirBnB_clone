#!/usr/bin/python3
""" A command line processor for manipulate objects
    created from Base class and its various subclasses
"""

import cmd
import sys
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class Console(cmd.Cmd):
    prompt = ""

    dict_cls = {"BaseModel": BaseModel, "User": User,
                "Place": Place,
                "State": State, "City": City,
                "Amenity": Amenity, "Review": Review}

    if sys.stdin.isatty():
        prompt = "(hbnb) "

    def preloop(self):
        """command to be excuted before cmdloop invocation"""
        if not sys.stdin.isatty():
            print("(hbnb)")

    def do_create(self, new_instance):
        """This method creates a new instance of BaseModel and
        saves it (to the file.json in the current dir)
        then prints out the id of the created instance.
        """
        if (new_instance):
            if (new_instance in self.dict_cls.keys()):
                new_instance = self.dict_cls[new_instance]()
            # if (new_instance == "BaseModel"):
                # new_instance = BaseModel()
                new_instance.save()
                print(new_instance.id)
            else:
                print("** class doesn't exist **")
        else:
            print("**class name missing **")

    def do_show(self, key):
        """Prints the string representation of an instance
        based on the class name and id.
        Ex:(hbnb)$ show BaseModel 1234-1234-1234.
        """
        from models import storage
        if (key):
            key_list = key.split()
            length = len(key_list)
            if (key_list[0] in self.dict_cls.keys()):
                if (length == 2):
                    delim = "."
                    get_obj = delim.join(key_list)
                    loader = storage.all()
                    obj = loader.get(get_obj, "** no instance found **")
                    print(obj)
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_destroy(self, key):
        """Delete an instance based on the class name and id
        (save the change into the JSON file).
        Ex: (hbnb)$ destroy BaseModel 1234-1234-1234.
        """
        from models import storage
        if (key):
            key_list = key.split()
            length = len(key_list)
            if (key_list[0] in self.dict_cls.keys()):
                if (length == 2):
                    delim = "."
                    get_obj = delim.join(key_list)
                    loader = storage.all()
                    obj = loader.get(get_obj, "** no instance found **")
                    if (obj != "** no instance found **"):
                        del loader[get_obj]
                        storage.save()
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_all(self, cls_name):
        """ Prints all string representation of all instances based
        or not on the class name. Ex:(hbnb) $ all BaseModel or $
        """
        from models import storage
        to_list = []
        for obj in storage.all().values():
            to_list.append(obj.__str__())
        if (cls_name):
            if (cls_name in self.dict_cls.keys()):
                print(to_list)
            else:
                print("** class doesn't exist **")
        else:
            print(to_list)

    @staticmethod
    def rm_quotation(string):
        """handle attr value surrounded with single or double quotation"""
        tup = (34, 39)
        if (ord(string[0]) in tup and ord(string[-1]) in tup):
            return (string[1:-1])
        else:
            return string

    def do_update(self, attr):
        """Updates an instance based on the class name and id by adding or
            updating attribute (save the change into the JSON file).
            Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com".
        """
        from models import storage
        if (attr):
            list_attr = attr.split()
            length = len(list_attr)
            if (list_attr[0] in self.dict_cls.keys()):
                if (length >= 2):
                    delim = '.'
                    key = delim.join(list_attr[0:2])
                    load_dict = storage.all()
                    get_val = load_dict.get(key, "no")
                    if (get_val != "no"):
                        if (length >= 3):
                            if (length >= 4):
                                value = self.rm_quotation(list_attr[3])
                                setattr(get_val, list_attr[2], value)
                                storage.save()
                            else:
                                print("** value missing **")
                        else:
                            print("** attribute name missing **")
                    else:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    @staticmethod
    def all_and_count(classname, command):
        """This method handles default argument:
            <class name>.all() or class name>.count() command
        """
        from models import storage
        load_obj = storage.all()
        lst = []
        count = 0
        tup = ("BaseModel", "User", "Amenity",
               "Review", "Place", "State", "City")
        if (classname in tup):
            for keys, cls_obj in load_obj.items():
                c_name = keys[0:keys.index('.')]
                if c_name == classname:
                    count += 1
                    lst.append(cls_obj.__str__())
            if (command == "all()"):
                print(lst)
            else:
                print(count)
        else:
            print("** class doesn't exist **")

    @staticmethod
    def handle_update(string, clsname):
        """This method handle default command
        <class name>.update(<id>, <attribute name>, <attribute value>).
        """
        restruct = string.split(",")
        length = len(restruct)
        print(restruct)
        id_tag = ""
        atrr_name = ""
        attr_val = ""
        # I need to nested this below if-elif statement
        # inside a try and except block to manage in IndexError
        if (length >= 3):
            id_tag = Console.rm_quotation(restruct[0][7:])
            attr_name = Console.rm_quotation(restruct[1][1:])
            index = restruct[2].index(')')
            attr_val = Console.rm_quotation(restruct[2][1:index])
        elif (length == 2):
            d_tag = Console.rm_quotation(restruct[0][7:])
            attr_name = Console.rm_quotation(restruct[1][1:])
        elif (length == 1):
            id_tag = Console.rm_quotation(restruct[0][7:])
        concat = clsname + " " + id_tag + " " + attr_name + " " + attr_val
        return (concat)

    def default(self, string):
        """handle commands/methods that's not explicitly defined"""
        args = string.split('.')
        length = len(args)
        # I need to nested this below if-elif statement
        # inside a try and except block to manage in IndexError
        if (length >= 2) and (args[1] == "all()" or args[1] == "count()"):
            self.all_and_count(args[0], args[1])
        elif (length >= 2 and (args[1][:4] == "show")):
            concat = args[0] + " "
            concat += self.rm_quotation(args[1][6:-2])
            self.do_show(concat)
        elif (length >= 2 and (args[1][:7]) == "destroy"):
            concat = args[0] + " "
            concat += self.rm_quotation(args[1][9:-2])
            self.do_destroy(concat)
        elif (length >= 2 and args[1][:6] == "update"):
            data = self.handle_update(args[1], args[0])
            self.do_update(data)

    def postcmd(self, stop, line):
        """handle post cmd command during isatty"""
        if not sys.stdin.isatty():
            print("(hbnb) ", end='')
        return stop

    def emptyline(self):
        """handler for empty argument"""
        pass

    def do_EOF(self, line):
        """handle for EOF signal"""
        "Exit"
        return True

    def do_quit(self, line):
        """The quit command terminate the Console"""
        sys.exit(0)


if __name__ == '__main__':
    Console().cmdloop()
