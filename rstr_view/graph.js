//visualization 12/7
function showGraph(title, clist, emlist, evlist, llist, tlist){
  var graphArea = $("#show-graph");
  //graphArea.empty();
  d3.select("body").selectAll("svg").remove();
  var w = 1500;
    var h = 800;
    var linkDistance=200;
  
  clist = d3.set(clist);
  tlist = d3.set(tlist);
  emlist = d3.set(emlist);
  llist = d3.set(llist);
  var dataset = {
    'people':new Array(),
    'time':new Array(),
    'emotion':new Array(),
    'location':new Array(),
    'nodes':[{name: title, type: "none"}],
    'edges': new Array()
    };
  list2node(dataset, evlist, "event");
  list2node(dataset, emlist, "emotion");
  list2node(dataset, clist, "person");
  list2node(dataset, llist, "location");
  list2node(dataset, tlist, "time");
  dataset['nodes'].forEach(function(entry, i) 
  {
    var singleObj = {};
    switch(entry.type)
    {
      case 'person':
        singleObj['source'] = 0;
        singleObj['target'] = i;
        dataset['edges'].push(singleObj);
        break;
      case 'emotion':
        singleObj['source'] = 0;
        singleObj['target'] = i;
        dataset['edges'].push(singleObj);
        break;
      case 'event':
        singleObj['source'] = i-1;
        singleObj['target'] = i;
        dataset['edges'].push(singleObj);
        break;
      case 'location':
        singleObj['source'] = 0;
        singleObj['target'] = i;
        dataset['edges'].push(singleObj);
        break;
      case 'time':
        singleObj['source'] = 0;
        singleObj['target'] = i;
        dataset['edges'].push(singleObj);
        break;
      default:
        break;
    } 
  });
  //console.log(dataset.edges);
    //var colors = d3.scale.category10();
 
    var svg = d3.select("body").append("svg").attr({"width":w,"height":h});

    var force = d3.layout.force()
        .nodes(dataset.nodes)
        .links(dataset.edges)
        .size([w,h])
        .linkDistance([linkDistance])
        .charge([-500])
        .theta(0.1)
        .gravity(0.05)
        .start();

 

    var edges = svg.selectAll("line")
      .data(dataset.edges)
      .enter()
      .append("line")
      .attr("id",function(d,i) {return 'edge'+i})
      .attr('marker-end','url(#arrowhead)')
      .style("stroke","#ccc")
      .style("pointer-events", "none");
    
    var nodes = svg.selectAll("circle")
      .data(dataset.nodes)
      .enter()
      .append("ellipse")
      .attr("rx", function(d,i){return i===0?100:40})
    .attr("ry", function(d,i){return i===0?75:30})
      .style("fill",function(d,i)
    {
    if(i===0)
      return "#FF6600";
    switch(d.type)
    {
      case 'person':
        return 'yellow';
        break;
      case 'emotion':
        return 'red';
        break;
      case 'event':
        return "#6699FF";
        break;
      case 'location':
        return 'white';
        break;
      case 'time':
        return 'green';
        break;
      default:
        break;
    }
    })
      .call(force.drag)


    var nodelabels = svg.selectAll(".nodelabel") 
       .data(dataset.nodes)
       .enter()
       .append("text")
       .attr({"x":function(d){return d.x;},
              "y":function(d){return d.y;},
              "class":"nodelabel",
        "font-size":15,
        "text-anchor":"middle",
              "stroke":"black"})
       .text(function(d){return d.name;});

    var edgepaths = svg.selectAll(".edgepath")
        .data(dataset.edges)
        .enter()
        .append('path')
        .attr({'d': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
               'class':'edgepath',
               'fill-opacity':0,
               'stroke-opacity':0,
               'fill':'#ccc',
               'stroke':'red',
               'id':function(d,i) {return 'edgepath'+i}})
        .style("pointer-events", "none");

    var edgelabels = svg.selectAll(".edgelabel")
        .data(dataset.edges)
        .enter()
        .append('text')
        .style("pointer-events", "none")
        .attr({'class':'edgelabel',
               'id':function(d,i){return 'edgelabel'+i},
               'dx':80,
               'dy':0,
               'font-size':13,
               'fill':'#aaa'});

    edgelabels.append('textPath')
        .attr('xlink:href',function(d,i) {return '#edgepath'+i})
        .style("pointer-events", "none")
        .text(function(d,i)
    {
      switch(d.target.type)
      {
        case 'person':
          return '相關人物';
          break;
        case 'emotion':
          return '情緒';
          break;
        case 'event':
          return '事件'+(i+1);
          break;
        case 'location':
          return '地點';
          break;
        case 'time':
          return '時間';
          break;
        default:
          break;
      }
      //console.log(d);
    });


    svg.append('defs').append('marker')
        .attr({'id':'arrowhead',
               'viewBox':'-0 -5 10 10',
               'refX':25,
               'refY':0,
               //'markerUnits':'strokeWidth',
               'orient':'auto',
               'markerWidth':20,
               'markerHeight':20,
               'xoverflow':'visible'})
        .append('svg:path')
            .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
            .attr('fill', '#ccc')
            .attr('stroke','#ccc');
     

    force.on("tick", function(){

        edges.attr({"x1": function(d){return d.source.x;},
                    "y1": function(d){return d.source.y;},
                    "x2": function(d){return d.target.x;},
                    "y2": function(d){return d.target.y;}
        });

        nodes.attr({"cx":function(d){return d.x;},
                    "cy":function(d){return d.y;}
        });

        nodelabels.attr("x", function(d) { return d.x; }) 
                  .attr("y", function(d) { return d.y; });

        edgepaths.attr('d', function(d) { var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
                                           //console.log(d)
                                           return path});       

        edgelabels.attr('transform',function(d,i){
            if (d.target.x<d.source.x){
                bbox = this.getBBox();
                rx = bbox.x+bbox.width/2;
                ry = bbox.y+bbox.height/2;
                return 'rotate(180 '+rx+' '+ry+')';
                }
            else {
                return 'rotate(0)';
                }
        });
    });
}

function list2node(dataset, list, type)
{
  list.forEach(function(entry) 
  {
    var singleObj = {}
    singleObj['name'] = entry;
    singleObj['type'] = type;
    dataset['nodes'].push(singleObj);
  })
} 