#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import copy

class Construct(object):
    """
        Базовый класс для конструкций языка C
    """
    def __new__(cls, *args, **kwargs):
        """
        """
        return super(Construct, cls).__new__(cls)

    def add(self, item):
        """
            Добавление конструкции внутрь данной конструкции
        """
        item = copy(item)
        if not item in self.detailes:
            self.detailes.append(item)

    def _getBody(self):
        """
        """
        body = ''
        for item in self.detailes:
            body += '\n\t' + "\n\t".join(item.__str__().split('\n'))
        return body

    def _end(self):
        """
            Окончание конструкции
        """
        return '\n}'

    def _return(self):
        variables = ''
        body = self._getBody()
        if len(self.vars) > 0:
            for i in self.vars:
                initVar = ''
                if self.vars[i][1] != '': # требуется инициализация
                    initVar = ' = ' + self.vars[i][1]
                variables += '\n\t' + "\n\t".join([ self.vars[i][0] + ' ' + i + initVar + ';' ])
        return self.definition + variables + body + self._end()

    def __copy__(self):
        """
        """
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __add__(self, other):
        """
        """
        return self._return() + other

    def __radd__(self, other):
        """
        """
        return other + self._return()

    def __str__(self):
        """
            Генерация строки конструкции
        """
        return self._return()

    def addComment(self, comment = ''):
        """
            Добавление комментария к конструкции
        """
        if comment == '':
            comment = self.__class__.__name__
        if not hasattr(self, 'comment'):
            self.definition = '/*\n * ' + "\n * ".join(comment.__str__().split('\n')) + '\n */\n' + self.definition
            self.comment = True

    def addPrefix(self, prefix = ''):
        """
            Добавление строки к самому началу конструкции
        """
        if not hasattr(self, 'prefix'):
            self.definition = prefix + ' ' + self.definition
            self.prefix = True

    def addVar(self, typeVar, nameVar, initVar = ''):
        """
        """
        self.vars.update({nameVar : [typeVar, initVar]})


class Macros(Construct):
    """
        Базовый класс для конструкций вида #macro
    """
    def add(self, item):
        """
            В конструкцию невозможно добавлять другие конструкции
        """
        pass

    def _return(self):
        body = self._getBody()
        return self.definition + body + self._end()

    def _getBody(self):
        """
        """
        body = ''
        for item in self.detailes:
            body += '\n' + "\n".join(item.__str__().split('\n'))
        return body

    def _end(self):
        """
            Окончание конструкции
        """
        return ''

class Source(Construct):
    """
        Класс для описания исходного кода
    """
    def __init__(self):
        """
        """
        self.vars = {}
        self.definition = ''
        self.body = ''
        self.detailes = []

    def add(self, item):
        """
            Переопределенный метод для иного добавления подконструкций
        """
        item = copy(item)
        if not item in self.detailes:
            self.detailes.append(item)

    def _getBody(self):
        """
        """
        body = ''
        for item in self.detailes:
            body += '\n' + item.__str__() + '\n'
        return body

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return ''

    def addComment(self, comment = ''):
        pass

    def addPrefix(self, prefix = ''):
        pass


class Function(Construct):
    """
        Класс для описания функций
    """
    def __init__(self, type = 'void', name = 'main', argv = ['void']):
        """
        """
        self.vars = {}
        self._type = type
        self._name = name
        self._argv = argv
        self.definition = self._type + ' ' + self._name + '(' + ', '.join(self._argv) + ') {'
        self.body = ''
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._type, self._name, self._argv)
        newone.__dict__.update(self.__dict__)
        return newone

    def changeDefinition(self, type = 'void', name = 'main', argv = ['void']):
        """
        """
        self.definition = type + ' ' + name + '(' + ', '.join(argv) + ') {'


class Struct(Construct):
    """
        Класс для описания структур
    """
    def __init__(self, name, declaration = True):
        """
        """
        self.vars = {}
        self._name = name
        self._declaration = declaration
        self.definition = 'struct ' + self._name + ' {'
        self.body = ''
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._name, self._declaretion)
        newone.__dict__.update(self.__dict__)
        return newone

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return '\n}' + (' ' + self._name)*self._declaration + ';'


class Enum(Construct):
    """
        Класс для описания перечислений
    """
    def __init__(self, name = '', declaration = False):
        """
        """
        self.vars = {}
        self._name = name
        self._declaration = declaration
        self.definition = 'enum {'
        self.body = ''
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._name, self._declaration)
        newone.__dict__.update(self.__dict__)
        return newone

    def _return(self):
        variables = ''
        body = self._getBody()
        if len(self.vars) > 0:
            for i in self.vars:
                initVar = ''
                if self.vars[i][1] != '': # требуется инициализация
                    initVar = ' = ' + self.vars[i][1]
                variables += '\n\t' + "\n\t".join([ self.vars[i][0] + ' ' + i + initVar + ',' ])
        return self.definition + variables + body + self._end()

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return '\n}' + (' ' + self._name)*self._declaration + ';'


class Line(Construct):
    """
        Класс для описания строки
    """
    def __init__(self, type = '', name = '', operator = '', _name = '', nosep = False):
        """
        """
        self.vars = {}
        self._type = type
        self._name = name
        self._operator = operator
        self.__name = _name
        self._nosep = nosep
        self.definition = self._type + ' ' + self._name + ' ' + self._operator + ' ' + self.__name
        self.definition = self.definition.strip(' ')
        self.body = ''
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._type, self._name, self._operator, self.__name, self._nosep)
        newone.__dict__.update(self.__dict__)
        return newone

    def add(self, item):
        """
            В конструкцию невозможно добавлять другие конструкции
        """
        pass

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        if self._nosep:
            return ''
        else:
            return ';'


class Comment(Construct):
    """
        Класс для описания комментария
    """
    def __init__(self, name = ''):
        """
        """
        self.vars = {}
        self._name = name
        self.definition = '//\n// ' + self._name
        self.definition = self.definition.strip()
        self.body = ''
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._name)
        newone.__dict__.update(self.__dict__)
        return newone

    def add(self, item):
        pass

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return '\n//'


class Define(Macros):
    """
        Класс для описания #define
    """
    def __init__(self, name = '', _name = ''):
        """
        """
        self._name = name
        self.__name = _name
        if _name == '':
            self.definition = '#define ' + self._name
        else:
            self.definition = '#define ' + self._name + ' ' + self.__name
        self.definition = self.definition.strip()
        self.body = ''
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._name, self.__name)
        newone.__dict__.update(self.__dict__)
        return newone

class Ifdef(Macros):
    """
        Класс для описания #ifdef
    """
    def __init__(self, name = '', negative = False):
        """
        """
        self._name = name
        self._negative = negative
        self.definition = '#ifdef '*(not negative) + '#ifndef '*negative + self._name
        self.definition = self.definition.strip()
        self.body = ''
        self._else = False
        self.elses = []
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._name, self._negative)
        newone.__dict__.update(self.__dict__)
        return newone

    def add(self, item):
        """
            Добавление конструкции внутрь данной конструкции
        """
        item = copy(item)
        if not item in self.detailes:
            self.detailes.append(item)

    def _getBody(self):
        """
        """
        body = ''
        for item in self.detailes:
            body += '\n' + "\n".join(item.__str__().split('\n'))
        if self.elses != []:
            body += '\n#else'
            for item in self.elses:
                body += '\n' + "\n".join(item.__str__().split('\n'))
        return body

    def addElse(self, item = ''):
        """
            Добавление ветки Else
        """
        if not self._else:
            if not item in self.elses:
                self.elses.append(item)
            self._else = True

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return '\n#endif' + (' // ' + self._name)*self._negative

class Include(Macros):
    """
        Класс для описания #include
    """
    def __init__(self, name = ''):
        """
        """
        self._name = name
        self.definition = '#include ' + self._name
        self.definition = self.definition.strip()
        self.body = ''
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._name)
        newone.__dict__.update(self.__dict__)
        return newone

class Pragma(Macros):
    """
        Класс для описания #pragma
    """
    def __init__(self, name = '', _name = ''):
        """
        """
        self._name = name
        self.__name = _name
        self.definition = '#pragma ' + self._name + ' ' + self.__name
        self.definition = self.definition.strip()
        self.body = ''
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._name, self.__name)
        newone.__dict__.update(self.__dict__)
        return newone

class If(Construct):
    """
        Класс для описания условной конструкции If-Else
    """
    def __init__(self, arg1, cond = '', arg2 = ''):
        """
        """
        self._arg1 = arg1
        self._cond = cond
        self._arg2 = arg2
        self.vars = {}
        self._else = False
        if cond:
            cond = ' ' + cond
        if arg2:
            arg2 = ' ' + arg2
        self.definition = 'if (' + str(self._arg1) + ' ' + str(self._cond) + ' ' + str(self._arg2)
        self.definition = self.definition.strip(' ')
        self.definition += ') {'
        self.needBrace = True
        self.needEndBrace = True
        self.detailes = []
        self.elses = []
        self.elseIfs = []
        self.needReturn = False

    def __copy__(self):
        """
        """
        newone = type(self)(self._arg1, self._cond, self._arg2)
        newone.__dict__.update(self.__dict__)
        return newone

    def changeCond(self, arg1, cond = '', arg2 = ''):
        """
        """
        if cond:
            cond = ' ' + cond
        if arg2:
            arg2 = ' ' + arg2
        self.definition = 'if (' + arg1 + cond + arg2 + ') {'

    def _getBody(self):
        """
        """
        needBrace = self.needBrace
        needEndBrace = self.needEndBrace
        body = ''
        for item in self.detailes:
            body += '\n\t' + "\n\t".join(item.__str__().split('\n'))
        for item in self.elseIfs:
            body += '\n'
            if needBrace:
                body += '} '
                needBrace = False
            body += 'else '
            needEndBrace = False
            body += '\n\t' + "\n\t".join(item.__str__().split('\n'))
        if self.elses != []:
            body += '\n'
            if needBrace:
                body += '} '
                needBrace = False
            body += 'else {'
            needEndBrace = True
            for item in self.elses:
                body += '\n\t' + "\n\t".join(item.__str__().split('\n'))
        return body

    def addElse(self, item = ''):
        """
            Добавление ветки Else
        """
        if not item in self.elses:
            self.elses.append(item)

    def addElseIf(self, item = ''):
        """
            Добавление ветки Else IF
        """
        if type(item) != If:
            raise Exception('Item isn\'t instance of the class If')
        if not item in self.elseIfs:
            self.elseIfs.append(item)

    def addReturn(self):
        """
        """
        self.needReturn = True

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        if self.needEndBrace:
            return '\n\treturn;'*self.needReturn + '\n}'
        return ''


class For(Construct):
    """
        Класс для описания цикла For
    """
    def __init__(self, expression1 = '', expression2 = '', expression3 = ''):
        """
        """
        self._expression1 = expression1
        self._expression2 = expression2
        self._expression3 = expression3
        self.vars = {}
        self.definition = 'for (' + self._expression1 + '; ' + self._expression2 + '; ' + self._expression3 + ') {'
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._expression1, self._expression2, self._expression3)
        newone.__dict__.update(self.__dict__)
        return newone


class While(Construct):
    """
        Класс для описания цикла While
    """
    def __init__(self, expression = ''):
        """
        """
        self._expression = expression
        self.vars = {}
        self.definition = 'while (' + self._expression + ') {'
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._expression)
        newone.__dict__.update(self.__dict__)
        return newone


class DoWhile(Construct):
    """
        Класс для описания цикла Do-While
    """
    def __init__(self, expression = ''):
        """
        """
        self.vars = {}
        self._expression = expression
        self.definition = 'do {'
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._expression)
        newone.__dict__.update(self.__dict__)
        return newone

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return '\n} while (' + self._expression + ');'


class Switch(Construct):
    """
        Класс для описания конструкции Switch
    """
    def __init__(self, arg):
        """
        """
        self._arg = arg
        self.names = []
        self.vars = {}
        self._default = ''
        self.definition = 'switch (' + self._arg + ') {'
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._arg)
        newone.__dict__.update(self.__dict__)
        return newone

    def add(self, arg, item = ''):
        """
            Переопределенный метод для иного добавления подконструкции
        """
        item = copy(item)
        if not arg in self.names:
            self.detailes.append([arg, item])
            self.names.append(arg)

    def _getBody(self):
        """
        """
        body = ''
        for item in self.detailes:
            body += '\n\tcase ' + item[0] + ':'
            body += '\n\t\t' + "\n\t\t".join(item[1].__str__().split('\n'))# + ';'
            body += '\n\t\tbreak;'
        body += self._default
        return body

    def addDefault(self, item = ''):
        """
            Добавление блока default
        """
        if self._default != '':
            return
        self._default = '\n\tdefault:'
        self._default += '\n\t\t' + "\n\t\t".join(item.__str__().split('\n'))


class Call(Construct):
    """
        Класс для описания вызовов функций и процедур
    """
    def __init__(self, name = 'main', argv = ['void']):
        """
        """
        self.vars = {}
        self._name = name
        self._argv = argv
        self.definition = name + '(' + ', '.join(str(x) for x in argv) + ')'
        self.detailes = []

    def __copy__(self):
        """
        """
        newone = type(self)(self._name, self._argv)
        newone.__dict__.update(self.__dict__)
        return newone

    def _end(self):
        """
            Конструкция не требует завершения
        """
        return ''


class Union(Construct):
    """
    """
    def __init__(self, item = ''):
        """
        """
        self.vars = {}
        self._item = item
        self.definition = ''
        self.detailes = [self._item]

    def __copy__(self):
        """
        """
        newone = type(self)(self._item)
        newone.__dict__.update(self.__dict__)
        return newone

    def add(self, item):
        """
            Переопределенный метод для иного добавления подконструкции
        """
        item = copy(item)
        self.detailes.append(item)

    def _getBody(self):
        """
        """
        body = ''
        for item in self.detailes:
            if body != '':
                body += '\n'
            body += str(item)
        return body

    def _end(self):
        """
            Конструкция не требует завершения
        """
        return ''
