import random


class Horario:
    slots = 4
    disciplinas = dict()
    inc_t = dict()

    @staticmethod
    def init_disc():
        Horario.disciplinas[1] = {1, 2, 3, 4, 5}
        Horario.disciplinas[2] = {6, 7, 8, 9}
        Horario.disciplinas[3] = {10, 11, 12}
        Horario.disciplinas[4] = {1, 2, 3, 4}
        Horario.disciplinas[5] = {5, 6, 7, 8}
        Horario.disciplinas[6] = {9, 10, 11, 12}
        Horario.disciplinas[7] = {1, 2, 3, 5}
        Horario.disciplinas[8] = {6, 7, 8}
        Horario.disciplinas[9] = {4, 9, 10, 11, 12}
        Horario.disciplinas[10] = {1, 2, 4, 5}
        Horario.disciplinas[11] = {3, 6, 7, 8}
        Horario.disciplinas[12] = {9, 10, 11, 12}
        Horario.inc_table()

    @staticmethod
    def gen_solution():
        dis = Horario.disciplinas.keys()
        sol = []
        for i in dis:
            s = random.randint(1, Horario.slots)
            sol.append(s)
        return sol

    @staticmethod
    def inc_table():
        for i in Horario.disciplinas.keys():
            s = dict()
            for j in Horario.disciplinas.keys():
                s[j] = Horario.inc(i, j)
            Horario.inc_t[i] = s

    @staticmethod
    def inc(D1, D2):
        return len(Horario.disciplinas[D1].intersection(
            Horario.disciplinas[D2]))

    @staticmethod
    def val(sol):
        s = dict()
        for i in range(Horario.slots):
            s[i+1] = []
        for i, j in enumerate(sol):
            s[j].append(i)
        val = 0
        for i in s.keys():
            for j in s[i]:
                val += Horario.inc_t[i][j]
        return -val


Horario.init_disc()
