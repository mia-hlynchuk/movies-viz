console.log('Hello from the forceGraph file');
const graph = d3.select('#graph');
const width = graph.attr('width');
const height = graph.attr('height');

let nodesData = [];
let linksData = [];

let node;
let link;

d3.json('data/force_data.json')
  .then((data) => {
    console.log(data);

    // holds our data
    nodesData = data.nodes;
    linksData = data.links;

    // console.table(nodesData);
    // console.table(linksData);

    console.log(`Nodes: ${nodesData.length}`);
    console.log(`Links: ${linksData.length}`);

    // set up the simulation        
    const simulation = d3.forceSimulation(nodesData);

    // add two forces to the simulation: charge and center        
    simulation
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(width / 2, height / 2));

    // create the link force
    const linkForce = d3.forceLink(linksData)
      .id(d => d.index);

    // add the link force to the simulation
    simulation.force('links', linkForce);
    simulation.on('tick', tickActions);

    // draw the lines (links)
    link = graph.append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(linksData)
      .enter()
      .append('line')
      .attr('stroke-width', '.01');

    // draw the circles (nodes)
    node = graph.append('g')
      .attr('class', 'nodes')
      .selectAll('circle')
      .data(nodesData)
      .enter()
      .append('circle')
      .attr('r', 0.05)
      .attr('fill', (d) => {
        if (d.type == 'movie') return 'red';
        else if (d.type == 'actor') return 'blue';
        return 'green';
      })
      .attr('class', (d) => {
        if (d.type == 'movie') return 'movie';
        else if (d.type == 'actor') return 'actor';
      })
      .attr('id', d => d.id)
      .attr('name', d => d.name);
  });


function tickActions() {
  // update the circle positions for each tick
  node
    .attr('cx', d => d.x)
    .attr('cy', d => d.y);

  // update link positions 
  link
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y);
}

