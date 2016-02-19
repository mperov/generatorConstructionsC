#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        if not item._name in self.names:
            self.detailes.append(item)
            self.names.append(item._name)

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
        freeVar = ''
        variables = ''
        body = self._getBody()
        if len(self.vars) > 0:
            for i in self.vars:
                if self.vars[i][2] != '': # требуется освобождение
                    freeVar += '\n\t' + "\n\t".join([ self.vars[i][2] + '( ' + i + ' );' ])
                initVar = ''
                if self.vars[i][1] != '': # требуется инициализация
                    initVar = ' = ' + self.vars[i][1]
                variables += '\n\t' + "\n\t".join([ self.vars[i][0] + ' ' + i + initVar + ';' ])
        return self.definition + variables + body + freeVar + self._end()

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

    def addVar(self, typeVar, nameVar, initVar = 'tcg_temp_new()', freeVar = 'tcg_temp_free'):
        """
        """
        if self._conditionTCG and initVar == 'tcg_temp_new()':
            initVar = 'tcg_temp_local_new()'
        self.vars.update({nameVar : [typeVar, initVar, freeVar]})

    def startConditionTCG(self):
        """
        """
        self._conditionTCG = True

    def endConditionTCG(self):
        """
        """
        self._conditionTCG = False

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
        self.names = []
        self.vars = {}
        self.definition = ''
        self.body = ''
        self.detailes = []

    def add(self, item):
        """
            Переопределенный метод для иного добавления подконструкций
        """
        if not item._name in self.names:
            self.detailes.append(item)
            self.names.append(item._name)

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
        self.names = []
        self.vars = {}
        self._conditionTCG = False
        self._name = name
        self.definition = type + ' ' + name + '(' + ', '.join(argv) + ') {'
        self.body = ''
        self.detailes = []

    def changeDefinition(self, type = 'void', name = 'main', argv = ['void']):
        """
        """
        self.definition = type + ' ' + name + '(' + ', '.join(argv) + ') {'


class Struct(Construct):
    """
        Класс для описания структур
    """
    def __init__(self, name, declaretion = True):
        """
        """
        self.names = []
        self.vars = {}
        self._name = name
        self.declaretion = declaretion
        self.definition = 'struct ' + self._name + ' {'
        self.body = ''
        self.detailes = []

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return '\n}' + (' ' + self._name)*self.declaretion + ';'


class Line(Construct):
    """
        Класс для описания строки
    """
    def __init__(self, type = '', name = '', operator = '', _name = '', nosep = False):
        """
        """
        self.names = []
        self.vars = {}
        self.definition = type + ' ' + name + ' ' + operator + ' ' + _name
        self._name = self.definition
        self.definition = self.definition.strip(' ')
        self.body = ''
        self.detailes = []
        self.nosep = nosep

    def add(self, item):
        """
            В конструкцию невозможно добавлять другие конструкции
        """
        pass

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        if self.nosep:
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
        self.names = []
        self.vars = {}
        self.definition = '//\n// ' + name
        self._name = self.definition
        self.definition = self.definition.strip()
        self.body = ''
        self.detailes = []

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
        self.names = []
        if _name == '':
            self.definition = '#define ' + name
        else:
            self.definition = '#define ' + name + ' ' + _name
        self._name = self.definition
        self.definition = self.definition.strip()
        self.body = ''
        self.detailes = []

class Ifdef(Macros):
    """
        Класс для описания #ifdef
    """
    def __init__(self, name = '', negative = False):
        """
        """
        self.name = name
        self.names = []
        self.definition = '#ifdef '*(not negative) + '#ifndef '*negative + name
        self._name = self.definition
        self.definition = self.definition.strip()
        self.body = ''
        self._else = False
        self.elses = []
        self.detailes = []
        self.negative = negative

    def add(self, item):
        """
            Добавление конструкции внутрь данной конструкции
        """
        if not item._name in self.names:
            self.detailes.append(item)
            self.names.append(item._name)

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
            item._name += ' else'
            if not item._name in self.names:
                self.elses.append(item)
                self.names.append(item._name)
            self._else = True

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return '\n#endif' + (' // ' + self.name)*self.negative

class Include(Macros):
    """
        Класс для описания #include
    """
    def __init__(self, name = ''):
        """
        """
        self.names = []
        self.definition = '#include ' + name
        self._name = self.definition
        self.definition = self.definition.strip()
        self.body = ''
        self.detailes = []

class Pragma(Macros):
    """
        Класс для описания #pragma
    """
    def __init__(self, name = '', _name = ''):
        """
        """
        self.names = []
        self.definition = '#pragma ' + name + ' ' + _name
        self._name = self.definition
        self.definition = self.definition.strip()
        self.body = ''
        self.detailes = []

class If(Construct):
    """
        Класс для описания условной конструкции If-Else
    """
    def __init__(self, arg1, cond = '', arg2 = ''):
        """
        """
        self.names = []
        self.vars = {}
        self._conditionTCG = False
        self._else = False
        if cond:
            cond = ' ' + cond
        if arg2:
            arg2 = ' ' + arg2
        self.definition = 'if (' + str(arg1) + str(cond) + str(arg2) + ') {'
        self._name = self.definition
        self.needBrace = True
        self.needEndBrace = True
        self.detailes = []
        self.elses = []
        self.elseIfs = []
        self.needReturn = False

    def changeCond(self, arg1, cond = '', arg2 = ''):
        """
        """
        if cond:
            cond = ' ' + cond
        if arg2:
            arg2 = ' ' + arg2
        self.definition = 'if (' + arg1 + cond + arg2 + ') {'
        self._name = self.definition

    def _getBody(self):
        """
        """
        body = ''
        for item in self.detailes:
            body += '\n\t' + "\n\t".join(item.__str__().split('\n'))
        if self.elses != []:
            body += '\n'
            if self.needBrace:
                body += '} '
                self.needBrace = False
            body += 'else {'
            self.needEndBrace = True
            for item in self.elses:
                body += '\n\t' + "\n\t".join(item.__str__().split('\n'))
        for item in self.elseIfs:
            body += '\n'
            if self.needBrace:
                body += '} '
                self.needBrace = False
            body += 'else '
            self.needEndBrace = False
            body += '\n\t' + "\n\t".join(item.__str__().split('\n'))
        return body

    def addElse(self, item = ''):
        """
            Добавление ветки Else
        """
        item._name += ' else'
        if not item._name in self.names:
            self.elses.append(item)
            self.names.append(item._name)

    def addElseIf(self, item = ''):
        """
            Добавление ветки Else IF
        """
        item._name += ' else'
        if not item._name in self.names:
            self.elseIfs.append(item)
            self.names.append(item._name)

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
        self.names = []
        self.vars = {}
        self.definition = 'for (' + expression1 + '; ' + expression2 + '; ' + expression3 + ') {'
        self._name = self.definition
        self.detailes = []


class While(Construct):
    """
        Класс для описания цикла While
    """
    def __init__(self, expression = ''):
        """
        """
        self.names = []
        self.vars = {}
        self.definition = 'while (' + expression + ') {'
        self._name = self.definition
        self.detailes = []


class DoWhile(Construct):
    """
        Класс для описания цикла Do-While
    """
    def __init__(self, expression = ''):
        """
        """
        self.names = []
        self.vars = {}
        self.expression = expression
        self.definition = 'do {'
        self._name = self.definition + expression
        self.detailes = []

    def _end(self):
        """
            Переопределенный метод для иного завершения конструкции
        """
        return '\n} while (' + self.expression + ');'


class Switch(Construct):
    """
        Класс для описания конструкции Switch
    """
    def __init__(self, arg):
        """
        """
        self.names = []
        self.vars = {}
        self._default = ''
        self.definition = 'switch (' + arg + ') {'
        self._name = self.definition
        self.detailes = []

    def add(self, arg, item = ''):
        """
            Переопределенный метод для иного добавления подконструкции
        """
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


class Calls(Construct):
    """
        Класс для описания вызовов функций и процедур
    """
    def __init__(self, name = 'main', argv = ['void']):
        """
        """
        self.names = []
        self.vars = {}
        self._name = name
        self.definition = name + '(' + ', '.join(argv) + ')'
        self.detailes = []

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
        self.names = []
        self.vars = {}
        self.definition = ''
        self._name = item
        self.detailes = [item]

    def add(self, item):
        """
            Переопределенный метод для иного добавления подконструкции
        """
        self._name += ';' + str(item)
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
