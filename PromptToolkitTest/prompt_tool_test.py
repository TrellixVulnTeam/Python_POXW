#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: prompt_tool_test.py
@time: 2020/4/1
@author: alfons
"""
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt

# results = checkboxlist_dialog(
#     title="CheckboxList dialog",
#     text="What would you like in your breakfast ?",
#     values=[
#         ("eggs", "Eggs"),
#         ("bacon", "Bacon"),
#         ("croissants", "20 Croissants"),
#         ("daily", "The breakfast of the day")
#     ],
#     style=Style.from_dict({
#         'dialog': 'bg:#cdbbb3',
#         'button': 'bg:#bf99a4',
#         'checkbox': '#e8612c',
#         'dialog.body': 'bg:#a9cfd0',
#         'dialog shadow': 'bg:#c98982',
#         'frame.label': '#fcaca3',
#         'dialog.body label': '#fd8bb6',
#     })
# ).run()

from prompt_toolkit.completion import Completer, Completion


class MyCustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        # Display this completion, black on yellow.
        yield Completion('completion1', start_position=0,
                         style='bg:ansiyellow fg:ansiblack')

        # Underline completion.
        yield Completion('completion2', start_position=0,
                         style='underline')

        # Specify class name, which will be looked up in the style sheet.
        yield Completion('completion3', start_position=0,
                         style='class:special-completion')


prompt(completer=MyCustomCompleter())
