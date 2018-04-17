w = 800;			// Width of our visualization
h = 400;			// Height of our visualization
margin = 10;
xOffset = 50;		// Space for x-axis labels
yOffset = 100;		// Space for y-axis labels

d3.csv('metoo_topic_1.csv', function(csvData) {
	data = csvData;

	xScale = d3.scale.linear()
				.domain([d3.min(data, function(d) { return 20000*parseFloat(d['prop'])*Math.cos(0.01745329252*(90*parseFloat(d['score']) + 90)); })-1, 
					d3.max(data, function(d) { return 20000*parseFloat(d['prop'])*Math.cos(0.01745329252*(90*parseFloat(d['score']) + 90)); })+1])
						 //d3.max(data, function(d) { return 20000*d['prop']*Math.cos(90*d['score'] + 90); })+1])
				.range([yOffset + margin, w - margin]);
	yScale = d3.scale.linear()
				.domain([d3.min(data, function(d) { return 20000*parseFloat(d['prop'])*Math.sin(90*parseFloat(d['score']) + 90); })-1, 
					d3.max(data, function(d) { return 20000*parseFloat(d['prop'])*Math.sin(90*parseFloat(d['score']) + 90); })+1])
						 //d3.max(data, function(d) { return 20000*d['prop']*Math.sin(90*d['score'] + 90); })+1])
				.range([h - xOffset - margin, margin]);

var svg = d3.select("#linesSVG").append("svg:svg")
    .attr("width", w)
    .attr("height", h);

	//var line = svg.selectAll('line')
    			//.data(data)
				//.enter().select("#linesSVG").append('svg:svg')

	xAxis = d3.svg.axis()
				.scale(xScale)
				.orient('bottom')
				.ticks(5);
	xAxisG = svg.append('g')
				.attr('class', 'axis')
				.attr('transform', 'translate(0,' + (h - xOffset) + ')')
				.call(xAxis);
	xLabel = svg.append('text')
				.attr('class','label')
				.attr('x', w/2)
				.attr('y', h - 5)
				.text('x/y scale: 20000 times proportion of word times cos/sin of 90 times score of word plus 90 in radians');

	yAxis = d3.svg.axis()
				.scale(yScale)
				.orient('left')
				.ticks(5);
	yAxisG = svg.append('g')
				.attr('class', 'axis')
				.attr('transform', 'translate(' + yOffset + ',0)')
				.call(yAxis);
	yLabel = svg.append('text')
				.attr('class','label')
				.attr('x', yOffset/2)
				.attr('y', h/2-10);


	var line = svg.selectAll('line').data(csvData)
		
	line.enter()
		.append("svg:line")          // attach a line
    	.style("stroke", "black")  // colour the line
    	.attr("x1", xScale(0))     // x position of the first end of the line
    	.attr("y1", yScale(0))      // y position of the first end of the line
    	.attr("x2", function(d) {return xScale(20000*parseFloat(d['prop'])*Math.cos(0.01745329252*(90*parseFloat(d['score']) + 90))); })     // x position of the second end of the line
    	.attr("y2", function(d) {return yScale(20000*parseFloat(d['prop'])*Math.sin(0.01745329252*(90*parseFloat(d['score']) + 90))); });    // y position of the second end of the line
    });