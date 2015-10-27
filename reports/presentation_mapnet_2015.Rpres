

Kaka: Towards a Distrubuted Genotype Information System
========================================================
author: Helge Dzierzon and Samantha Baldwin
date: October 28 2015


TOC
========================================================

* Why
* How?
* Status
* Conclusions and Outview

Genotype Data in PFR
========================================================

* Many species
  + e.g. Kiwifruit, Apple, Pear, Potato, Grape, ...
* Genotype data e.g. 
  + GBS
  + QTL
  

PFR Wetware Distribution
========================================================

* 15 PFR sites
* Communication across sites difficult
* Analysts often on different sites

***

![PFR](images/pfr_nz.png)


Current way of "Sharing"
========================================================

* THE K-Drive
* Excel Sheets

***

![current situation](images/science_thunder.png)

Existing Databases in PFR
========================================================

* EBrida (breeder DB for e.g. pedigrees)
* Kea (inhouse sample tracking)
* Ensembl (Genome Browsing)
* Kaka (Genotypes concentrates on samples)
* Kakapo (Location)

Kaka
========================================================

* Adds om Kea
* Has Restful API
* Distributed (Docker Farms)
* Digests semi-structured data (JSON objcts, NoSQL)
* Continuous integration
* Stores location and sample_id (Chr, location on Chromosome)

***

![Django](images/python-django.png)
![Pgsql](images/pgsql.png)
![docker](images/docker.png)
![TravisCI](images/travis_cl.png)


Querying
======================================================

```
http://localhost/report/genotype/xlsx/?experiment=12East
http://localhost/report/genotype/csv/?experiment=12East
http://localhost/gui/genotype/list/
```

Screenshots
======================================================

![exps](images/exps.png)


Screenshots
======================================================

![exps](images/exps_csv.png)


Screenshots
======================================================

![exps](images/datasources.png)

Conclusions
========================================================

* Genotype and phenotype information in one database
* It is a great tool already but needs a nerd
* It needs some input from the research community
* Kea needs to be attached as a docker container
* The data input is very manual
* It needs an interface to Ensembl

Thank you! Questions?
========================================================

![Questions](images/questions.jpg)


