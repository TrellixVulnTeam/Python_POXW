"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ProtobufExample.py
 @Time    : 2018/7/31 14:08
"""
import os
import test_pb2

ADDRESS_BOOK = "Address.txt"


def PromptForAddress(person):
    """
    输入个人信息
    :param person: 个人信息存储载体
    :return:
    """
    person.id = int(input("Enter person ID number: "))
    person.name = input("Enter name: ")

    email = input("Enter email address (blank for none): ")
    if email != "":
        person.email = email

    while True:
        number = input("Enter a phone number (or leave blank to finish): ")
        if number == "":
            break

        phone_number = person.phones.add()  # 生成电话号码的增量，关键字为repeated
        phone_number.number = number

        type = input("Is this a mobile, home, or work phone? ")
        if type == "mobile":
            phone_number.type = test_pb2.Person.MOBILE
        elif type == "home":
            phone_number.type = test_pb2.Person.HOME
        elif type == "work":
            phone_number.type = test_pb2.Person.WORK
        else:
            print("Unknown phone type; leaving as default value.")


def ListPeople(address_book):
    """
    个人信息展示
    :param address_book: 待展示的电话本
    :return:
    """
    for person in address_book.people:
        print("Person ID:", person.id)
        print("  " * 4 + "Name:", person.name)
        if person.HasField('email'):
            print("  " * 4 + "E-mail address:", person.email)

        # 根据类型显示电话号码
        for phone_number in person.phones:
            if phone_number.type == test_pb2.Person.MOBILE:
                print("  " * 4 + "Mobile phone #: ", end=" ")
            elif phone_number.type == test_pb2.Person.HOME:
                print("  " * 4 + "Home phone #: ", end=" ")
            elif phone_number.type == test_pb2.Person.WORK:
                print("  " * 4 + "Work phone #: ", end=" ")
            print(phone_number.number)


address_books = test_pb2.AddressBook()

# 从文件中反序列化
if os.path.isfile(ADDRESS_BOOK):
    with open(ADDRESS_BOOK, "rb") as f:
        address_books.ParseFromString(f.read())         # 从字符串中读取

ListPeople(address_books)
PromptForAddress(address_books.people.add())  # 传入值为个人信息的列表增量，关键字为repeated

# 序列化数据至文件
with open(ADDRESS_BOOK, "wb") as f:
    f.write(address_books.SerializeToString())          # 序列化到字符串，用于存储
