
var message_box = function(node) {
    var self = this;

    var init = function(node) {
        var element = $(document.createElement('div'))
            .addClass('message-box')
            .append($(document.createElement('h3')).text('CONSOLE'));
        node.append(element);

        self.node = element;
    };

    self.message = function(msg) {
        var element = $(document.createElement('div'));

        element.addClass('message').text(msg);
        self.node.append(element);
    };

    init(node);
};

Array.prototype.remove = function(from, to) {
  var rest = this.slice((to || from) + 1 || this.length);
  this.length = from < 0 ? this.length + from : from;
  return this.push.apply(this, rest);
};

/**
 * Plot with two independent variables
 * and two dependent variables
 */
var aligned_plot_4d = function(node) {
    var self = this;
    self.container = node;

    (function() {
        var element = $(document.createElement('div'))
            .attr('id', 'console')
            .addClass('graph-item');
        node.append(element);

        console.log(element);
        self.messages = new message_box(element);
    })();

    console.log(44, self.messages);


    var margin = {
        'left': 20,
        'right': 20,
        'top': 20,
        'bottom': 20
    };
    var radius = 20;
    var legend_dimens = {
        'width': 20,
        'tick_margin': 40,
        'offset': 10
    };

    var legend_count = 0;
    var colormaps = {
        'purity': 'viridis_r',
        'p': 'viridis',
        'completeness': 'viridis'
    };

    var dimens = {
        'height': null,
        'width': null
    };

    self.plot = function(data) {
        var chart = d3.select(self.container.get(0));
        var svg = init_svg(chart, data);

        var stats = genDataStats(data.points);

        add_gradients(svg, data, stats);
        add_points(svg, data);

        add_legends(svg, data.axes, stats);
    };

    /**
     * Generate the text for the tooltip on mouse hover
     */
    var tip_text = function(d) {

        /**
         * Generate a jquery node from raw html
         * Append it to a jquery <div> block and
         * then get the inner html
         */
        var html = function(element) {
            return $('<div/>').append(element).html();
        };

        var value_span = function(text) {
            return html($('<span/>', {
                class: 'tip-detail',
                text: text
            }));
        };

        var title_block = function(id) {
            var elements = [];

            var text = '';
            for (var key in id) {
                var value = id[key];
                text = text + ' ' + key + ' ' + value_span(value);
            }
            text = $('<div>' + text + '</div>');
            text.attr('id', 'title').addClass('tip-line tip-values');
            // console.log(html(text))

            return html(text);
        };

        var value_line = function(name, values) {
            values = values.slice();
            for (var n in values)
                values[n] = parseFloat(values[n]).toFixed(3);

            var text = [
                $('<span/>', {id: 'name', text: name}),
                $('<span/>', {id: 'value', class: 'tip-value tip-detail',
                              text: values[0]}),
                $('<span/>', {id: 'norm', class: 'tip-value tip-detail',
                              text: values[1]})
            ];

            text = $('<div/>', {class: 'tip-line '}).append(text);

            return html(text);
        };

        var text = '';
        text += title_block(d.id);
        text += value_line('Purity', d.values.purity);
        text += value_line('Completeness', d.values.completeness);

        out = $('<div/>').append($(text));
        return out.html();
    };

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            return tip_text(d);
    });

    var legend_width = function() {
        d = legend_dimens;
        return d.width + d.tick_margin + d.offset;
    };

    /*****************************************************/

    /**
     * Calculate the min and max of field in the points
     */
    var calculateStats = function(points, name) {
        min = points[0][name];
        max = points[0][name];

        for (var i = 0; i < points.length; i++) {
            var value = points[name];
            if (value < min) min = value;
            else if (value > max) max = value;
        }

        return {
            'min': min,
            'max': max
        };
    };

    var genDataStats = function(points) {
        stats = {};
        for (var name in points[0]) {
            console.log(name)
            stats[name] = calculateStats(points, name);
        }

        console.log(stats)
        return stats;
    };

    var genColorScale = function(stats, color) {
        var colors = genColorMap(color);

        console.log(stats, color);
        var colorScale = d3.scaleLinear()
            .domain(linspace(stats.min, stats.max, colors.length))
            .range(colors);
        return colorScale;
    };

    /*****************************************************/

    var init_svg = function(chart, data) {
        // Compute svg dimensions
        var height = data.height * radius;
        var full_height = height + margin.top + margin.bottom;

        var width = (data.width * 20);
        var full_width = width + (2 * legend_width()) +
            margin.left + margin.right;

        self.dimens = {
            'width': width,
            'height': height
        };

        // Create svg handle
        var svg = chart.select('svg#graph-svg')
            .attr('width', full_width + 'px')
            .attr('height', full_height + 'px')
            .call(tip);

        return svg;
    };

    /*****************************************************/

    /**
     * Add colors to each plotted point
     */
    var add_gradients = function(svg, data, stats) {
        console.log(stats)
        axes = data.axes;
        var scales = {
            'a': genColorScale(stats.a, colormaps[axes.a]),
            'b': genColorScale(stats.b, colormaps[axes.b])
        };

        grads = svg.append('defs').selectAll('linearGradient')
            .data(data.points)
            .enter()
            .append('linearGradient')
            .attr('id', function(d) {return 'grad' + d.id;})
            .attr('x1', '100%')
            .attr('x2', '0%')
            .attr('y1', '0%')
            .attr('y2', '0%');
        grads.append('stop')
            .attr('offset', '50%')
            .style('stop-color', function(d) {
                return scales.b(d.b[0]);
            });
        grads.append('stop')
            .attr('offset', '50%')
            .style('stop-color', function(d) {
                return scales.a(d.a);
            });

        console.log(scales.a(.45));
    };

    /**
     * Add the points to the plot
     */
    var add_points = function(svg, data, names) {

        circles = svg.append('g')
            .attr('transform', 'translate(' +
                  margin.left + ', ' + margin.top + ')');

        var gentext = function(d) {
            var text = `id ${json.stringify(d.id)} `;
            var a = parseFloat(d.a).toFixed(8);
            var b = parseFloat(d.b).toFixed(8);
            text += `${axes.a}: ${a} ${axes.b}: ${b}`;
            return text;
        };

        circles.selectAll('circle')
            .data(data.points)
            .enter()
            .append('circle')
            .attr('r', '10' + 'px')
            .attr('cx', function(d) {return d.y * 20 + 10;})
            .attr('cy', function(d) {return d.x * 20 + 10;})
            .style('stroke-opacity', 0.6)
            .style('fill', function(d) {return 'url(#grad' + d.id;})
            .on('click', function(d) {
                var text = gentext(d);
                self.messages.message(text);
            })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);
    };

    var add_legends = function(svg, axes, stats) {
        add_legend(svg, axes, stats, 'a');
        add_legend(svg, axes, stats, 'b');
    };

    var add_legend = function(svg, axes, stats, key) {
        var offset = {
            'x': margin.left + self.dimens.width +
                 legend_dimens.offset + legend_count * legend_width(),
            'y': margin.top
        };

        console.log(offset, margin, self.dimens, legend_dimens)

        stats = stats[key];
        var axis = axes[key];

        var height = self.dimens.height;
        var width = legend_dimens.width;
        var colormap = genColorMap(colormaps[axis]);
        // console.log(10009, colormap, key)

        var legend = svg.append('g')
            .attr('transform', 'translate(' +
                offset.x + ', ' +
                offset.y + ')');

        var grad = legend.append('defs').append('linearGradient')
            .attr('id', 'legend-gradient')
            .attr('x1', '0%')
            .attr('y1', '100%')
            .attr('x2', '0%')
            .attr('y2', '0%')
            .attr('spreadMethod', 'pad');

        // Defining color stop spacing
        var pct = linspace(0, 100, colormap.length).map(function(d) {
            return Math.round(d) + '%';
        });

        // Adding gradient stops
        var colourPct = d3.zip(pct, colormap);
        colourPct.forEach(function(d) {
            grad.append('stop')
                .attr('offset', d[0])
                .attr('stop-color', d[1])
                .attr('stop-opacity', 1);
        });

        legend.append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', width)
            .attr('height', height)
            .style('fill', 'url(#legend-gradient)');

        var legendScale = d3.scaleLinear()
            .domain([stats.min, stats.max])
            .range([height, 0]);

        var legendAxis = d3.axisRight(legendScale)
            .ticks(5)
            .tickFormat(d3.format('.8f'));

        legend.append('g')
            .attr('class', 'legend axis')
            .attr('transform', 'translate(' + 25 + ', 0)')
            .call(legendAxis);

        legend_count += 1;
    };

    /*****************************************************/

};

var genColorMap = function(key) {
    colors = {
        'viridis': [
            '#440154', '#481567', '#482677', '#453781', '#404788',
            '#39568c', '#33638d', '#2d708e', '#287d7e', '#238a8d',
            '#1f968b', '#20a387', '#29af7f', '#3cbb75', '#55c667',
            '#73d055', '#95d840', '#b8de29', '#dce319', '#fde725'
        ],
        'bw': ['#000000', '#aaaaaa']
    };

    var viridis_r = colors['viridis'].slice();
    colors['viridis_r'] = viridis_r;
    viridis_r.reverse();

    return colors[key];
};

var genColorScale = function(stats, color) {
    var range = genColorMap(color);

    console.log(stats, range);
    var colorScale = d3.scaleLinear()
        .domain(linspace(stats.min, stats.max, range.length))
        .range(range);
    return colorScale;
};

var get_data = function(callback, experiment, type) {
    var url = new URI(window.location.href);
    var name = url.segment(1);
    var type = url.segment(2);

    $.get('/data', {
        'type': type,
        'plot': name
    }, function(data, status) {
        if (status == 'success' && data != null) {
            // console.log('data: ' + data.points.purity);
            console.log('status: ' + status);
            console.log(data);

            callback(data);
        }
    });
};

var defstep = function(start, end, n) {
    return (end - start) / n;
};

var linspace = function(start, end, n) {
    var out = [];
    var delta = (end - start) / (n - 1);

    var i = 0;
    while (i < (n - 1)) {
        out.push(start + (i * delta));
        i++;
    }

    out.push(end);
    // console.log(out)
    return out;
};

var run = function() {
    console.log(10);
    var data = [4, 8, 15, 16, 23, 42];
    var plotter = new aligned_plot_4d($('div#chart'));
    get_data(plotter.plot, 'random-500-p', 'sorted');

    plotter.messages.message('test');
};


$(document).ready(function() {
    run();
});
