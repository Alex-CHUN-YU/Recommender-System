name := """RecommenderSystem"""

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayJava)

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  javaJdbc,
  cache,
  javaWs,
  "mysql" % "mysql-connector-java" % "5.0.8"
)
// https://mvnrepository.com/artifact/dom4j/dom4j
libraryDependencies += "dom4j" % "dom4j" % "1.6.1"
// https://mvnrepository.com/artifact/tw.cheyingwu/CKIPClient
libraryDependencies += "tw.cheyingwu" % "CKIPClient" % "0.4.3"
// https://mvnrepository.com/artifact/org.eclipse.persistence/org.eclipse.persistence.moxy
libraryDependencies += "org.eclipse.persistence" % "org.eclipse.persistence.moxy" % "2.5.0"
// https://mvnrepository.com/artifact/net.sf.json-lib/json-lib
libraryDependencies += "net.sf.json-lib" % "json-lib" % "2.4" classifier "jdk15"
// https://mvnrepository.com/artifact/com.googlecode.json-simple/json-simple
libraryDependencies += "com.googlecode.json-simple" % "json-simple" % "1.1"



fork in run := true