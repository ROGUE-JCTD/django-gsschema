Geoserver Schema
================
A service that allows users to upload/download the geoserver schema.xsd files associated with each layer. More specifically, gsschema is a [Django][1] application which uses the [GeoServer][2] rest api to retrieve the list of layers and then associate a layer with a schema file provided by the user. The schema.xsd file describes a featureType by listing all its attributs as well as the type associated with attribute. The GeoSHAPE project uses the schema file to specify the drop down choices for a given attribute as well as an optional way to indicate that a particular attribute should be populated using datetime picker in [MapLoom][6] (web client) and [Arbiter][5] (mobile client).It is an open-source application that has been developed under the [ROGUE][4] project and is part of the [GeoSHAPE][3] eco-system.

Notes
=============

API Quick Guide
=============


  [1]: http://djangoproject.com "Django"
  [2]: http://geoserver.org "GeoServer"
  [3]: http://geoshape.org "GeoSHAPE"
  [4]: http://github.com/rogue-jctd/ "ROGUE"
  [5]: http://github.com/ROGUE-JCTD/Arbiter-Android "Arbiter"
  [6]: http://github.com/ROGUE-JCTD/MapLoom  "MapLoom"
