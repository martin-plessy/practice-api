DROP TABLE IF EXISTS employee_type;

CREATE TABLE employee_type (
	uid  INTEGER     PRIMARY KEY,

	type VARCHAR(50) UNIQUE NOT NULL
);
