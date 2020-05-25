import logging as log
import sqlite3


class LoadData:
    def __init__(self, File, Project):
        self.conn = None
        self.data = None
        self.conn = sqlite3.connect('DB\DBAstai.db')
        self.cur = self.conn.cursor()
        self.File = File
        self.Project = Project

    def LoadRoads(self, arra2D):
        # Revisa si existe el objeto Polinea en la base de datos:
        self._CheckExist('PolyLine')
        try:
            query = 'INSERT INTO Geometry (X,Y,Z,File,Layer,Atrib,IDx, Element_type, Project, Period) VALUES (?,?,?,?,?,?,?,?,?,?)'
            self.cur.executemany(query, arra2D)
            self.conn.commit()
        except sqlite3.Error as e:
            log.error(e)
        except Exception as e:
            log.exception(e)
        finally:
            if self.conn:
                log.info('....OK')
                self.conn.close()

    def LoadOrgDest(self, arra2D):
        self._CheckExist('Point')
        try:
            query = 'INSERT INTO Geometry (X,Y,Z,File,Layer,Atrib,IDx, Element_type, Project, Period) VALUES (?,?,?,?,?,?,?,?,?,?)'
            self.cur.executemany(query, arra2D)
            self.conn.commit()
        except sqlite3.Error as e:
            log.error(e)
        except Exception as e:
            log.exception(e)
        finally:
            if self.conn:
                log.info('....OK')
                self.conn.close()

    def LoadCompactRoad(self, arra2D):
        self._CheckExist('Dist')
        try:
            query = 'INSERT INTO Compact_routes (Id_seg,Atrib,Layer,Project,Dist, Pend) VALUES (?,?,?,?,?,?)'
            self.cur.executemany(query, arra2D)
            self.conn.commit()
        except sqlite3.Error as e:
            log.error(e)
        except Exception as e:
            log.exception(e)
        finally:
            if self.conn:
                log.info('....OK')
                self.conn.close()
        pass

    # Revisar si existe un mismo resgistro ID and Project been similar

    def _CheckExist(self, Element_type):
        if Element_type == 'PolyLine' or Element_type == 'Point':
            query = """SELECT EXISTS(SELECT 1 FROM Geometry WHERE File=? AND Project=? AND Element_Type = ? LIMIT 1)"""
            self.cur.execute(query, (self.File, self.Project, Element_type))

            r = self.cur.fetchone()
            if int(r[0]) > 0:
                log.info("-------Existes register---------")
                self._DeleteRegister(Element_type)
            else:
                log.info("-------Load register---------")
        if Element_type == 'Dist':
            query = """SELECT EXISTS(SELECT 1 FROM Compact_routes WHERE Project='Test_1' LIMIT 1)"""
            self.cur.execute(query)
            r = self.cur.fetchone()
            if int(r[0]) > 0:
                log.info("-------Existes register---------")
                self._DeleteRegister(Element_type)
            else:
                log.info("-------Load register---------")
            pass

    def _UpdateRegister(self, Element_type):

        return

    def _DeleteRegister(self, Element_type):
        if Element_type == 'PolyLine' or Element_type == 'Point':
            query = """DELETE FROM Geometry WHERE File=? AND Project=? AND Element_Type = ? """
            self.cur.execute(query, (self.File, self.Project, Element_type))
            self.conn.commit()
            log.info("-------Delete register---------")
        if Element_type == 'Dist':
            query = """DELETE FROM Compact_routes WHERE Project='Test_1'"""
            self.cur.execute(query)
            self.conn.commit()
            log.info("-------Delete register---------")


#query_string = 'INSERT INTO Geometry (X,Y,Z,File,Layer,Atrib,IDx) VALUES (?,?,?,?,?,?,?)'
#g = LoadData()
#g.LoadRoads(query_string, arr)
