Sesame is a flexible Triplestore server, hosted at OpenRDF (http://www.openrdf.org/).

Required Software:
- Java
- Java Servlet Container, Apache Tomcat (http://tomcat.apache.org/) is recommended.

Installation:
1) Download it from http://www.openrdf.org/download.jsp
- It comes with 2 Web Arcieve (WAR) files: 
	+ Sesame (HTTP) server (openrdf-sesame.war)
	+ OpenRDF Workbench (openrdf-workbench.war)

2) Deploy those WARs into the Java Servlet Container
For Tomcat:
- Use Tomcat Application Manager
- Put them into the Tomcat Webapps folder

3) Access Point:
- Workbench : http://localhost:8080/openrdf-workbench
- SPARQL Endpoint: http://localhost:8080/openrdf-sesame/repositories/<REPOSITORY-ID>

Repository:
By Default, the repository of the Sesame server is located at $HOME/.aduna/openrdf-sesame/repositories/
