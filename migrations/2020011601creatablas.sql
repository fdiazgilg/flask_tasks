BEGIN TRANSACTION;

CREATE TABLE "tareas1" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"titulo"	TEXT NOT NULL,
	"descripcion"	TEXT,
	"fecha"	TEXT NOT NULL,
	"id_empleado"	INTEGER,
	FOREIGN KEY("id_empleado") REFERENCES "empleados"("id")
);

INSERT INTO "tareas1" (titulo, descripcion, fecha) SELECT tareas.titulo, tareas.descripcion, tareas.fecha FROM tareas;

DROP TABLE "tareas";

ALTER TABLE "tareas1" RENAME TO "tareas";

COMMIT;
