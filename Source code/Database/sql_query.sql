CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    begin_date TEXT NOT NULL,
	edited_date TEXT
);

INSERT OR IGNORE INTO projects(name, description, begin_date) VALUES('Train Door Project', 'Test with Train Door project', '2021-02-26')

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_project INTEGER NOT NULL,
	id_goal INTEGER NOT NULL,
    description TEXT NOT NULL,
    begin_date TEXT NOT NULL,
	edited_date TEXT,
	FOREIGN KEY(id_project) REFERENCES projects(id)
);	


CREATE TABLE IF NOT EXISTS assumptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_project INTEGER NOT NULL,
	id_assumption INTEGER NOT NULL,
    description TEXT NOT NULL,
    begin_date TEXT NOT NULL,
	edited_date TEXT,
	FOREIGN KEY(id_project) REFERENCES projects(id)
);

INSERT INTO assumptions (id_project, id_assumption, description, begin_date) VALUES (1, 1, 'Assumption of Train Door', '2021-03-02')

SELECT * FROM assumptions WHERE id_project = 1

drop table goals
drop table projects
INSERT OR IGNORE INTO goals(id_project, id_goal, description, begin_date) VALUES(1, 1, 'Provide an easy way to control the door.', '2021-02-26')

SELECT * FROM goals WHERE id_project = 1 ORDER BY id_goal
SELECT * FROM projects ORDER BY name


CREATE TABLE IF NOT EXISTS losses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_project INTEGER NOT NULL,
	id_loss INTEGER NOT NULL,
    description TEXT NOT NULL,
    begin_date TEXT NOT NULL,
	edited_date TEXT,
	FOREIGN KEY(id_project) REFERENCES projects(id)
);	
INSERT INTO losses(id_project, id_loss, description, begin_date) VALUES(1, 1, 'Injury to a person by falling out of the train.', '2021-02-26')
INSERT INTO losses(id_project, id_loss, description, begin_date) VALUES(1, 2, 'Being hit by a closing door.', '2021-02-26')
INSERT INTO losses(id_project, id_loss, description, begin_date) VALUES(1, 3, 'Being trapped inside a train during an emergency.', '2021-02-26')
drop table Losses
SELECT * FROM losses WHERE id_project = 1 ORDER BY id_loss

CREATE TABLE IF NOT EXISTS hazards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_project INTEGER NOT NULL,
	id_hazard INTEGER NOT NULL,
    description TEXT NOT NULL,
    begin_date TEXT NOT NULL,
	edited_date TEXT,
	FOREIGN KEY(id_project) REFERENCES projects(id)
);	

INSERT INTO hazards(id_project, id_loss, id_hazard, description, begin_date) VALUES(1, 2, 1, 'Door close on a person in the door way.', '2021-02-26')
INSERT INTO hazards(id_project, id_loss, id_hazard, description, begin_date) VALUES(1, 1, 1, 'Door open when the train is moving or not in a station.', '2021-02-26')
INSERT INTO hazards(id_project, id_loss, id_hazard, description, begin_date) VALUES(1, 3, 1, 'Passengers/staff are unable to exit during an emergency.', '2021-02-26')
drop table hazards
SELECT * FROM hazards WHERE id_project = 1 ORDER BY id_hazard
SELECT * FROM hazards WHERE id_project = 1 and id_loss = 2 ORDER BY id_hazard

CREATE TABLE IF NOT EXISTS hazards_losses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_project INTEGER NOT NULL,
	id_hazard INTEGER NOT NULL,
	id_loss INTEGER NOT NULL,
    FOREIGN KEY(id_project) REFERENCES projects(id)
    FOREIGN KEY(id_hazard) REFERENCES hazards(id)
    FOREIGN KEY(id_loss) REFERENCES losses(id)
);


CREATE TABLE IF NOT EXISTS safety_constraints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_project INTEGER NOT NULL,
	id_safety_constraint INTEGER NOT NULL,
    description TEXT NOT NULL,
    begin_date TEXT NOT NULL,
	edited_date TEXT,
	FOREIGN KEY(id_project) REFERENCES projects(id)
);	

CREATE TABLE IF NOT EXISTS safety_constraints_hazards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_project INTEGER NOT NULL,
	id_constraint INTEGER NOT NULL,
	id_hazard INTEGER NOT NULL,
    FOREIGN KEY(id_project) REFERENCES projects(id)
    FOREIGN KEY(id_hazard) REFERENCES hazards(id)
    FOREIGN KEY(id_constraint) REFERENCES safety_constraints(id)
);

DROP TABLE safety_constraints
INSERT INTO safety_constraints(id_project, id_hazard, id_safety_constraint, description, begin_date) VALUES(1, 2, 1, 'Door must not be opened when train is in motion.', '2021-02-26')


SELECT * FROM safety_constraints WHERE id_project = 1 ORDER BY id_safety_constraint
SELECT * FROM safety_constraints WHERE id_project = 1 and id_hazard = 2 ORDER BY id_safety_constraint


SELECT * FROM hazards_losses WHERE id_project = 1 
SELECT * FROM hazards WHERE id_project = 1 ORDER BY id_hazard

DELETE FROM hazards_losses WHERE id_project = 1 AND id_hazard = 1
INSERT INTO hazards_losses(id_project, id_hazard, id_loss) VALUES(?, ?, ?)


SELECT hl.id, hl.id_project, hl.id_hazard, hl.id_loss, l.id_loss FROM hazards_losses AS hl 
	JOIN losses AS l ON l.id = hl.id_loss
	WHERE hl.id_project = 1 AND hl.id_hazard = 15 ORDER BY l.id_loss
SELECT * FROM losses



CREATE TABLE IF NOT EXISTS things (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
	ontology_name TEXT NOT NULL
);	

SELECT * from things
drop table things

INSERT INTO things(id, name, ontology_name) VALUES (1, 'Controller', 'Controller');
INSERT INTO things(id, name, ontology_name) VALUES (2, 'Actuator', 'Actuator');
INSERT INTO things(id, name, ontology_name) VALUES (3, 'Controlled Process', 'CP');
INSERT INTO things(id, name, ontology_name) VALUES (4, 'Sensor', 'Sensor');
INSERT INTO things(id, name, ontology_name) VALUES (5, 'Input', 'Input');
INSERT INTO things(id, name, ontology_name) VALUES (6, 'Output', 'Output');
INSERT INTO things(id, name, ontology_name) VALUES (7, 'External Communication', 'External_communication');
INSERT INTO things(id, name, ontology_name) VALUES (8, 'Algorithm', 'Algorithm');
INSERT INTO things(id, name, ontology_name) VALUES (9, 'Process Model', 'Process_model');
INSERT INTO things(id, name, ontology_name) VALUES (10, 'Environmental Disturbances', 'Environmental_disturbances');
INSERT INTO things(id, name, ontology_name) VALUES (11, 'High_level Controller', 'HLC');

SELECT * FROM things ORDER BY name
SELECT * FROM things WHERE id = 1 ORDER BY name
drop table things

SELECT * FROM variables AS a JOIN components AS c ON a.id_component = c.id WHERE c.id_thing = 4 AND c.id_project = 1
SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date, v.edited_date FROM variables AS v 
	JOIN components AS c ON v.id_component = c.id 
	JOIN actions AS a ON a.source = c.id_thing
		WHERE c.id_project = 1 AND a.name = "Feedback_of_CP"
SELECT * FROM components
SELECT * FROM actions


CREATE TABLE IF NOT EXISTS components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_thing INTEGER NOT NULL,
	id_project INTEGER NOT NULL,
    name TEXT NOT NULL,
    begin_date TEXT NOT NULL,
	edited_date TEXT,
	FOREIGN KEY(id_thing) REFERENCES things(id)
	FOREIGN KEY(id_project) REFERENCES projects(id)
);

drop table components
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(1, 1, 'Train Door Controller', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(2, 1, 'Door Actuator', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(4, 1, 'Door Sensor', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(7, 1, 'External Information', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(3, 1, 'Physical Door', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(5, 1, 'Train Door Input', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(6, 1, 'Train Door Output', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(8, 1, 'Train Door Algorithm', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(9, 1, 'Train Door Process Model', '2021-02-26')
INSERT INTO components(id_thing, id_project, name, begin_date) VALUES(10, 1, 'Train Door Environmental Disturbances', '2021-02-28')

select * from things
SELECT * FROM components

SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date FROM components AS c
	JOIN things AS t ON t.id = c.id_thing
		WHERE t.ontology_name = 'External_communication' AND c.id_project = 1



CREATE TABLE IF NOT EXISTS variables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_component INTEGER NOT NULL,
	id_project INTEGER NOT NULL,
    name TEXT NOT NULL,
    begin_date TEXT NOT NULL,
	edited_date TEXT,
	FOREIGN KEY(id_component) REFERENCES components(id)
	FOREIGN KEY(id_project) REFERENCES projects(id)
);

drop table variables

INSERT INTO variables(id_component, id_project, name, begin_date) VALUES(3, 1, 'Door Position', '2021-02-26')
INSERT INTO variables(id_component, id_project, name, begin_date) VALUES(3, 1, 'Door State', '2021-02-26')
INSERT INTO variables(id_component, id_project, name, begin_date) VALUES(4, 1, 'Train Position', '2021-02-26')
INSERT INTO variables(id_component, id_project, name, begin_date) VALUES(4, 1, 'Train Motion', '2021-02-26')
INSERT INTO variables(id_component, id_project, name, begin_date) VALUES(4, 1, 'Emergency', '2021-02-26')
INSERT INTO variables(id_component, id_project, name, begin_date, edited_date, id_component_link) VALUES(6, 1, 'Input state', '2021-02-26', '2021-02-28', 8)
INSERT INTO variables(id_component, id_project, name, begin_date, edited_date, id_component_link) VALUES(7, 1, 'Output state', '2021-02-26', '2021-02-28', 9)

SELECT * FROM components WHERE id_thing = 1 AND id_project = 1
SELECT * FROM variables WHERE id_component = 3 AND id_project = 1

CREATE TABLE IF NOT EXISTS variables_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_variable INTEGER NOT NULL,
    value TEXT NOT NULL,
    begin_date TEXT NOT NULL,
	edited_date TEXT,
	FOREIGN KEY(id_variable) REFERENCES variables(id)
);

INSERT INTO variables_values(id_variable, value, begin_date) VALUES(1, 'Fully Open', '2021-02-26')
INSERT INTO variables_values(id_variable, value, begin_date) VALUES(1, 'Fully Closed', '2021-02-26')
INSERT INTO variables_values(id_variable, value, begin_date) VALUES(1, 'Partially Open', '2021-02-26')

SELECT * from variables
SELECT * FROM variables_values WHERE id_variable = 1

INSERT INTO variables_values(id_variable, value, begin_date) VALUES(2, 'Person in doorway', '2021-02-26')
INSERT INTO variables_values(id_variable, value, begin_date) VALUES(2, 'Person not in doorway', '2021-02-26')

INSERT INTO variables_values(id_variable, value, begin_date) VALUES(3, 'Aligned with platform', '2021-02-26')
INSERT INTO variables_values(id_variable, value, begin_date) VALUES(3, 'Not aligned with platform', '2021-02-26')

INSERT INTO variables_values(id_variable, value, begin_date) VALUES(4, 'Stopped', '2021-02-26')
INSERT INTO variables_values(id_variable, value, begin_date) VALUES(4, 'Train is moving', '2021-02-26')

INSERT INTO variables_values(id_variable, value, begin_date) VALUES(5, 'No emergency', '2021-02-26')
INSERT INTO variables_values(id_variable, value, begin_date) VALUES(5, 'Evacuation required', '2021-02-26')


INSERT INTO variables_values(id_variable, value, begin_date) VALUES(6, 'Passengers entering', '2021-02-26')
INSERT INTO variables_values(id_variable, value, begin_date) VALUES(6, 'Passengers exiting', '2021-02-26')

INSERT INTO variables_values(id_variable, value, begin_date) VALUES(7, 'Passengers in', '2021-02-26')
INSERT INTO variables_values(id_variable, value, begin_date) VALUES(7, 'Passengers out', '2021-02-26')


SELECT * FROM variables_values

CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	source INTEGER NOT NULL,
	destiny INTEGER NOT NULL,
    name TEXT NOT NULL,
    name_ontology TEXT NOT NULL,
    name_link TEXT NOT NULL,
	FOREIGN KEY(source) REFERENCES things(id)
	FOREIGN KEY(destiny) REFERENCES things(id)
);

SELECT a.name FROM actions AS a WHERE a.name_ontology = 'Control_action_actuator'


SELECT a.id, a.source, a.destiny, a.name, a.name_ontology, a.name_link, c.name FROM actions AS a
	JOIN components AS c ON a.source = c.id_thing
		WHERE a.name_ontology = 'Feedback_of_CP' AND c.id_project = 1



CREATE TABLE IF NOT EXISTS actions_component (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_component_src INTEGER NOT NULL,
	id_action INTEGER NOT NULL,
	name TEXT NOT NULL,
	begin_date TEXT NOT NULL,
	edited_date TEXT,
	id_project INTEGER NOT NULL,
	FOREIGN KEY(id_component_src) REFERENCES components(id)
	FOREIGN KEY(id_action) REFERENCES components(id)
	FOREIGN KEY(id_project) REFERENCES projects(id)
);

drop table actions_component

INSERT INTO actions_component(id_component_src, id_action, name, begin_date, edited_date, id_project) VALUES(1, 1, 'Open Door', '2021-02-26', '', 1)
INSERT INTO actions_component(id_component_src, id_action, name, begin_date, edited_date, id_project) VALUES(1, 1, 'Close Door', '2021-02-26', '', 1)

SELECT * FROM actions
SELECT * FROM actions_component


SELECT * FROM components

CREATE TABLE IF NOT EXISTS components_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_component_src INTEGER NOT NULL,
	id_component_dst INTEGER NOT NULL,
	FOREIGN KEY(id_component_src) REFERENCES components(id)
	FOREIGN KEY(id_component_dst) REFERENCES components(id)
);

INSERT INTO components_links(id_component_src, id_component_dst) VALUES(1, 2)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(3, 1)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(4, 1)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(8, 1)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(9, 1)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(2, 5)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(5, 3)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(6, 5)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(5, 7)
INSERT INTO components_links(id_component_src, id_component_dst) VALUES(10, 5)


SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date FROM components AS c 
                    JOIN things AS t ON t.id = c.id_thing 
                    WHERE t.ontology_name = 'Environmental_disturbances' AND c.id_project = 1


SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date, t.ontology_name FROM components AS c 
	JOIN things AS t ON t.id = c.id_thing 
	WHERE t.ontology_name = 'Environmental_disturbances' AND c.id_project = 1



CREATE TABLE IF NOT EXISTS saf_uca_type (
    id INTEGER PRIMARY KEY,
	description INTEGER NOT NULL
);

INSERT INTO saf_uca_type(id, description) VALUES (1, 'provided')
INSERT INTO saf_uca_type(id, description) VALUES (2, 'not provided')
INSERT INTO saf_uca_type(id, description) VALUES (3, 'provided too early')
INSERT INTO saf_uca_type(id, description) VALUES (4, 'provided too late')
INSERT INTO saf_uca_type(id, description) VALUES (5, 'provided in wrong order')
INSERT INTO saf_uca_type(id, description) VALUES (6, 'stopped too son')
INSERT INTO saf_uca_type(id, description) VALUES (7, 'applied too long')

SELECT * FROM saf_uca_type


CREATE TABLE IF NOT EXISTS saf_uca (
    id INTEGER PRIMARY KEY,
	id_controller INTEGER NOT NULL,
	id_uca_type INTEGER NOT NULL,
	id_control_action INTEGER NOT NULL,
	order_analysis INTEGER NOT NULL,
	FOREIGN KEY(id_controller) REFERENCES components(id)
	FOREIGN KEY(id_uca_type) REFERENCES saf_uca_type(id)
	FOREIGN KEY(id_control_action) REFERENCES actions_component(id)
);

CREATE TABLE IF NOT EXISTS saf_uca_hazard (
    id INTEGER PRIMARY KEY,
	id_uca INTEGER NOT NULL,
	id_hazard INTEGER NOT NULL,
	FOREIGN KEY(id_uca) REFERENCES saf_uca(id)
	FOREIGN KEY(id_hazard) REFERENCES hazards(id)
);


CREATE TABLE IF NOT EXISTS saf_uca_context (
    id INTEGER PRIMARY KEY,
	id_uca INTEGER NOT NULL,
	id_variable INTEGER NOT NULL,
	id_value INTEGER NOT NULL,
	FOREIGN KEY(id_uca) REFERENCES saf_uca(id)
	FOREIGN KEY(id_variable) REFERENCES variables(id)
	FOREIGN KEY(id_value) REFERENCES variables_values(id)
);

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action) VALUES (1, 4, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (1, 5, 11)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (1, 3)

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action) VALUES (1, 4, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (2, 2, 4)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (2, 1)


INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action) VALUES (1, 5, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (3, 4, 9)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (3, 2)

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action) VALUES (1, 5, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (4, 3, 7)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (4, 2)


INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action) VALUES (1, 2, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (5, 4, 8)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (5, 2)

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action) VALUES (1, 3, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (6, 4, 9)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (6, 2)

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action) VALUES (1, 3, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (7, 5, 11)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (7, 3)


INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action) VALUES (1, 7, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (8, 5, 11)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (8, 3)


INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action, order_analysis) VALUES (1, 4, 2, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (9, 1, 1)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (9, 4, 9)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (9, 2)

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action, order_analysis) VALUES (1, 4, 2, 2)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (10, 1, 3)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (10, 4, 9)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (10, 2)


INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action, order_analysis) VALUES (1, 5, 2, 3)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (11, 2, 4)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (11, 1)

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action, order_analysis) VALUES (1, 5, 2, 4)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (12, 5, 11)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (12, 3)


INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action, order_analysis) VALUES (1, 2, 2, 5)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (13, 2, 4)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (13, 1)

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action, order_analysis) VALUES (1, 3, 2, 6)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (14, 4, 9)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (14, 2)

INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action, order_analysis) VALUES (1, 3, 2, 7)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (15, 1, 3)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (15, 2)


INSERT INTO saf_uca(id_controller, id_uca_type, id_control_action, order_analysis) VALUES (1, 7, 2, 8)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (16, 1, 3)
INSERT INTO saf_uca_context(id_uca, id_variable, id_value) VALUES (16, 4, 9)
INSERT INTO saf_uca_hazard(id_uca, id_hazard) VALUES (16, 2)




CREATE TABLE IF NOT EXISTS saf_loss_scenario_req (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_controller INTEGER NOT NULL,
	id_uca INTEGER NOT NULL,
	id_project INTEGER NOT NULL,
	id_comp_cause INTEGER NOT NULL,
	id_comp_src INTEGER NOT NULL,
	id_comp_dst INTEGER NOT NULL,
	requirement TEXT NOT NULL,
	cause TEXT NOT NULL,
	FOREIGN KEY(id_controller) REFERENCES components(id)
	FOREIGN KEY(id_uca) REFERENCES saf_uca(id)
	FOREIGN KEY(id_project) REFERENCES projects(id)
	FOREIGN KEY(id_comp_cause) REFERENCES components(id)
	FOREIGN KEY(id_comp_src) REFERENCES components(id)
	FOREIGN KEY(id_comp_dst) REFERENCES components(id)
);

drop table saf_loss_scenario_req

drop table components_links_var
CREATE TABLE IF NOT EXISTS components_links_var (
    id INTEGER PRIMARY KEY,
	id_link INTEGER NOT NULL,
	id_var INTEGER,
	id_act INTEGER,
	FOREIGN KEY(id_link) REFERENCES components_links(id)
	FOREIGN KEY(id_var) REFERENCES variables(id)
	FOREIGN KEY(id_act) REFERENCES actions_component(id)
);
	








select * from saf_uca_type
select * from actions_component
select * from variables
select * from variables_values



SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name, sf.order_analysis 
	FROM saf_uca AS sf
	JOIN components AS c ON c.id = sf.id_controller
	JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type
	JOIN actions_component AS ac ON ac.id = sf.id_control_action
	WHERE sf.id_controller = 1

	
	
SELECT suc.id, suc.id_uca, suc.id_variable, v.name, suc.id_value, vv.value FROM saf_uca_context AS suc
	JOIN variables AS v ON v.id = suc.id_variable
	JOIN variables_values AS vv ON vv.id = suc.id_value
	WHERE suc.id_uca = 1
	

SELECT suh.id, suh.id_uca, suh.id_hazard, h.description FROM saf_uca_hazard AS suh
	JOIN hazards AS h ON h.id = suh.id_hazard
	WHERE suh.id_uca = 2

ALTER TABLE saf_uca_type ADD COLUMN order INTEGER NOT NULL DEFAULT 0;
SELECT * FROM saf_uca


ALTER TABLE components ADD COLUMN comp_father INTEGER NOT NULL DEFAULT 0;


SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date, v.edited_date FROM variables AS v 
                      JOIN components AS c ON v.id_component = c.id 
                        JOIN actions AS a ON a.source = c.id_thing 
                        WHERE c.id_project = 1 AND a.name_ontology = 'Feedback_of_CP'
						
						
SELECT h.id, h.id_project, h.id_loss, h.id_hazard, h.description, h.begin_date, h.edited_date, l.id_loss FROM hazards AS h 
	JOIN losses AS l ON h.id_loss = l.id
	WHERE h.id_project = 1

SELECT * FROM hazards
SELECT * FROM losses


ALTER TABLE variables ADD CONSTRAINT id_component_link FOREIGN KEY (id_component_link) REFERENCES components_links(id);
ALTER TABLE variables ADD COLUMN id_component_link INTEGER REFERENCES components_links(id);
ALTER TABLE actions_component ADD COLUMN id_component_link INTEGER REFERENCES components_links(id);


				  
SELECT * FROM variables
SELECT * FROM variables_values
SELECT * FROM components_links
SELECT * FROM components
SELECT * FROM things

SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, t.ontology_name, t.name FROM components AS c 
	JOIN things AS t ON t.id = c.id_thing WHERE c.id_project = 1

SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
	JOIN components AS cs ON cl.id_component_src = cs.id
	JOIN components AS cd ON cl.id_component_dst = cd.id
	WHERE cs.id_project = 1 AND cd.id_project = 1 AND cs.id_thing = 1
	
SELECT * FROM actions 

ALTER TABLE actions_component ADD COLUMN id_project INTEGER REFERENCES projects(id)







SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
	JOIN components AS cs ON cl.id_component_src = cs.id
	JOIN components AS cd ON cl.id_component_dst = cd.id
	WHERE cs.id_project = 1 AND cd.id_project = 1 AND cd.id_thing = 6


SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date, v.id_component_link from variables AS v
	JOIN components_links AS cl ON v.id_component_link  = cl.id
	JOIN components AS c ON c.id = cl.id_component_dst
	WHERE c.id = 1

SELECT * FROM components WHERE 
	JOIN components_links AS cl ON 


SELECT * from things
SELECT * from components_links
SELECT * FROM variables_values WHERE id_variable = 1

INSERT INTO variables_values(id_variable, value, begin_date) VALUES(2, 'Person in doorway', '2021-02-26')

SELECT * FROM components




SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date, v.id_component_link from variables AS v 
                    JOIN components_links AS cl ON v.id_component_link = cl.id 
                    JOIN components AS c ON c.id = cl.id_component_dst  
					JOIN things AS t ON t.id = c.id_thing
					WHERE c.id = 1 AND t.id = 7
					
					select * from components
					select * from components_links
					select * from things as t WHERE t.ontology_name = 'External_communication'
					select * from variables
					
SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date, t.ontology_name FROM components AS c 
                    JOIN things AS t ON t.id = c.id_thing 
					JOIN components_links AS cl ON cl.id_component_dst = c.id
                    WHERE t.ontology_name = 'External_communication' AND c.id_project = 1 
					
					
SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date FROM components AS c 
					JOIN components_links AS cl ON cl.id_component_src = c.id
                    WHERE cl.id_component_dst = 1 AND cl.id_component_src = 4 AND c.id_project = 1 
					
select * from components_links AS cl where 
SELECT * FROM components
					
SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name 
                    FROM components_links AS cl 
                    JOIN components AS cs ON cl.id_component_src = cs.id 
                    JOIN components AS cd ON cl.id_component_dst = cd.id 
                    WHERE cs.id_project = 1 AND cd.id_project = 1 AND cs.id_thing = 4 AND cl.id_component_dst = 1


SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
	JOIN components AS cs ON cl.id_component_src = cs.id 
    JOIN components AS cd ON cl.id_component_dst = cd.id 
	WHERE cl.id_component_dst = 1

SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
	JOIN components AS cs ON cl.id_component_src = cs.id 
    JOIN components AS cd ON cl.id_component_dst = cd.id 
	WHERE cl.id_component_src = 1 
                    
                    
                    WHERE cs.id_project = ? AND cd.id_project = ? AND cl.id_component_dst = 1
					
select * from safety_constraints_hazards
SELECT sch.id, sch.id_project, sch.id_constraint, sch.id_hazard, h.id_hazard FROM safety_constraints_hazards AS sch 
         JOIN hazards AS h ON h.id = sch.id_hazard
         WHERE sch.id_project = 1 AND sch.id_constraint = 1 ORDER BY h.id_hazard
		 
		 
SELECT * FROM components WHERE id_project = 1 AND comp_father = 1 AND id_thing = 7
SELECT id FROM components WHERE id_project = 1 AND comp_father = 80 AND id_thing = 7

SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date, c.name from variables AS v 
	JOIN components AS c ON c.id = v.id_component 
	WHERE c.id_project = 1 AND c.id_thing = 3 
	
select * from variables
select * from components

SELECT suc.id, suc.id_uca, suc.id_variable, v.name, suc.id_value, vv.value FROM saf_uca_context AS suc 
                    JOIN variables AS v ON v.id = suc.id_variable 
                    JOIN variables_values AS vv ON vv.id = suc.id_value 
                    
					
SELECT suc.id, suc.id_uca, suc.id_variable, suc.id_value FROM saf_uca_context AS suc WHERE suc.id_uca = 16
SELECT name FROM variables WHERE id = 3
SELECT value FROM variables_values WHERE id = 3

SELECT id FROM saf_uca WHERE id_control_action = 20
SELECT * FROM variables_values WHERE id_variable = 102

SELECT * FROM components WHERE id_thing = 1 AND id_project = 1 AND id <> 1

SELECT * FROM saf_loss_scenario_req

SELECT lsr.id, lsr.id_controller, lsr.id_uca, lsr.id_project, lsr.id_comp_cause, lsr.id_comp_src, lsr.id_comp_dst, lsr.requirement, lsr.cause, cs.name, cd.name, cc.name FROM saf_loss_scenario_req AS lsr 
	JOIN components AS cs ON cs.id = lsr.id_comp_src
	JOIN components AS cd ON cd.id = lsr.id_comp_dst
	JOIN components AS cc ON cc.id = lsr.id_comp_dst
	WHERE id_uca = 1
	
SELECT * FROM saf_uca
SELECT * FROM components


SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name FROM saf_uca AS sf
            JOIN components AS c ON c.id = sf.id_controller
            JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type 
            JOIN actions_component AS ac ON ac.id = sf.id_control_action
            WHERE c.id_project = 1
			
			
SELECT lsr.id, lsr.id_controller, lsr.id_uca, lsr.id_project, lsr.id_comp_cause, lsr.id_comp_src, lsr.id_comp_dst, lsr.requirement, 
                    lsr.cause, cs.name, cd.name, cc.name FROM saf_loss_scenario_req AS lsr 
                    JOIN components AS cs ON cs.id = lsr.id_comp_src 
                    JOIN components AS cd ON cd.id = lsr.id_comp_dst 
                    JOIN components AS cc ON cc.id = lsr.id_comp_dst 
                    WHERE lsr.id_project = 1
					
					
ALTER TABLE saf_uca ADD COLUMN uca_origin TEXT NOT NULL DEFAULT ''
ALTER TABLE saf_uca ADD COLUMN is_hazardous INTEGER NOT NULL DEFAULT 0
ALTER TABLE saf_uca DROP not_hazardous

SELECT * from saf_uca

SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name, sf.uca_origin, sf.is_hazardous FROM saf_uca AS sf 
                    JOIN components AS c ON c.id = sf.id_controller 
                    JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type 
                    JOIN actions_component AS ac ON ac.id = sf.id_control_action  
                    WHERE sf.id_control_action= 1 AND sf.uca_origin = 'rule'
					
					
SELECT * FROM saf_loss_scenario_req WHERE id_uca = 1

UPDATE components SET name = 'LALA teste', edited_date = '6/6/6' WHERE comp_father = 108 AND id_thing = 9


SELECT * FROM components_links_var WHERE id_var = 


SELECT count(id) FROM actions_component WHERE id_component_src = 1
SELECT id FROM actions_component WHERE id_component_src = 1


SELECT count(id) FROM variables WHERE id_component = 1
SELECT * FROM variables


SELECT count(id) FROM components_links WHERE id_component_src = 1 OR id_component_dst = 1
SELECT * FROM components_links WHERE id_component_src = 1 OR id_component_dst = 1


SELECT count(id) FROM saf_uca WHERE id_controller = 1 AND is_hazardous = 1
SELECT * FROM saf_uca WHERE id_controller = 1


SELECT count(id) FROM saf_loss_scenario_req WHERE id_controller = 1
SELECT * FROM saf_loss_scenario_req WHERE id_controller = 1







SELECT sf.id, sf.id_controller, c.name, sf.id_uca_type, sut.description, sf.id_control_action, ac.name, sf.is_hazardous FROM saf_uca AS sf 
            JOIN components AS c ON c.id = sf.id_controller 
            JOIN saf_uca_type AS sut ON sut.id = sf.id_uca_type 
            JOIN actions_component AS ac ON ac.id = sf.id_control_action 
            WHERE c.id_project = 1 AND sf.is_hazardous = 1


SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
                   JOIN components AS cs ON cl.id_component_src = cs.id 
                   JOIN components AS cd ON cl.id_component_dst = cd.id 
                   WHERE cs.id_project = 1 AND cd.id_project = 1
				   
SELECT * FROM components
SELECT * FROM things



SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, ts.ontology_name, td.ontology_name FROM components_links AS cl 
                   JOIN components AS cs ON cl.id_component_src = cs.id 
                   JOIN components AS cd ON cl.id_component_dst = cd.id 
				   JOIN things AS ts ON ts.id = cs.id_thing
				   JOIN things AS td ON td.id = cd.id_thing
                   WHERE cs.id_project = 1 AND cd.id_project = 1
				   

SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
                   JOIN components AS cs ON cl.id_component_src = cs.id 
                   JOIN components AS cd ON cl.id_component_dst = cd.id 
                   WHERE cl.id_component_dst = 1 AND cs.id_thing <> 1 AND cs.id_thing <> 11


SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
                   JOIN components AS cs ON cl.id_component_src = cs.id 
                   JOIN components AS cd ON cl.id_component_dst = cd.id 
                   WHERE cl.id_component_dst = 1

				   
SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
                   JOIN components AS cs ON cl.id_component_src = cs.id 
                   JOIN components AS cd ON cl.id_component_dst = cd.id 
                   WHERE cl.id_component_src = 1 AND (cd.id_thing == 1 OR cd.id_thing == 11)

				   
SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date, t.ontology_name, t.name
                    FROM components AS c 
                    JOIN things AS t ON t.id = c.id_thing 
                    WHERE c.id_project = 1 AND c.id_thing <> 8 AND c.id_thing <> 9 AND c.id_thing <> 10 ORDER BY c.name
					
					
DELETE FROM components_links_var WHERE id_link = 80

SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
                   JOIN components AS cs ON cl.id_component_src = cs.id 
                   JOIN components AS cd ON cl.id_component_dst = cd.id 
                   WHERE cl.id_component_src = 1 AND cs.id_thing == 1
				   
ALTER TABLE components ADD COLUMN is_external_component INTEGER NOT NULL DEFAULT 0;
ALTER TABLE components ADD COLUMN hlc_control INTEGER NOT NULL DEFAULT 0;


SELECT c.id, c.id_thing, c.id_project, c.name, c.begin_date, c.edited_date, c.comp_father, c.is_external_component FROM components AS c


SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
		JOIN components AS cs ON cl.id_component_src = cs.id 
		JOIN components AS cd ON cl.id_component_dst = cd.id 
		WHERE cs.id_project = 1 AND cd.id_project = 1
		

SELECT cv.id, cv. id_link, cv.id_var, cv.id_act, ac.name, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links_var AS cv
		JOIN components_links AS cl ON cv.id_link = cl.id
		JOIN components AS cs ON cl.id_component_src = cs.id 
		JOIN components AS cd ON cl.id_component_dst = cd.id 
		JOIN actions_component AS ac ON cv.id_act = ac.id
		WHERE cs.id_project = 1 AND cd.id_project = 1 AND cd.id = 9 AND cv.id_act > 0 AND cs.id_thing = 1 AND cd.id_thing = 1
		
		
select * from components
select * from actions_component







SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
	JOIN components AS cs ON cl.id_component_src = cs.id 
    JOIN components AS cd ON cl.id_component_dst = cd.id
	INNER JOIN components_hlc AS ch ON ch.id_controller = cl.id_component_src 
    WHERE cl.id_component_src = 110 AND cs.id_thing == 1 AND cl.id <> ch.id_hlc
	
	
	
	
SELECT id_hlc FROM components_hlc WHERE id_controller = 110



SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
                   JOIN components AS cs ON cl.id_component_src = cs.id 
                   JOIN components AS cd ON cl.id_component_dst = cd.id 
                   WHERE cl.id_component_dst = 110
				  



DELETE FROM components_hlc WHERE id_controller = 666 OR id_hlc = 666


CREATE TABLE IF NOT EXISTS components_hlc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	id_controller INTEGER NOT NULL,
	id_hlc INTEGER NOT NULL,
	FOREIGN KEY(id_controller) REFERENCES components(id)
	FOREIGN KEY(id_hlc) REFERENCES components(id)
);

	
SELECT DISTINCT ac.name FROM actions_component  AS ac
	JOIN components_links_var AS clv ON clv.id_act = ac.id
	JOIN components_links AS cl ON cl.id = clv.id_link
	JOIN components_hlc AS ch ON ch.id_controller = cl.id_component_src
	WHERE ac.id_project = 1 AND cl.id_component_src = 110 AND ch.id_controller = 110 AND id_hlc = 5
	
	
SELECT DISTINCT var.name FROM variables AS var
	JOIN components_links_var AS clv ON clv.id_var = var.id
	JOIN components_links AS cl ON cl.id = clv.id_link
	JOIN components_hlc AS ch ON ch.id_controller = cl.id_component_dst
	WHERE var.id_project = 1 AND cl.id_component_src = 110 AND ch.id_controller = 110 AND id_hlc = 5
	
	
	
	
SELECT ac.id, ac.id_component_src, ac.name, ac.begin_date, ac.edited_date, ac.id_project FROM actions_component AS ac
	JOIN components_links_var AS clv ON clv.id_act = ac.id
	JOIN components_links AS cl ON cl.id = clv.id_link
	WHERE cl.id_component_src = 116 AND ac.id_project = 4 AND cl.id_component_dst = 125
	
	
SELECT * FROM variables WHERE id_component = ? AND id_project = 4

SELECT * FROM components_links_var
SELECT * FROM components_hlc
SELECT * FROM components_links
SELECT * FROM components
SELECT * FROM actions_component




SELECT cv.id, cv. id_link, cv.id_var, cv.id_act, ac.name, cl.id_component_src, cl.id_component_dst, cs.name, cd.name 
                    FROM components_links_var AS cv 
                    JOIN components_links AS cl ON cv.id_link = cl.id 
		            JOIN components AS cs ON cl.id_component_src = cs.id 
		            JOIN components AS cd ON cl.id_component_dst = cd.id 
		            JOIN actions_component AS ac ON cv.id_act = ac.id 
		            WHERE cs.id_project = 4 AND cd.id_project = 4 AND cd.id = 122 AND cv.id_act > 0 AND cs.id_thing = 1 AND cd.id_thing = 1
					
					
					
					
SELECT ac.name, cs.name, cd.name  FROM components_links_var AS clv 
	JOIN actions_component AS ac ON ac.id = clv.id_act
	JOIN components_links AS cl ON clv.id_link = cl.id 
	JOIN components AS cs ON cl.id_component_src = cs.id 
	JOIN components AS cd ON cl.id_component_dst = cd.id 
	WHERE clv.id_link = 83 and clv.id_act > 0
	

SELECT v.name, cs.name, cd.name FROM components_links_var AS clv 
	JOIN variables AS v ON v.id = clv.id_var
	JOIN components_links AS cl ON clv.id_link = cl.id 
	JOIN components AS cs ON cl.id_component_src = cs.id 
	JOIN components AS cd ON cl.id_component_dst = cd.id 
	WHERE clv.id_link = 83 and clv.id_var > 0

	
SELECT ac.name, cs.name, cd.name FROM components_links AS cl 
	JOIN components_links_var AS clv ON clv.id_link = cl.id
	JOIN actions_component AS ac ON ac.id = clv.id_act
	JOIN components AS cs ON cl.id_component_src = cs.id 
	JOIN components AS cd ON cl.id_component_dst = cd.id 
	WHERE cl.id_component_src = 122 AND cl.id_component_dst = 116 AND clv.id_act > 0 AND cs.id_thing = 1




SELECT * FROM components

ALTER TABLE project_files ADD COLUMN order_file INTEGER NOT NULL DEFAULT 1;
	
	