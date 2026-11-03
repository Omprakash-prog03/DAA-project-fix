// UI only: all three algorithms live in the Python algorithms/ directory.
(() => {
  const byId = id => document.getElementById(id);
  const money = amount => '₹' + new Intl.NumberFormat('en-IN').format(amount);
  const svgNamespace = 'http://www.w3.org/2000/svg';
  let demo;
  let routeEdges = new Set();
  let mstEdges = new Set();

  function edgeKey(a, b) { return [a, b].sort().join('-'); }

  function svgElement(name, attributes, text) {
    const element = document.createElementNS(svgNamespace, name);
    for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function drawGraph() {
    const svg = byId('graph-svg');
    svg.replaceChildren();
    const points = Object.fromEntries(demo.nodes.map(node => [node.id, node]));
    for (const edge of demo.edges) {
      const a = points[edge.source], b = points[edge.destination];
      const key = edgeKey(edge.source, edge.destination);
      const onRoute = routeEdges.has(key), onTree = mstEdges.has(key);
      const style = onRoute && onTree ? 'both' : onRoute ? 'path' : onTree ? 'tree' : 'road';
      svg.appendChild(svgElement('line', {x1:a.x, y1:a.y, x2:b.x, y2:b.y, class:style}));
      const x = (a.x + b.x) / 2, y = (a.y + b.y) / 2;
      svg.appendChild(svgElement('circle', {cx:x, cy:y, r:14, class:'weight-bg'}));
      svg.appendChild(svgElement('text', {x, y:y+5, class:'weight-text'}, String(edge.weight)));
    }
    for (const node of demo.nodes) {
      svg.appendChild(svgElement('circle', {cx:node.x, cy:node.y, r:23, class:'node-circle'}));
      svg.appendChild(svgElement('text', {x:node.x, y:node.y+6, class:'node-text'}, node.id));
    }
  }

  function showSteps(id, steps) {
    const list = byId(id);
    list.replaceChildren();
    steps.forEach(step => { const item = document.createElement('li'); item.textContent = step; list.appendChild(item); });
  }

  async function post(url, body) {
    const response = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Could not calculate the result.');
    return result;
  }

  function showError(target, error) {
    byId(target).textContent = error.message || 'Something went wrong.';
  }

  byId('route-form').addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const start = byId('start').value, end = byId('end').value;
      const result = await post('/api/demo/dijkstra', {source:start, destination:end});
      byId('route-result').replaceChildren();
      const path = document.createElement('strong'); path.className = 'result-primary';
      path.textContent = result.path.length ? result.path.join(' → ') : 'No route found';
      const distance = document.createElement('p'); distance.textContent = result.distance === null ? 'The destination is unreachable.' : `Total distance: ${result.distance}`;
      const visited = document.createElement('p'); visited.textContent = `Visited nodes: ${result.visited.join(', ')}`;
      byId('route-result').append(path, distance, visited);
      showSteps('route-steps', [`Start at ${start} with distance 0.`, ...result.steps, result.path.length ? `Reconstruct the path: ${result.path.join(' → ')}.` : 'The destination is unreachable.']);
      routeEdges = new Set(result.path.slice(1).map((node, i) => edgeKey(result.path[i], node)));
      drawGraph();
    } catch (error) { showError('route-result', error); }
  });

  byId('mst-button').addEventListener('click', async () => {
    try {
      const result = await post('/api/demo/kruskal', {});
      byId('mst-result').replaceChildren();
      const list = document.createElement('ul'); list.className = 'result-list';
      result.edges.forEach(edge => { const item=document.createElement('li'); item.textContent=`${edge.source} — ${edge.destination} : ${edge.weight}`; list.appendChild(item); });
      const total = document.createElement('p'); total.textContent = `Total MST cost: ${result.total}`;
      byId('mst-result').append(list,total);
      showSteps('mst-steps', ['Sort all roads by weight.', ...result.steps, `The tree has total cost ${result.total}.`]);
      mstEdges = new Set(result.edges.map(edge => edgeKey(edge.source, edge.destination)));
      drawGraph();
    } catch (error) { showError('mst-result', error); }
  });

  function displayTable(result) {
    const container = byId('dp-table'); container.replaceChildren();
    const description = document.createElement('p'); description.className='hint';
    description.textContent = `DP table: best benefit for each budget. Column values are in units of ${money(result.unit)}. The table ends at the smaller of the budget and total candidate costs.`;
    const table = document.createElement('table');
    const header = document.createElement('tr');
    for (const heading of ['Stations', ...result.table[0].map((_, index) => String(index))]) {
      const cell=document.createElement('th'); cell.textContent=heading; header.appendChild(cell);
    }
    table.appendChild(header);
    result.table.forEach((row, index) => {
      const tr=document.createElement('tr');
      const label=document.createElement('th'); label.textContent=index === 0 ? 'None' : `Through ${result.candidates[index-1]}`; tr.appendChild(label);
      row.forEach(value => {const cell=document.createElement('td'); cell.textContent=value; tr.appendChild(cell);});
      table.appendChild(tr);
    });
    container.append(description, table);
  }

  byId('station-form').addEventListener('submit', async event => {
    event.preventDefault();
    try {
      const budget = Number(byId('budget').value);
      if (!Number.isSafeInteger(budget) || budget < 0) throw new Error('Enter a non-negative whole-number budget.');
      const station_ids = [...document.querySelectorAll('.station-checkbox:checked')].map(box => box.value);
      const result = await post('/api/demo/knapsack', {budget, station_ids});
      byId('station-result').replaceChildren();
      const selected=document.createElement('strong'); selected.className='result-primary';
      selected.textContent = result.selected.length ? result.selected.map(station => station.station_name).join(', ') : 'No stations selected';
      const totals=document.createElement('p'); totals.textContent=`Total cost: ${money(result.cost)} · Total benefit: ${result.benefit}`;
      const remaining=document.createElement('p'); remaining.textContent=`Budget remaining: ${money(result.remaining)}`;
      byId('station-result').append(selected,totals,remaining);
      showSteps('station-steps', [`Start with budget ${money(budget)} and ${station_ids.length} candidates.`, `Fill the table: compare excluding each station with including it once.`, `Backtrack through the table to find ${result.selected.length} selected station(s).`, `Their cost is ${money(result.cost)} and benefit is ${result.benefit}.`]);
      displayTable(result);
    } catch (error) { showError('station-result', error); }
  });

  async function init() {
    try {
      const response = await fetch('/api/demo');
      if (!response.ok) throw new Error('Could not load the demonstration data.');
      demo = await response.json();
      for (const id of ['start', 'end']) {
        demo.nodes.forEach(node => { const option=document.createElement('option'); option.value=node.id; option.textContent=node.id; byId(id).appendChild(option); });
      }
      byId('end').value = 'E';
      for (const station of demo.stations) {
        const label=document.createElement('label'); label.className='station-card';
        const checkbox=document.createElement('input'); checkbox.className='station-checkbox'; checkbox.type='checkbox'; checkbox.value=station.station_id; checkbox.checked=true;
        const title=document.createElement('strong'); title.textContent=station.station_name;
        const cost=document.createElement('span'); cost.textContent=`Cost ${money(station.installation_cost)}`;
        const benefit=document.createElement('span'); benefit.textContent=`Benefit ${station.benefit}`;
        const checkLabel=document.createElement('span'); checkLabel.className='check-label'; checkLabel.append(checkbox, document.createTextNode(' Include as candidate'));
        label.append(title,cost,benefit,checkLabel); byId('station-cards').appendChild(label);
      }
      drawGraph();
    } catch (error) { byId('status').textContent=error.message; }
  }
  init();
})();
