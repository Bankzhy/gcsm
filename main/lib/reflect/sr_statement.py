import copy
import uuid

from lib.reflect.sr_core import SRCore


class SRStatement(SRCore):
    def __init__(self, id, word_list=[], type=None, ):
        self.word_list = word_list
        self.id = id
        self.type = type
        self.block_depth = -1
        self.sid = 0
        self.sn = 0

    def get_loc_var_list(self):
        loc_var_list = []
        special_char = [']', '+', "-", "!", "*", "/", ")"]
        for index, word in enumerate(self.word_list):
            if word == "=":
                if self.word_list[index - 1] in special_char:
                    break
                loc_var_list.append(self.word_list[index - 1])
                break
        return loc_var_list

    def replace_param(self, new_param, old_param):

        for i in range(0, len(self.word_list)):
            if self.word_list[i] == old_param:
                self.word_list[i] = new_param

    def replace_return(self, l_s):
        # print(self.word_list)
        if len(self.word_list) > 0:
            if self.word_list[0] == "return":
                self.word_list.pop(0)
                self.word_list.insert(0, "=")
                if l_s is None:
                    return
                if l_s[len(l_s) - 1] != "]":
                    self.word_list.insert(0, l_s[len(l_s) - 1])
                else:
                    for w in reversed(l_s):
                        self.word_list.insert(0, w)

                # if len(l_s) == 1:
                #     self.word_list.insert(0, l_s[0])
                # elif len(l_s) == 2:
                #     self.word_list.insert(0, l_s[1])

    def get_statement_string(self):
        return ' '.join(self.word_list)

    def to_string(self, space=1):
        result = ""
        # print(self.id)
        # print(self.word_list)
        result += " ".join(self.word_list)
        return result

    def to_node_string(self):
        result = ""
        result += " ".join(self.word_list)
        return result

    def to_node_word_list(self):
        return self.word_list

    def get_copy(self):
        return copy.deepcopy(self)

    def find_keyword(self, keyword):
        for word in self.word_list:
            if keyword == word:
                return True
        return False


class SRIFStatement(SRStatement):

    def __init__(self, id, word_list=[], pos_statement_list=[], neg_statement_list=[], condition=[]):
        self.word_list = word_list
        self.condition = condition
        self.pos_statement_list = pos_statement_list
        self.neg_statement_list = neg_statement_list
        self.id = id
        self.block_depth = -1
        self.sid = 0

    def replace_param(self, new_param, old_param):
        super(SRIFStatement, self).replace_param(new_param=new_param, old_param=old_param)
        # print(self.condition)
        for i in range(0, len(self.condition)):
            if self.condition[i] == old_param:
                self.condition[i] = new_param

    def to_string(self, space=1):
        result = ""
        result += "if"
        # result += "("

        if len(self.condition) > 0:
            result += " ".join(self.condition)
        # result += ")"

        if len(self.pos_statement_list) > 0:
            result += "{"
            result += "\n"
            space += 1
            for statement in self.pos_statement_list:
                for x in range(0, space):
                    result += "    "
                result += statement.to_string(space=space)
                result += "\n"
            for x in range(0, space - 1):
                result += "    "
            result += "}"

        if len(self.neg_statement_list) > 0:
            result += "else"
            result += "{"
            result += "\n"
            for statement in self.neg_statement_list:
                for x in range(0, space):
                    result += "    "
                result += statement.to_string(space=space)
                result += "\n"
            for x in range(0, space - 1):
                result += "    "
            result += "}"
        return result

    def to_node_string(self):
        result = ""
        result += "if"
        # result += "("

        if len(self.condition) > 0:
            result += " ".join(self.condition)
        return result

    def to_node_word_list(self):
        word_list = []
        word_list.append("if")
        if len(self.condition) > 0:
            word_list.extend(self.condition)
        return word_list


class SRFORStatement(SRStatement):
    def __init__(self,
                 id="-1", word_list=[], child_statement_list=[], init=[], end_condition=[], update=[]):
        self.word_list = word_list
        self.init = init
        self.end_condition = end_condition
        self.update = update
        self.child_statement_list = child_statement_list
        self.id = id
        self.sid = 0
        self.block_depth = -1

    def replace_param(self, new_param, old_param):
        super(SRFORStatement, self).replace_param(new_param=new_param, old_param=old_param)
        for i in range(0, len(self.end_condition)):
            if self.end_condition[i] == old_param:
                self.end_condition[i] = new_param
        for i in range(0, len(self.init)):
            if self.init[i] == old_param:
                self.init[i] = new_param
        for i in range(0, len(self.update)):
            if self.update[i] == old_param:
                self.update[i] = new_param

    def to_string(self, space=1):
        result = ""
        result += "for"
        result += " ("
        result += " ".join(self.init)
        # result += ";"
        result += " ".join(self.end_condition)
        result += ";"
        result += " ".join(self.update)
        result += " ) "
        result += "{"
        result += "\n"

        space += 1
        for st in self.child_statement_list:
            for x in range(0, space):
                result += "    "
            result += st.to_string(space=space)
            result += "\n"

        for x in range(0, space - 1):
            result += "    "
        result += "}"
        return result

    def to_node_string(self):
        result = ""
        result += "for"
        result += " ("
        result += " ".join(self.init)
        # result += ";"
        result += " ".join(self.end_condition)
        result += ";"
        result += " ".join(self.update)
        result += " ) "
        return result

    def to_node_word_list(self):
        word_list = []
        word_list.append("for")
        word_list.append("(")
        word_list.extend(self.init)
        word_list.extend(self.end_condition)
        word_list.append(";")
        word_list.extend(self.update)
        word_list.append(")")
        return word_list

    def get_copy(self):
        return copy.deepcopy(self)


class SRWhileStatement(SRStatement):

    def __init__(self, id, word_list=[], child_statement_list=[], end_condition=[]):
        self.word_list = word_list
        self.end_condition = end_condition
        self.child_statement_list = child_statement_list
        self.id = id
        self.sid = 0
        self.block_depth = -1

    def replace_param(self, new_param, old_param):
        super(SRWhileStatement, self).replace_param(new_param=new_param, old_param=old_param)
        for i in range(0, len(self.end_condition)):
            if self.end_condition[i] == old_param:
                self.end_condition[i] = new_param

    def to_string(self, space=1):
        result = ""
        result += "while"
        result += " ("
        result += " ".join(self.end_condition)
        result += " )"
        result += " {"
        result += "\n"

        space += 1
        for st in self.child_statement_list:
            for x in range(0, space):
                result += "    "
            result += st.to_string(space=space)
            result += "\n"

        for x in range(0, space - 1):
            result += "    "
        result += "}"
        return result

    def to_node_string(self):
        result = ""
        result += "while"
        result += " ("
        result += " ".join(self.end_condition)
        result += " )"
        return result

    def to_node_word_list(self):
        word_list = []
        word_list.append("while")
        word_list.append("(")
        word_list.extend(self.end_condition)
        word_list.append(")")
        return word_list


class SRTRYStatement(SRStatement):

    def __init__(self, word_list=[], id="-1", try_statement_list=[],
                 catch_block_list=[], final_block_statement_list=[]):
        self.word_list = word_list
        self.id = id
        self.sid = 0
        self.try_statement_list = try_statement_list,
        self.catch_block_list = catch_block_list,
        self.final_block_statement_list = final_block_statement_list
        self.block_depth = -1

    def to_string(self, space=1):
        result = ""
        result += "try"
        result += " {"
        result += "\n"
        space += 1

        for st in self.try_statement_list:
            print(st.to_string())
            for x in range(0, space):
                result += "    "
            result += st.to_string(space=space)
            result += "\n"

        for x in range(0, space - 1):
            result += "    "
        result += "} "

        for cb in self.catch_block_list:
            result += cb.to_string(space=space - 1)

        result += "finally"
        result += " {"
        result += "\n"

        for st in self.final_block_statement_list:
            for x in range(0, space):
                result += "    "
            result += st.to_string(space=space)
            result += "\n"

        for x in range(0, space - 1):
            result += "    "
        result += "} "
        return result

    def to_node_string(self):
        result = ""
        result += "try"
        return result

    def to_node_word_list(self):
        word_list = []
        word_list.append("try-catch: hasError?")
        return word_list


class CatchBlock(SRStatement):

    def __init__(self, word_list=[], child_statement_list=[], catch_param=[]):
        self.word_list = word_list
        self.child_statement_list = child_statement_list
        self.catch_param = catch_param

    def to_string(self, space=1):
        result = ""
        result += "catch"
        result += "( "
        result += "".join(self.catch_param)
        result += " )"
        result += " {"
        result += "\n"

        space += 1
        for st in self.child_statement_list:
            for x in range(0, space):
                result += "    "
            result += st.to_string(space=space)
            result += "\n"

        for x in range(0, space - 1):
            result += "    "
        result += "} "
        return result

    def to_node_string(self):
        result = ""
        result += "catch"
        result += "( "
        result += "".join(self.catch_param)
        result += " )"
        return result

    def to_if_st_expression(self):
        if len(self.child_statement_list) == 0:
            wl = ['System', '.', 'out', '.', 'println', '(', '1', ')', ';']
            fake_st = SRStatement(
                word_list=wl,
                id=uuid.uuid1().hex
            )
            self.child_statement_list.append(fake_st)
        new_st = SRIFStatement(
            id=uuid.uuid1().hex,
            word_list=self.word_list,
            pos_statement_list=self.child_statement_list,
            neg_statement_list=[],
            condition=self.catch_param)
        return new_st
