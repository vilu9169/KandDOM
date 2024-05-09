import React, { useRef, useEffect, useContext } from "react";
import { Container } from "react-bootstrap";
import { Chrono } from "react-chrono";
import { AuthContext } from "./AuthContextProvider";
import Graphin, { Utils } from '@antv/graphin';
// import jsondata from './data.js';
// import { useState } from 'react';

const MapOfRelations= () => {
  // const graphConfig = {
  //   name: 'Ångströmsnätverket',
  // };
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
    <div className="App" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: '80vw', height: '80vh' }}>
      <div style={{ width: '100%', height: '100%', border: '1px solid black' }}>
        <Graphin data={data} style={{ width: '100%', height: '100%' }} layout={{ type: 'dagre' }}/>
      </div>
    </div>
  );
}
export default MapOfRelations;

//<Graphin graph={graphConfig} />