w = 1000;			// Width of our visualization
h = 500;			// Height of our visualization
margin = 10;
xOffset = 50;		// Space for x-axis labels
yOffset = 100;		// Space for y-axis labels

d3.csv('tweets_stars.csv', function(csvData) {

	data = csvData.filter(function(d){ return (+d['topic'] == 8);});

	// functions to get x, y scale values; *const* is for adjusting coordinates for rotating
	function calc_scale_cos(d, c) {
		return -(20000*(+d['prop']) + c) *Math.cos(0.01745329252*(90*(+d['score']) + 90));
	}

	function calc_scale_sin(d, c) {
		return (20000*(+d['prop']) + c) *Math.sin(0.01745329252*(90*(+d['score']) + 90));
	}
	xScale = d3.scaleLinear()
				.domain([d3.min(data, function(d) { return calc_scale_cos(d, 0); })-100, //100 is also a constant to be adjusted based on 20000
						 d3.max(data, function(d) { return calc_scale_cos(d, 0); })+100])
				.range([yOffset + margin, w - margin]);
	yScale = d3.scaleLinear()
				.domain([d3.min(data, function(d) { return calc_scale_sin(d, 0); })-100, 
						 d3.max(data, function(d) { return calc_scale_sin(d, 0); })+100])
				.range([h - xOffset - margin, margin]);

	var svg = d3.select("#linesSVG").append("svg:svg")
		.attr("width", w + 100)
		.attr("height", h);

	domain = 10000
	var colorScale = d3.scaleSequential()
		.domain([1, -1])
		.interpolator(d3.interpolateRdYlBu);

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

	var line = svg.selectAll('.starLine').data(data)
		
	line.enter()
		.append("svg:line")          // attach a line
    	//.style("stroke", "black")  // colour the line
    	.attr("class", "starLine")
    	.attr("x1", function(d) {return xScale(0);})     // x position of the first end of the line
    	.attr("y1", function(d) {return yScale(0);})       // y position of the first end of the line
    	.attr("x2", function(d) {return xScale(calc_scale_cos(d, 0)); })     // x position of the second end of the line
    	.attr("y2", function(d) {return yScale(calc_scale_sin(d, 0)); })    // y position of the second end of the line
    	.style('stroke', function(d) {return colorScale(+d['score']); })
    	//colorScale(parseInt((domain + domain*parseFloat(d['expected_scaled'])) / 2));
    	.style('stroke-width', 2)
    	.style("stroke-opacity", 0.5)
    	.on("mouseover", mouseover)
    	.on("mouseout", mouseout);

    function rotateHelper(d) {
    	if (+d['score'] >= 0 && +d['score'] < 1) 
            {return 90*(+d['score']) - 90;} //5 is an adjusting constant
        else if (+d['score'] == -1) {return 0;}
        else {return 90*(+d['score']) - 270;}
    }

    var text = svg.selectAll(".word")
                .data(data)
                .enter()
                .append("text")
                .attr('class', 'word')
                .attr('x', function(d) {if (+d['score'] >= 0) {return xScale(calc_scale_cos(d, 0));}
                						else {return xScale(calc_scale_cos(d, 0));}})
                .attr('y', function(d) {if (+d['score'] >= 0) {return yScale(calc_scale_sin(d, 0));}
                						else {return yScale(calc_scale_sin(d, 0));}})
                .attr("font-family", "sans-serif")
                .attr("font-size", "10px")
                .attr("fill", "black")
                .text(function(d) { if (+d['prop'] > 0.005) {return d['word']; }})
                .attr('transform', function(d) {return "rotate(" + rotateHelper(d) + "," +
            										d3.select(this).attr("x") + "," + 
            										d3.select(this).attr("y") + ")"})
                .attr("text-anchor", function(d) {if (+d['score'] >= 0) return "start";
            									  else return "end";});


d3.select("#slider")
	.on("input", function() {
  //text.text(function(d) { if (parseFloat(d['prop']) > 0.005) {return d['word']; }})
  update(+this.value);
});




// update the elements
	function update(prop) {

		var select = svg.selectAll('.word')
		.text(function(d) { if (+d['prop'] > prop) {return d['word']; }})}


                /*
	  // adjust the text on the range slider
	  d3.select("props-value").text(prop);
	  d3.select("props").property("value", prop);

	  // update the rircle radius
	  d3.selectAll(".word") 
	  	.exit()
	  	.remove()

	  d3.append("text")
	  	.enter()
	    .text(function(d) { if (parseFloat(d['prop']) > prop) {return d['word']; }}); //give slider input)
	}*/


    function mouseover(d, i) {

        d3.select(this).style("stroke-opacity", 0.7)
                       .attr("stroke-width", 3.5);

        $("#id1").text(d['word']);
        $("#id2").text(d['topic']);
        $("#id3").text((+d['score']).toFixed(4));
        $("#id4").text(d['count']);
        
        $("#id5").text((+d['prop']).toFixed(5));

   };

   function mouseout(d, i) {

        d3.select(this).style("stroke", function(d) { return colorScale(+d['score']); })
                       .style("stroke-opacity", 0.5)
                       .attr("stroke-width", 2);

        $("#id1").html("&nbsp");
        $("#id2").html("&nbsp");
        $("#id3").html("&nbsp");
        $("#id4").html("&nbsp");
        $("#id5").html("&nbsp");

   };

    });
