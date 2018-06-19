w = 1000;			// Width of our visualization
h = 500;			// Height of our visualization
margin = 10;
xOffset = 50;		// Space for x-axis labels
yOffset = 100;		// Space for y-axis labels

d3.csv('metoo_stars.csv', function(csvData) {

	data = csvData;

	// functions to get x, y scale values
	function calc_scale_cos(d) {
		return parseFloat(d['x']) + 20000*parseFloat(d['prop'])*Math.cos(0.01745329252*(90*parseFloat(d['score']) + 90));
	}

	function calc_scale_sin(d) {
		return parseFloat(d['y']) + 20000*parseFloat(d['prop'])*Math.sin(0.01745329252*(90*parseFloat(d['score']) + 90));
	}
	xScale = d3.scaleLinear()
				.domain([d3.min(data, function(d) { return calc_scale_cos(d); })-10, 
						 d3.max(data, function(d) { return calc_scale_cos(d); })+10])
						 //d3.max(data, function(d) { return 20000*d['prop']*Math.cos(90*d['score'] + 90); })+1])
				.range([yOffset + margin, w - margin]);
	yScale = d3.scaleLinear()
				.domain([d3.min(data, function(d) { return calc_scale_sin(d); })-10, 
						 d3.max(data, function(d) { return calc_scale_sin(d); })+10])
						 //d3.max(data, function(d) { return 20000*d['prop']*Math.sin(90*d['score'] + 90); })+1])
				.range([h - xOffset - margin, margin]);

	var svg = d3.select("#linesSVG").append("svg:svg")
		.attr("width", w + 100)
		.attr("height", h);

	//var line = svg.selectAll('line')
    			//.data(data)
				//.enter().select("#linesSVG").append('svg:svg')

	domain = 10000
	var colorScale = d3.scaleSequential()
		.domain([1, -1])
		.interpolator(d3.interpolateCool);

	xAxis = d3.axisBottom()
				.scale(xScale)
				//.orient('bottom')
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

	yAxis = d3.axisLeft()
				.scale(yScale)
				//.orient('left')
				.ticks(5);
	yAxisG = svg.append('g')
				.attr('class', 'axis')
				.attr('transform', 'translate(' + yOffset + ',0)')
				.call(yAxis);
	yLabel = svg.append('text')
				.attr('class','label')
				.attr('x', yOffset/2)
				.attr('y', h/2-10);

	var legendSequential = d3.legendColor()
		.title('Scaled Expected Sentiment of Topic')
		.titleWidth(50)
	    .shapeWidth(30)
	    .shapeHeight(20)
	    .labelOffset(15)
	    .cells([1.0, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8, -1.0])
	    .shapePadding(5)
	    .orient("vertical")
	    .scale(colorScale) 

	svg.append("g")
  		.attr("class", "legendSequential")
  		.attr("transform", 'translate(' + (w + 20) + ', 20)')
  		.call(legendSequential);


svg.select(".legendSequential")
  .call(legendSequential);

	var line = svg.selectAll('line').data(csvData)
		
	line.enter()
		.append("svg:line")          // attach a line
    	//.style("stroke", "black")  // colour the line
    	.attr("x1", function(d) {return xScale(parseFloat(d['x']));})     // x position of the first end of the line
    	.attr("y1", function(d) {return yScale(parseFloat(d['y']));})       // y position of the first end of the line
    	.attr("x2", function(d) {return xScale(calc_scale_cos(d)); })     // x position of the second end of the line
    	.attr("y2", function(d) {return yScale(calc_scale_sin(d)); })    // y position of the second end of the line
    	.style('stroke', function(d) {return colorScale(parseFloat(d['expected_scaled'])); })
    	//colorScale(parseInt((domain + domain*parseFloat(d['expected_scaled'])) / 2));
    	.style("stroke-opacity", "0.2")
    	.on("mouseover", mouseover)
    	.on("mouseout", mouseout);

    function mouseover(d, i) {

        d3.select(this).style("opacity", "1")
                       .attr("stroke-width", 3);

        $("#id1").text(d['word']);
        $("#id2").text(d['topic']);
        $("#id3").text(parseFloat(d['score']).toFixed(4));
        $("#id4").text(d['count']);
        
        $("#id5").text(parseFloat(d['prop']).toFixed(5));

   };

   function mouseout(d, i) {

        d3.select(this).style("stroke", function(d) { return colorScale(parseFloat(d['expected_scaled'])); })
                       .style("stroke-opacity", "0.2")
                       .attr("stroke-width", 1);

        $("#id1").html("&nbsp");
        $("#id2").html("&nbsp");
        $("#id3").html("&nbsp");
        $("#id4").html("&nbsp");
        $("#id5").html("&nbsp");

   };

    });
