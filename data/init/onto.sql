--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

--
-- Data for Name: core_ontology; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (20, 'Study', 'core_study', 'api', NULL, 'Study', true, 'api');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (21, 'Tree', 'seafood_tree', 'seafood', NULL, 'Tree', true, 'seafood');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (22, 'Crew', 'seafood_crew', 'seafood', NULL, 'Crew', true, 'seafood');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (23, 'Species', 'core_species', 'api', NULL, 'Species', true, 'api');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (24, 'Vessel', 'seafood_vessel', 'seafood', NULL, 'Vessel', true, 'seafood');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (25, 'Trip', 'seafood_trip', 'seafood', NULL, 'Trip', true, 'seafood');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (26, 'Treatment', 'core_treatment', 'api', NULL, 'Treatment', true, 'api');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (27, 'SampleMethod', 'core_sample_method', 'api', NULL, 'SampleMethod', true, 'api');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (28, 'Instrument', 'core_instrument', 'api', NULL, 'Instrument', true, 'api');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (29, 'Tow', 'seafood_tow', 'seafood', NULL, 'Tow', true, 'seafood');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (30, 'City', 'seafood_city', 'seafood', NULL, 'City', true, 'seafood');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (31, 'BioSubject', 'core_bio_subject', 'api', NULL, 'BioSubject', true, 'api');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (33, 'Primer', 'genotype_primer', 'genotype', NULL, 'Primer', true, 'genotype');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (34, 'PrimerType', 'genotype_primer_type', 'genotype', NULL, 'PrimerType', true, 'genotype');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (35, 'PrimerOb', 'genotype_primer_ob', 'genotype', NULL, 'PrimerOb', true, 'genotype');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (36, 'Marker', 'genotype_marker', 'genotype', NULL, 'Marker', true, 'genotype');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (69, 'Term', 'core_term', 'api', NULL, 'Term', true, 'api');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (70, 'DataSource', 'core_datasource', 'api', NULL, 'DataSource', true, 'api');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (72, 'Staff', 'seafood_staff', 'seafood', NULL, 'Staff', true, 'seafood');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (74, 'Gene', 'gene_expression_gene', 'gene_expression', NULL, 'Gene', true, 'gene_expression                                                              ');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (76, 'Target', 'gene_experssion_target', 'gene_experssion', NULL, 'Target', true, 'gene_experssion                                                        ');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (32, 'Fish', 'seafood_fish', 'seafood', NULL, 'Fish', true, 'seafood                                                                                            ');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (83, 'StudyArea', 'core_studyarea', 'api', NULL, 'StudyArea', true, 'api                                                                                         ');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (84, 'Protein', 'core_protein', 'api', NULL, 'Protein', true, 'api                                                                                               ');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (85, 'StudyGroup', 'core_studygroup', 'api', NULL, 'StudyGroup', true, 'api                                                                                      ');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (86, 'Tissue', 'core_tissue', 'api', NULL, 'Tissue', true, 'api                                                                                                  ');
INSERT INTO core_ontology (id, name, tablename, owner, description, classname, is_entity, "group") VALUES (1, 'Genotype', 'genotype_genotype', 'genotype', '', 'Genotype', true, 'genotype');


--
-- Name: core_ontology_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('core_ontology_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

