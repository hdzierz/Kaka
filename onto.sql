--
--,PostgreSQL,database,dump
--

SET statement_timeout=0;
SET lock_timeout=0;
SET client_encoding='UTF8';
SET standard_conforming_strings=on;
SET check_function_bodies=false;
SET client_min_messages=warning;

SET search_path=public,pg_catalog;

--
--,Data,for,Name:,api_ontology;,Type:,TABLE,DATA;,Schema:,public;,Owner:,pinf
--

COPY api_ontology(id,name,tablename,owner,classname,is_entity,"group") FROM './onto.csv' WITH DELIMITER ',';
20,Study,api_study,api,Study,t,api
21,Tree,seafood_tree,seafood,Tree,t,seafood
22,Crew,seafood_crew,seafood,Crew,t,seafood
23,Species,api_species,api,Species,t,api
24,Vessel,seafood_vessel,seafood,Vessel,t,seafood
25,Trip,seafood_trip,seafood,Trip,t,seafood
26,Treatment,api_treatment,api,Treatment,t,api
27,SampleMethod,api_sample_method,api,SampleMethod,t,api
28,Instrument,api_instrument,api,Instrument,t,api
29,Tow,seafood_tow,seafood,Tow,t,seafood
30,City,seafood_city,seafood,City,t,seafood
31,BioSubject,api_bio_subject,api,BioSubject,t,api
33,Primer,genotype_primer,genotype,Primer,t,genotype
34,PrimerType,genotype_primer_type,genotype,PrimerType,t,genotype
35,PrimerOb,genotype_primer_ob,genotype,PrimerOb,t,genotype
36,Marker,genotype_marker,genotype,Marker,t,genotype
69,Term,api_term,api,Term,t,api
70,DataSource,api_datasource,api,DataSource,t,api
72,Staff,seafood_staff,seafood,Staff,t,seafood
74,Gene,gene_expression_gene,gene_expression,Gene,t,gene_expression
76,Target,gene_experssion_target,gene_experssion,Target,t,gene_experssion
32,Fish,seafood_fish,seafood,Fish,t,seafood
83,StudyArea,api_studyarea,api,StudyArea,t,api
84,Protein,api_protein,api,Protein,t,api
85,StudyGroup,api_studygroup,api,StudyGroup,t,api
86,Tissue,api_tissue,api,Tissue,t,api


SELECT pg_catalog.setval('api_ontology_id_seq',86,true);


--
--,PostgreSQL,database,dump,complete
--

