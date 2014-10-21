Information-Retrieval
=====================

CS 6200

=================================================================================================================================

crawler.py

A simple web crawler that reads web pages till depth 3 from the seed page. It is also equiped with focused crawling (Crawler looks 
for a phrase in the document, if the phrase is present then it scans child pages else skips current page)


=================================================================================================================================

pagerank.py

given a file with graph nodes represented in inlink format, gives page rank for all the nodes

there are two options for calculating pagerank
1. till page rank converges
2. for n iterations
