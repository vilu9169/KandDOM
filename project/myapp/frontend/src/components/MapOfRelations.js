import React, { useRef, useEffect, useContext } from "react";
import { Container } from "react-bootstrap";
import { Chrono } from "react-chrono";
import { AuthContext } from "./AuthContextProvider";
import Graphin, { Utils } from '@antv/graphin';
// import jsondata from './data.js';
// import { useState } from 'react';


const MapOfRelations= ({ closeMapOfRelations }) => {
  // const graphConfig = {
  //   name: 'Ångströmsnätverket',
  // };
  const mapOfRelationsContainerRef = useRef(null);

  useEffect(() => {
    const handleClickOutsideMapOfRealtions = (event) => {
      if (
        mapOfRelationsContainerRef.current &&
        !mapOfRelationsContainerRef.current.contains(event.target)
      ) {
        closeMapOfRelations();
      }
    };

    // Add event listener to detect clicks outside of the timeline container
    document.addEventListener("mousedown", handleClickOutsideMapOfRealtions);

    return () => {
      // Clean up event listener on component unmount
      document.removeEventListener("mousedown", handleClickOutsideMapOfRealtions);
    };
  }, [closeMapOfRelations]);
  const swedishNames = [
    { name: "Karl", description: "Karl är en enkel soldat" },
    { name: "Johan", description: "Johan är en stor ledare" },
    { name: "Julius", description: "Julius är bror till den stora ledaren Johan" },
    { name: "Elsa", description: "Elsa är en viktig person" },
    { name: "Greta", description: "Greta är en känd person" },
    { name: "Hanna", description: "Hanna är en vänlig person" },
    { name: "Olle", description: "Olle är en snäll person" },
    { name: "Sven", description: "Sven är en hjälte" }
  ];
  
  const nodes = swedishNames.map((person, index) => ({
    id: `Node${index + 1}`,
    data: {
      type: "user",
      description: person.description
    },
    style: {
      label: {
        value: person.name
      }
    }
  }));
  
  const edges = [
    { source: "Node1",
      target: "Node8",
      style: {
      "keyshape": {
        "lineDash": [
          2,
          2
        ],
        "stroke": "#FF6A00"
      },
      "label": {
        "value": "Brother",
        "fill": "#FF6A00"
      }
    } },
    { source: "Node2", target: "Node3" },
    { source: "Node7", target: "Node4" },
    { source: "Node1", target: "Node5" },
    { source: "Node5", target: "Node6" },
    { source: "Node2", target: "Node7" },
    { source: "Node7", target: "Node1" },
    // Add more edges as needed
  ];
  
  const data = {
    nodes,
    edges
  };
  return (
      <Container fluid className="info-container">
        <Container
        ref={mapOfRelationsContainerRef} 
        className="w-75 bg-2 info-window h-80 p-0"
      >
        <Graphin style={{ borderRadius: '5px', border: '3px solid #dac0a3'}} theme={{primaryEdgeColor: '#dac0a3', background:'#eadbc8', primaryColor: '#0f2c59' }} data={data}  layout={{ type: 'dagre' }}/>
        </Container>
      </Container>
    
  );
}
export default MapOfRelations;

//<Graphin graph={graphConfig} />