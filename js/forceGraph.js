console.log('Hello from force graph v2');

const svg = d3.select('svg');
const width = +svg.attr('width');
const height = +svg.attr('height');

const radius = 5;
const groupFilter = 1;

d3.json('data/force_data.json').then((data) => {
  console.log(data);

  const nodesData = data.nodes;
  const linksData = data.links;

  const simulation = d3.forceSimulation(nodesData)
    .force('charge', d3.forceManyBody().strength(-150)) 
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('x', d3.forceX(width / 2).strength(1))
    .force('y', d3.forceY(height / 2).strength(1))
    .force('link', d3.forceLink(linksData).id(d => d.index).distance(100).strength(2))
    .on('tick', ticked);

  const link = svg.append('g').attr('class', 'links')
    .selectAll('line')
    .data(linksData)
    .enter()
    // .filter((d) => { return d.value == groupFilter; })
    .filter((d) => { return d.show === true; })
    .append('line');

  const node = svg.append('g').attr('class', 'nodes')
    .selectAll('g')
    .data(nodesData)
    .enter()
    // .filter((d) => { return d.type == 'movie'; })
    // .filter((d) => { return d.group == groupFilter; })
    .filter((d) => {
      if (d.type === 'actor') {
        return d.show === true;
      }
      return d.type === 'movie';
    })
    .append('g')
    .attr('class', (d) => { return d.type; })
    .attr('name', (d) => { return d.name; });

  node.append('circle')
    .attr('r', radius);

  node.append('text')
    .text(d => `${d.name} (${d.group})`);

  function ticked() {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    node.selectAll('circle')
      .attr('cx', (d) => { return d.x = Math.max(radius, Math.min(width - radius, d.x)); })
      .attr('cy', (d) => { return d.y = Math.max(radius, Math.min(height - radius, d.y)); });

    node.selectAll('text')
      .attr('dx', (d) => { return d.x = Math.max(radius, Math.min(width - 10, d.x)); })
      .attr('dy', (d) => { return d.y = Math.max(radius, Math.min(height - 10, d.y)); });
  }
});
