Geoserver Schema
================
A service that allows users to upload/download the geoserver schema.xsd files associated with each layer. More specifically, gsschema is a [Django][1] application which uses the [GeoServer][2] rest api to retrieve the list of layers and then associate a layer with a schema file provided by the user. The schema.xsd file describes a featureType by listing all its attributs as well as the type associated with attribute. The GeoSHAPE project uses the schema file to specify the drop down choices for a given attribute as well as an optional way to indicate that a particular attribute should be populated using datetime picker in [MapLoom][6] (web client) and [Arbiter][5] (mobile client).It is an open-source application that has been developed under the [ROGUE][4] project and is part of the [GeoSHAPE][3] eco-system.

Notes
=============
- A "normal" schema can be defined as such:

*Hospitals1*
```
<?xml version="1.0" encoding="UTF-8"?><xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:geonode="http://www.geonode.org/" xmlns:gml="http://www.opengis.net/gml" elementFormDefault="qualified" targetNamespace="http://www.geonode.org/">
  <xsd:import namespace="http://www.opengis.net/gml" schemaLocation="http://<VM IP Address>/geoserver/schemas/gml/3.1.1/base/gml.xsd"/>
  <xsd:complexType name="Hospitals1Type">
    <xsd:complexContent>
      <xsd:extension base="gml:AbstractFeatureType">
        <xsd:sequence>
          <xsd:element maxOccurs="1" minOccurs="0" name="geometry" nillable="true" type="gml:PointPropertyType"/>
          <xsd:element maxOccurs="1" minOccurs="0" name="name" nillable="true" type="xsd:string"/>
          <xsd:element maxOccurs="1" minOccurs="0" name="status" nillable="true">
            <xsd:simpleType>
              <xsd:restriction base="xsd:string">
                <xsd:enumeration value="open"/>
                <xsd:enumeration value="closed"/>
              </xsd:restriction>
            </xsd:simpleType>
          </xsd:element>
          <xsd:element maxOccurs="1" minOccurs="0" name="number_of_beds_available" nillable="true" type="xsd:long"/>
          <xsd:element maxOccurs="1" minOccurs="0" name="number_of_beds_total" nillable="true" type="xsd:long"/>
          <xsd:element maxOccurs="1" minOccurs="0" name="fotos" nillable="true" type="xsd:string"/>
        </xsd:sequence>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
  <xsd:element name="Hospitals1" substitutionGroup="gml:_Feature" type="geonode:Hospitals1Type"/>
</xsd:schema>
```

- The main lines that are going to be edited are the 'xsd:element' sections.
- The attribute 'type' inside the 'xsd:element' has many options, such as the following:
    - 'xsd:date'
    - 'xsd:dateTime'
    - 'xsd:long'
    - 'xsd:string'
    - Any other supported 'xsd' type.

API Quick Guide
=============
Since schemas are already created (and each layer is using their own respective schema on MapLoom), GSSchema gives the user the ability to edit any available schema.
To start, you can log onto GSSchema:

*The user **_must_** be logged into GeoSHAPE.*

**example: http://192.168.99.100/gsschema/**

**/gsschema/**
-------------
You will be presented with a dropdown list, containing each layer that Geonode holds.
One a layer is selected, a few action buttons will be presented. These buttons are listed in order of a normal use of GSSchema.

*Describe FeatureType*
-------
This button will allow you to download the schema that is currently being used for the selected layer. After downloading the schema, any text editor can be used to edit the schema and be uploaded with the next button. Editing tips will be covered in [this document][7].

*Upload*
-------
Once a file is chosen for upload, this button will be enabled. This will upload the schema to Geoserver (while immediately reflecting on MapLoom) and make a local backup on the machine. This will then enable the **Download** and **Remove** buttons if it is successfully uploaded.

- Expected results for upload:
    - Successful
    - Error Uploading: "Invalid file" (Non-XML format, not '.xsd')
    - Error Uploading: "Invalid schema"

*Download*
------
This button allows you to download a schema that you previously uploaded through /gsschema/. This schema is local to the machine, and if no schemas have been uploaded, this button will be disabled.

*Remove*
-------
This will remove the currently selected layer's schema that is *local to the machine*. It will prompt the user with a window confirming if they want to remove the file. This button will be disabled if there is not a previous schema uploaded for that layer.



  [1]: http://djangoproject.com "Django"
  [2]: http://geoserver.org "GeoServer"
  [3]: http://geoshape.org "GeoSHAPE"
  [4]: http://github.com/rogue-jctd/ "ROGUE"
  [5]: http://github.com/ROGUE-JCTD/Arbiter-Android "Arbiter"
  [6]: http://github.com/ROGUE-JCTD/MapLoom  "MapLoom"
  [7]: https://docs.google.com/document/d/1gz0qHIhY0LT2xceRX8gpXDCwbOxshzmbLXCu48Tz-MM/edit
