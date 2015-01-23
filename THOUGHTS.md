# Let the Kea Fly-integrating genotype storage with KEA

* We need to define an Ontology (which is also part of another project) because:
* terminology is VERY important
*   see http://en.wikipedia.org/wiki/Genotype
*   KEA uses genotype as ontology term for a genetically-unique individual. i.e. the whole genome genotype across all loci
*   when we discuss markers, a genotype is the genotype at a given locus
* some historical data capture is desirable and exploring it will provide good use cases for design
* priority must be future focus, setting standards that will facilitate automation, and require meta-data provision as entry requirement
* assume that DNA provenance and identity is handled by KEA
* Many scales
*   very many samples, few markers e.g. commercial kiwi sex and trait markers
*   many markers, many samples e.g. GBS
*   moderate marker number, many samples e.g. SSR typing of populations
*   very many markers , few samples e.g. whole genome sequencing
* Many forms of genotype calls
*   binary 0/1, male/female
*   allele sizes -SSRs
*   0,1,2 etc
*   haplotypes
*   A/C
*   IUPAC 
*   Dosage for polyploids
* DNA provenance is KEA domain, what about genotype provenance? NGS requestor provides scope for experiment meta-data storage but hardly used. Really need to know how raw data and then genotype calls are made.
*   Thoughts on this
*       experiments, sensors and DNA samples are all data sources 
*       can we take a simple-minded approach and just store this as a hash somewhere?
*       eg. say we made genotype calls using a piece of code then reference the GitHub commit hash
*       ..or we could maintain a big data source table with several flavours in Postgres
*       Could ensure uptake because..
*           O provenance means NO databasing
*           Then analysts could have policy of only analysing databased genotype data
* Possible that Kea processes could be used for some of this
* Will need to work out how to assign KEA ids to existing DNA samples i.e. assign a special provenance type -NOT prepped from a KEA tissue sample
* VCF files are emerging as key source of NGS genotype data
* Should establish some standards for compression, naming,sample identity etc as these are the BASE for genetics
* Excellent toolsets for filtering and extracting genotypes, also writing to SQLLite (https://github.com/ekg/vcflib)
