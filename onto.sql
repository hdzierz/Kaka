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

SELECT pg_catalog.setval('api_ontology_id_seq',86,true);


--
--,PostgreSQL,database,dump,complete
--

