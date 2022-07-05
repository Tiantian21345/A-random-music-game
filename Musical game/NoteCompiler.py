from os import listdir

Inputs = "Sheets"
Outputs = "MachineNotes"


def where_next_non_float(string, start):  # return index of nonint #alpha+int,int
    i = start + 1  # skip first alpha
    if len(string) == i: return -1  # name only case
    while string[i].isdigit() or string[i] == '.' or string[i] == '-' or string[i] == '/':
        # after this, i is the index of non-interger #if digit
        if i == len(string) - 1:  # if checking last string #
            return -1
        i += 1
    return i


def where_correspond_bracket(string, start):  # full: "[...]"
    pointer = start  # [[...]...]
    i = 1  # [ is positive, ] is negative
    while i > 0:
        pointer += 1  # skip the [
        try:
            if string[pointer] == '[':
                i += 1
            elif string[pointer] == ']':
                i -= 1  # end when pointer at ] that reduce to 0
        except IndexError:
            return -1
    return pointer


def where_correspond_curly(string, start):  #
    pointer = start  # [[...]...]
    i = 1  # [ is positive, ] is negative
    while i > 0:
        pointer += 1  # skip the [
        try:
            if string[pointer] == '(':
                i += 1
            elif string[pointer] == ')':
                i -= 1  # end when pointer at ] that reduce to 0
        except IndexError:
            return -1
    return pointer


def extractor(string):  # function #1
    """
    '`' - Multiplies the amount of times the letter(s) after it in 'notes'
            by the int directly after it (if no int is provided, it defaults to 2)
    '-' - Sets the amount of delay after the group directly in front of it
            by the int directly after it (if no int is provided, it defaults to 0)
    '[...]' - Makes the contained contents treated as one letter
    """
    notes = []
    pointer = 0

    def stringformat(string_part):  # [name,duration,dash,reduction]
        for i, e in enumerate(string_part):
            if e == '-':
                if string_part[1:i] == '':  # if no duration and yes '-' a-?
                    if string_part[i + 1:] == '':  # a-
                        return string_part[0] + '1-0'
                    return string_part[0] + '1' + string_part[i:]  # a-N
                elif string_part[i + 1:] == '':  # if yes duration and no reduction aN-
                    return string_part[0:i + 1] + '0'
                return string_part  # yes duration and yes reduction
        if len(string_part) == 1:
            return string_part + '1-1'  # when no - and no duration a
        else:
            return string_part[0:] + '-' + string_part[1:]  # when no- and yes duration aN

    def alpha_case():  # pointer must be at alpha
        nonlocal pointer, notes, next_alpha
        next_alpha = where_next_non_float(string, pointer)
        if next_alpha == -1:
            notes.append(stringformat(string[pointer:]))
            pointer = len(string)  # for exit
        else:
            notes.append(stringformat(string[pointer:next_alpha]))
            pointer = next_alpha  # pointer is after the note

    while pointer < len(string):
        if string[pointer] == '[':  # [notes]scalar
            corresponding_bracket = where_correspond_bracket(string, pointer)
            next_alpha = where_next_non_float(string, corresponding_bracket)  # end of scalar
            if next_alpha == -1:  # scalar is full
                if string[corresponding_bracket + 1:] == '':
                    scalar = 1
                else:
                    scalar = float(string[corresponding_bracket + 1:])
            else:
                if string[corresponding_bracket + 1:next_alpha] == '':
                    scalar = 1
                else:
                    scalar = float(string[corresponding_bracket + 1:next_alpha])

            for a in extractor(string[pointer + 1: corresponding_bracket]):  # for notes in the bracket
                a_duration = a[1:a.find('-')]
                notes.append(a.replace(str(a_duration), str(float(a_duration) * scalar)))
            if next_alpha == -1:
                break
            else:
                pointer = next_alpha  # now pointer is a the character after the scalar
        elif string[pointer] == '(':
            pointer = where_correspond_curly(string, pointer) + 1
        elif string[pointer] == ';':  # ;multi note , ;multi[notes]
            next_alpha = where_next_non_float(string, pointer)
            if string[pointer + 1:next_alpha].isdigit():
                multiplier = int(string[pointer + 1:next_alpha])
            else:
                multiplier = 2  # if no number, =2
            if string[next_alpha].isalpha():  # if case 1
                for a in range(multiplier):  # repeat by the multiplier
                    pointer = next_alpha  # pointer = first
                    alpha_case()
            else:  # then next_alpha is [  case 2
                closing_bracket = where_correspond_bracket(string, next_alpha)
                for a in range(multiplier):  # repeat by the multiplier
                    notes.extend(extractor(string[next_alpha + 1:closing_bracket]))
                pointer = closing_bracket + 1
        elif string[pointer].isalpha() or string[pointer] == " ":  # note+notedata(*duration,*reduction)
            alpha_case()
    return notes  # plugged in to 2nd function for the real notes which is in the test.py file


# print(extractor(''))
# 'aa1a-a1-a-1;a;a1;a-;a1-;a-1;[a]2;[a-]2;[a1]2;[a1-]2;[a1-1]2;[[q-i-r-o-t-p].5i s].5'
for file in listdir(Inputs):
    with open(Inputs + '/' + file) as f:
        lines = f.read().replace('\n', '')  # remove \n
        with open(Outputs + '/' + file, mode='w') as f:
            f.write(str(extractor(lines)))
print('Ended')
