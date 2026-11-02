(() => {
  const $ = id => document.getElementById(id);
  let data, result;
  const fmt = n => new Intl.NumberFormat('en-IN', {maximumFractionDigits: 2}).format(n);
  const edgeKey = (a,b) => [a,b].sort().join('|');
  function draw() {
    const svg = $('network'); svg.replaceChildren();
    const ns = 'http://www.w3.org/2000/svg';
    const lats = data.nodes.map(n => n.latitude), lons = data.nodes.map(n => n.longitude);
    const spanX = Math.max(...lons)-Math.min(...lons) || 1, spanY = Math.max(...lats)-Math.min(...lats) || 1;
    const pos = Object.fromEntries(data.nodes.map(n => [n.id, [60 + 480*(n.longitude-Math.min(...lons))/spanX, 300-240*(n.latitude-Math.min(...lats))/spanY]]));
    const mst = new Set((result?.mst.edges || []).map(e => edgeKey(e.source,e.destination)));
    const path = result?.route.path || [], route = new Set(path.slice(1).map((n,i) => edgeKey(path[i],n)));
    const element = (tag, attrs, text) => {const el=document.createElementNS(ns,tag); Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v)); if(text) el.textContent=text; svg.appendChild(el);};
    data.edges.forEach(e => { const [x1,y1]=pos[e.source], [x2,y2]=pos[e.destination], key=edgeKey(e.source,e.destination); element('line',{x1,y1,x2,y2,class:route.has(key)?'line-route':mst.has(key)?'line-mst':'line-road'}); });
    data.nodes.forEach(n => {const [x,y]=pos[n.id]; element('circle',{cx:x,cy:y,r:8,class:'node'}); element('text',{x:x+12,y:y-10,class:'node-label'}, n.name);});
  }
  async function run(e) {
    if (e) e.preventDefault();
    if (!data) return;
    $('run').disabled = true; $('message').textContent = 'Calculating…';
    try {
      const response = await fetch('/api/optimize',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...data, source:$('source').value,destination:$('destination').value,budget:Number($('budget').value)})});
      const json = await response.json(); if(!response.ok) throw new Error(json.error || 'Optimization failed'); result=json;
      $('nodes').textContent=result.network.node_count; $('mst').textContent=fmt(result.mst.weight)+' km' + (result.mst.connected ? '' : ' (forest)'); $('distance').textContent=result.route.distance === null ? 'No route' : fmt(result.route.distance)+' km';
      $('selected-count').textContent=result.stations.selected.length; $('cost').textContent='₹'+fmt(result.stations.total_cost); $('benefit').textContent=fmt(result.stations.total_benefit);
      const names=Object.fromEntries(data.nodes.map(n=>[n.id,n.name])); $('route-text').textContent=result.route.path.map(id=>names[id]).join(' → ') || 'No route available.';
      $('stations').replaceChildren(); result.stations.selected.forEach(s => {const li=document.createElement('li');li.textContent=`${s.station_name} · ₹${fmt(s.installation_cost)} · benefit ${s.benefit}`; $('stations').appendChild(li);});
      if(!result.stations.selected.length) {const li=document.createElement('li');li.textContent='No stations selected for this budget.';$('stations').appendChild(li);}
      $('remaining').textContent='Remaining budget: ₹'+fmt(result.stations.remaining_budget); $('message').textContent=result.mst.connected ? 'Optimization complete.' : `Network disconnected: ${result.mst.components} components. Showing a spanning forest.`; draw();
    } catch(err) { $('message').textContent='Unable to calculate: '+err.message; } finally { $('run').disabled=false; }
  }
  $('planner').addEventListener('submit',run);
  fetch('/api/dataset/small_network').then(r=>{if(!r.ok) throw new Error('Dataset unavailable');return r.json();}).then(json=>{data=json; for(const id of ['source','destination']) data.nodes.forEach(n=>{const opt=document.createElement('option');opt.value=n.id;opt.textContent=n.name;$(id).appendChild(opt)}); $('destination').value=data.nodes[data.nodes.length-1].id; $('network-count').textContent=`${data.nodes.length} nodes / ${data.edges.length} roads`; draw(); run();}).catch(err=>{$('message').textContent='Could not load demo: '+err.message;$('run').disabled=true;});
})();
