SELECT ac.id, ac.id_component_src, ac.name, ac.begin_date, ac.edited_date, ac.id_project FROM actions_component AS ac
	JOIN components AS c ON c.id = ac.id_component_src
	WHERE ac.id_project = 5 AND c.is_external_component = 0
	
	SELECT * FROM components
	
SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date, v.edited_date FROM variables AS v 
	JOIN components AS c ON c.id = v.id_component
	WHERE v.id_project = 5 AND c.is_external_component = 0 AND c.id_thing = 1
	
	
	SELECT v.id, v.id_component, v.id_project, v.name, v.begin_date,  v.edited_date from variables AS v WHERE v.id = 68
	
	
	select * from components
	SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cs.id_thing, cd.name, cd.id_thing FROM components_links AS cl 
           JOIN components AS cs ON cl.id_component_src = cs.id 
           JOIN components AS cd ON cl.id_component_dst = cd.id 
		   JOIN components_links_var AS clv ON clv.id_link = cl.id
           WHERE clv.id_act = 30
		   
		   
SELECT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cs.id_thing, cd.name, cd.id_thing FROM components_links AS cl 
           JOIN components AS cs ON cl.id_component_src = cs.id 
           JOIN components AS cd ON cl.id_component_dst = cd.id 
		   JOIN components_links_var AS clv ON clv.id_link = cl.id
           WHERE clv.id_var = 100
		   
		   
SELECT * FROM sec_stride_requirement
SELECT * FROM sec_stride_dfd
SELECT * FROM sec_stride_priority


SELECT ssr.id, ssr.title, ssr.description, ssr.justification, ssr.id_priority, ssp.name, ssr.id_uca, ssr.id_link, ssr.id_dfd, ssd.name, ssr.id_stride, ss.name FROM sec_stride_requirement AS ssr
	JOIN sec_stride_priority AS ssp ON ssr.id_priority = ssp.id
	JOIN sec_stride_dfd AS ssd ON ssr.id_dfd = ssd.id
	JOIN sec_stride AS ss ON ssr.id_stride = ss.id
	WHERE ssr.id_uca = 17
	
	
	
SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name FROM components_links AS cl 
       JOIN components AS cs ON cl.id_component_src = cs.id 
       JOIN components AS cd ON cl.id_component_dst = cd.id 
       JOIN components_links_var AS clv ON clv.id_link = cl.id 
       WHERE cs.id_thing = 1 AND cd.id_thing = 1 AND cd.id_project = 6 AND cs.id_project = 6

		   SELECT * from projects
		   
SELECT v.name from variables AS v 
           JOIN components_links_var AS clv ON clv.id_var = v.id 
           WHERE clv.id_link = ?

SELECT a.name FROM actions_component AS a
                  JOIN components_links_var AS clv ON clv.id_act = a.id
                  WHERE clv.id_link = ?		   
		   
	
SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing FROM components_links AS cl 
	   JOIN components AS cs ON cl.id_component_src = cs.id 
	   JOIN components AS cd ON cl.id_component_dst = cd.id 
	   JOIN components_links_var AS clv ON clv.id_link = cl.id 
	   WHERE cl.id_component_dst = 164 AND clv.id_var > 0 AND cs.id_thing <> 1

SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing FROM components_links AS cl 
	   JOIN components AS cs ON cl.id_component_src = cs.id 
	   JOIN components AS cd ON cl.id_component_dst = cd.id 
	   JOIN components_links_var AS clv ON clv.id_link = cl.id 
	   WHERE cl.id_component_dst = 164 AND clv.id_var > 0 AND cs.id_thing == 1	   

SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing FROM components_links AS cl 
	   JOIN components AS cs ON cl.id_component_src = cs.id 
	   JOIN components AS cd ON cl.id_component_dst = cd.id 
	   JOIN components_links_var AS clv ON clv.id_link = cl.id 
	   WHERE cl.id_component_src = 164 AND clv.id_var > 0 AND cd.id_thing = 7
	   
SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing FROM components_links AS cl 
	   JOIN components AS cs ON cl.id_component_src = cs.id 
	   JOIN components AS cd ON cl.id_component_dst = cd.id 
	   JOIN components_links_var AS clv ON clv.id_link = cl.id 
	   WHERE cl.id_component_src = 164 AND clv.id_act > 0 AND cd.id_thing = 7

	   

				   
SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing FROM components_links AS cl 
	   JOIN components AS cs ON cl.id_component_src = cs.id 
	   JOIN components AS cd ON cl.id_component_dst = cd.id 
	   JOIN components_links_var AS clv ON clv.id_link = cl.id 
	   WHERE cl.id_component_src = 161 AND clv.id_act > 0 AND cd.id_thing <> 1

SELECT DISTINCT cl.id, cl.id_component_src, cl.id_component_dst, cs.name, cd.name, cs.id_thing, cd.id_thing FROM components_links AS cl 
	   JOIN components AS cs ON cl.id_component_src = cs.id 
	   JOIN components AS cd ON cl.id_component_dst = cd.id 
	   JOIN components_links_var AS clv ON clv.id_link = cl.id 
	   WHERE cl.id_component_src = 161 AND clv.id_act > 0 AND cd.id_thing == 1 