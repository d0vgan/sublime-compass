import sublime
from typing import List
from .sheet_group import SheetGroup
from .stack import get_stack

"""
This is more like Sheet stack
"""
class ViewStack():
    def __init__(self, window: sublime.Window, group: int):
        self.window = window
        self.group = group

        stack = get_stack(window, group) or []
        sheets_stack: List[SheetGroup] = []
        for item in stack:
            sheets = SheetGroup()
            for sheet_id in item[2]:
                sheets.append(sublime.Sheet(sheet_id))
            sheets.set_focused(sublime.Sheet(item[3]))
            sheets_stack.append(sheets)
        self.stack: List[SheetGroup] = sheets_stack

    def get(self, index: int):
        """
        @deprecated
        """
        if 0 <= index < len(self.stack):
            return self.stack[index]
        return None

    def push(self, window: sublime.Window, sheets: List[sublime.Sheet], group: int = 0):
        sheets = SheetGroup(sheets)

        for sheet in sheets:
            for i, sheet_stack in enumerate(self.stack):
                if sheet in sheet_stack:
                    self.stack[i].remove(sheet)

                    # remove if empty
                    if len(self.stack[i]) <= 0:
                        self.stack.pop(i)
                    break

        if len(sheets) == 1:
            sheets.set_focused(sheets[0])

        self.stack.insert(0, sheets)

    def append(self, window: sublime.Window, sheets: List[sublime.Sheet], group: int = 0):
        self.stack = [item for item in self.stack if item != sheets]
        self.stack.append(SheetGroup(sheets))

    def remove(self, sheet: sublime.Sheet):
        for i, sheet_stack in enumerate(self.stack):
            if sheet in sheet_stack:
                self.stack[i].remove(sheet)
                if len(self.stack[i]) <= 0:
                    self.stack.pop(i)
                break

    def clear(self):
        """
        @deprecated
        """
        self.stack = []

    def all(self) -> List[SheetGroup]:
        return self.stack

    def sheet_total(self):
        """
        @deprecated
        """
        total = 0
        for sheets in self.stack:
            total = total + sheets.__len__()
        return total

    def head(self):
        if self.stack.__len__() > 0:
            return self.stack[0]
        return None
