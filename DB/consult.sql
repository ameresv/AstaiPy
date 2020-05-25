CREATE TABLE Projects (
  ID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
  Project TEXT UNIQUE,
  Created TEXT NOT NULL,
  User INTEGER NOT NULL,
  Modified INTEGER,
  FOREIGN KEY (User) REFERENCES Users (Id)
);
CREATE TABLE "Users" (
  "Id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
  "User" TEXT NOT NULL
);
INSERT INTO Projects (Project, Created, User)
VALUES
  ('asd', '2000', 2);
-- Devuelve la fecha de creaccion de datatable
SELECT
  strftime('%d-%m-%Y', datetime('now')) as Today;
--Revisar si una tabla existe
SELECT
  name
FROM sqlite_master
WHERE
  type = 'table'
  AND name = 'Geometry';
SELECT
  EXISTS(
    SELECT
      1
    FROM Geometry
    WHERE
      File = ?
      AND Project = ?
      AND Element_Type = ?
    LIMIT
      1
  );
CREATE TABLE "Nodes_route" (
    "ID_PL" INTEGER NOT NULL UNIQUE,
    "PI_X" REAL NOT NULL,
    "PI_Y" INTEGER NOT NULL,
    "PI_Z" REAL NOT NULL,
    "Nodo_PI" INTEGER NOT NULL,
    "PF_X" REAL NOT NULL,
    "PF_Y" REAL NOT NULL,
    "PF_Z" REAL NOT NULL,
    "Nodo_PF" INTEGER NOT NULL,
    PRIMARY KEY("ID_PL"),
  );
CREATE TABLE "Geometry" (
    "X" REAL NOT NULL,
    "Y" REAL NOT NULL,
    "Z" NUMERIC NOT NULL,
    "File" TEXT NOT NULL,
    "Layer" TEXT NOT NULL,
    "Atrib" TEXT,
    "IDx" INTEGER NOT NULL,
    "Element_type" TEXT,
    "Project" TEXT,
    "Period" INTEGER,
    FOREIGN KEY("Project") REFERENCES "Projects"("Project")
  );
CREATE VIEW Prueba1 As
SELECT
  IDx,
  X,
  lag(X, -1, 0) OVER(
    ORDER by
      IDx
  ) Xp,
  Y,
  lag(Y, -1, 0) OVER(
    ORDER by
      IDx
  ) Yp,
  Z,
  lag(Z, -1, 0) OVER(
    ORDER by
      IDx
  ) Zp,
  Layer,
  Element_type,
  Atrib,
  Project
FROM Geometry;
SELECT
  IDx,
  (
    (X - Xp) *(X - Xp) + (Y - Yp) *(Y - Yp) +(Z - Zp) *(Z - Zp)
  ) as Dif_Long,
  ((X - Xp) *(X - Xp) + (Y - Yp) *(Y - Yp)) as Dif_Pend,
  (Z - Zp) as Dif_Cota,
  Layer,
  Atrib
FROM Prueba1
WHERE
  Element_type = 'PolyLine'
  AND Project = 'Test_1'
SELECT
  IDx,
  X,
  lag(X, -1, 0) OVER(
    ORDER by
      IDx
  ) Xp,
  Layer,
  Element_type,
  Atrib
FROM Geometry
WHERE
  Element_type = 'PolyLine'