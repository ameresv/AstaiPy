--  Created with Kata Kuntur - Data Modeller
--  Version: 2.9.1
--  Web Site: http://katakuntur.jeanmazuelos.com/
--  If you find a bug, please report it at:
--  http://pm.jeanmazuelos.com/katakuntur/issues/new
--  Database Management System: SQLite
--  Diagram: Astai
--  Author: Juan Mansilla
--  Date and time: 02/05/2020 16:26:10
PRAGMA foreign_keys = ON;

-- GENERATING TABLES
CREATE TABLE 'Project' (
	'Id_prj' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	'Project' TEXT NULL,
	'Create_prj' TEXT NULL,
	'Modified' TEXT NULL
);

CREATE TABLE 'Scenarios' (
	'Project' TEXT NOT NULL,
	'CountScenario' INTEGER NULL,
	'Project_Scn' TEXT NULL,
	'Commet_Project' TEXT NOT NULL,
	'Project_Folder' TEXT NULL,
	'Project_Id_prj' INTEGER NOT NULL,
	FOREIGN KEY ('Project_Id_prj') REFERENCES Project('Id_prj'),
	PRIMARY KEY('Project')
);

CREATE TABLE Routes (
	Project_Scn TEXT NOT NULL,
	InputMode INTEGER NULL,
	Path_routes TEXT NOT NULL,
	Scenarios_Project TEXT NOT NULL,
	FOREIGN KEY (Scenarios_Project) REFERENCES Scenarios(Project),
	PRIMARY KEY(Project_Scn)
);

CREATE TABLE Geometry (
	Project_Scn TEXT NOT NULL,
	X REAL NULL,
	Y REAL NULL,
	Z REAL NULL,
	Layer TEXT NULL,
	Atrib TEXT NULL,
	Count_Line INTEGER NULL,
	Element_type TEXT NULL,
	Periodo INTEGER NULL,
	Scenarios_Project TEXT NOT NULL,
	FOREIGN KEY (Scenarios_Project) REFERENCES Scenarios(Project),
	PRIMARY KEY(Project_Scn)
);

CREATE TABLE Noude_routes (
	Project_Scn TEXT NOT NULL,
	ID_PL INTEGER NULL,
	Nodo_PI INTEGER NULL,
	Nodo_PF INTEGER NULL,
	PI_X REAL NULL,
	PI_Y REAL NULL,
	PI_Z REAL NULL,
	PF_X REAL NULL,
	PF_Y REAL NULL,
	PF_Z REAL NULL,
	PRIMARY KEY(Project_Scn)
);

CREATE TABLE Compact_routes (
	Project_Scn TEXT NOT NULL,
	ID_PL INTEGER NULL,
	Dist REAL NULL,
	Pend REAL NULL,
	PRIMARY KEY(Project_Scn)
);

CREATE TABLE Project_Setup (
	Project_SCN TEXT NOT NULL,
	Fleet_Loader TEXT NULL,
	Num_Loader INTEGER NULL,
	Fleet_Truck TEXT NULL,
	Num_Truck INTEGER NULL,
	Other TEXT NOT NULL,
	Numb_Other INTEGER NOT NULL,
	Scenarios_Project TEXT NOT NULL,
	FOREIGN KEY (Scenarios_Project) REFERENCES Scenarios(Project),
	PRIMARY KEY(Project_SCN)
);

CREATE TABLE Date_Project (
	Project TEXT NOT NULL,
	Periodos TEXT NULL,
	Cnt_Periodo INTEGER NOT NULL,
	Start REAL NULL,
End REAL NOT NULL,
PRIMARY KEY(Project)
);

CREATE TABLE Loader (
	Fleet_Loader TEXT NOT NULL,
	Description TEXT NOT NULL,
	Dump_Time REAL NULL,
	Load_Time REAL NULL,
	Spot_Time REAL NULL,
	Wait_Time REAL NULL,
	Project_Setup_Project_SCN TEXT NOT NULL,
	FOREIGN KEY (Project_Setup_Project_SCN) REFERENCES Project_Setup(Project_SCN),
	PRIMARY KEY(Fleet_Loader)
);

CREATE TABLE Hauler (
	Fleet_Truck TEXT NOT NULL,
	PayLoad REAL NULL,
	Max_Speed REAL NULL,
	Table_Speed INTEGER NULL,
	Numb_Clases INTEGER NULL,
	Project_Setup_Project_SCN TEXT NOT NULL,
	FOREIGN KEY (Project_Setup_Project_SCN) REFERENCES Project_Setup(Project_SCN),
	PRIMARY KEY(Fleet_Truck)
);

CREATE TABLE Tablet_Speed (
	ID_Table INTEGER NOT NULL,
	Segment REAL NULL,
	Value REAL NULL,
	Hauler_Fleet_Truck TEXT NOT NULL,
	FOREIGN KEY (Hauler_Fleet_Truck) REFERENCES Hauler(Fleet_Truck),
	PRIMARY KEY(ID_Table)
);