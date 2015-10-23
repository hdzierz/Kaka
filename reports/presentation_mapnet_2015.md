<style>
.reveal h1, .reveal h2, .reveal h3 {
  word-wrap: normal;
  -moz-hyphens: none;
}
.small-code pre code {
  font-size: 1em;
}
.midcenter {
    position: fixed;
    top: 50%;
    left: 50%;
}
.footer {
    color: black; background: #E8E8E8;
    position: fixed; top: 90%;
    text-align:center; width:100%;
}
.pinky .reveal .state-background {
  background: #FF69B4;
} 
.pinky .reveal h1,
.pinky .reveal h2,
.pinky .reveal p {
  color: black;
}
</style>


Kaka: Towards a Distrubuted Genotype Information System
========================================================
author: Helge Dzierzon and Samantha Baldwin
date: October 28 2015


TOC
========================================================

* Why
* How?
* Status
* Conclusions

Genotype Data in PFR
========================================================

* Many species
  + e.g. Kiwifruit, Apple, Pear, Potato, Grape, ...
* Genotype data we are concentrating on 
  + GBS
  + QTL
* Others?
  + Expression data?

Issues by PFR distribution of Wetware
========================================================

* 15 PFR sites
* Communication across sites difficult
* Access to the data via shared drives
* Data currently stored in Excel sheets

***

![PFR](images/pfr_nz.png)

Existing Databases Initiatives in PFR
========================================================

* EBrida (provenance)
* Kea (sample tracking)
* Ensembl (Genome Browsing)

DBs in development @PFR
========================================================

* Kaka (Genotypes concentrates on samples)
* Kakapo (Location)

Kaka
========================================================

* Supplmenet to Kea
* Python Django
* PGSQL and JSON (NoSQL)
* Docker Farms
* Continuous integration
* Needs location  (Chr, location on Chromosome)

***

![Django](images/python-django.png)
![Pgsql](images/pgsql.png)
![docker](images/docker.png)
![TravisCI](images/travis_cl.png)


Status
========================================================

* DB has been developed as a proof of concept
* Some example data have been loaded
* RStudio, noteboods databases etc. have been attached and can access api
* API has been developed

***

Screenshot

Conclusions
========================================================

* Genotype and phenotype data in one database
* Kea needs a schnittstelle 
* It is a great tool already but needs a nerd
* It needs some input from teh research community
* The data input is very manual
* Better visualisation

Thank you! Questions?
========================================================

![Questions](images/questions.jpg)


