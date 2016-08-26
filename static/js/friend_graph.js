function execute() {

$.ajax({
    beforeSend: function () {
        $(".loader").show(300);
    },
    url: '/get_username',
    data: $('form').serialize(),
    type: 'POST',
    success: function (response) {
        $(".loader").animate(
            {'width': 0, 'height':0}, 300,
            function () {
                $(".loader").hide();
                $("#mainDiv").show().animate({
                    "opacity": 1
                })
            }
        )
        links = response['links'];
        nodes = response['nodes'];

        var svg = d3.select("#mainDiv"),
            width = +svg.attr("width"),
            height = +svg.attr("height");

        var color = d3.scaleOrdinal(d3.schemeCategory20);

        var simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function (d) {
                return d.id;
            }))
            .force("charge", d3.forceManyBody().strength(-250))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("x", d3.forceX())
            .force("Y", d3.forceY());

        var link = svg.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("x2", 0.5)
            .attr("stroke-width", function (d) {
                return Math.sqrt(d.value);
            })
            .attr("stroke", function (d) {
                return d.co;
            });

        var node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", function (d) {
                return d.Size;
            })
            .attr("fill", function (d) {
                return 'mintcream'
            })
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        node.append("title")
            .text(function (d) {
                return d.id;
            });

        simulation
            .nodes(nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(links);

        function ticked() {
            link
                .attr("x1", function (d) {
                    return d.source.x;
                })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            node
                .attr("cx", function (d) {
                    return d.x;
                })
                .attr("cy", function (d) {
                    return d.y;
                });
        }

        function dragstarted(d) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(d) {
            d.fx = d3.event.x;
            d.fy = d3.event.y;
        }

        function dragended(d) {
            if (!d3.event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    },
    error: function (error) {
        console.log(error)
    }
});

}