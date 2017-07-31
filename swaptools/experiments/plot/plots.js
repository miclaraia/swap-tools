var plotter;

var message_box = function(node) {
    var self = this;

    var init = function(node) {
        var _console = node.find('div#console');
        self.console = _console;
    };

    self.message = function(msg) {
        var element = $(document.createElement('div'));
        element.addClass('message').text(msg);
        self.console.append(element);
    };

    init(node);
};

var options_manager = function(node, callback) {
    var self = this;

    var init = function(node, callback) {
        self.callback = callback;

        self.graph_type = node.find('#graph-type');
        self.graph_type.change(self.onchange);
    };

    self.get_state = function() {
        var type = self.graph_type.find(':selected').attr('value');
        var state = {
            graph_type: type
        };

        return state;
    };

    self.onchange = function() {
        state = self.get_state();
        self.callback(state);
    };

    init(node, callback);
};

var tooltip = function(node) {

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

    var init = function(node) {
        self.container = node;
        self.messages = new message_box(node);
        self.options = new options_manager(node, self.redraw);
    };

    /*****************************************************/

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
        'offset': 10,
        'top_padding': 10,
    };

    var colormaps = {
        'purity': 'viridis',
        'completeness': 'viridis',
        'low threshold': 'viridis',
        'high threshold': 'viridis_r',
        'retired': 'viridis',
    };

    var dimens = {
        'height': null,
        'width': null
    };

    /*****************************************************/

    self.init = function(data) {
        self.legend_count = 0;
        self.data = data;
        self.redraw();
    };

    self.redraw = function() {
        console.log('redrawing')
        self.legend_count = 0;
        self.container.find('svg').remove();
        self.plot(self.data);
    };

    self.plot = function(data) {
        var type = self.options.get_state().graph_type;
        data = remap_coordinates(data, type);

        var svg = init_svg(self.container, data);
        var stats = genDataStats(data.points);

        console.log('data', data);
        console.log('stats', stats);
        console.log('type', type);

        add_gradients(svg, data, stats);
        add_points(svg, data);

        add_legends(svg, data.axes, stats);
    };

    /**
     * Generate the text for the tooltip on mouse hover
     */
    var tip_text = function(d, axes) {

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

        var title_block = function(point) {
            var elements = [];

            var text = '';
            console.log(axes, d)
            text += `${axes.x} ${value_span(point.x)} `;
            text += `${axes.y} ${value_span(point.y)}`;
            text = $(`<span>${text}</span>`)
                .attr('id', 'title')
                .addClass('tip-line tip-values');
            // console.log(html(text))

            return html(text);
        };

        var value_line = function(key) {
            var value = d[key];
            var name = axes[key];
            value = parseFloat(value).toFixed(3);

            var text = [
                $('<span/>', {id: 'name', text: name}),
                $('<span/>', {id: 'value', class: 'tip-value tip-detail',
                              text: value})
            ];

            text = $('<div/>', {class: 'tip-line '}).append(text);

            return html(text);
        };

        var text = '';
        text += title_block(d);
        text += value_line('a');
        text += value_line('b');

        out = $('<div/>').append($(text));
        return out.html();
    };

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            return tip_text(d, self.data.axes);
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
            var value = points[i][name];
            if (value < min) min = value;
            if (value > max) max = value;
        }

        return {
            'min': min,
            'max': max
        };
    };

    var genDataStats = function(points) {
        stats = {};
        for (var name in points[0]) {
            stats[name] = calculateStats(points, name);
        }

        return stats;
    };

    var genColorScale = function(stats, color) {
        var colors = genColorMap(color);

        var colorScale = d3.scaleLinear()
            .domain(linspace(stats.min, stats.max, colors.length))
            .range(colors);
        return colorScale;
    };

    /*****************************************************/

    var init_svg = function(container, data) {
        var chart = container.find('#chart').get(0);
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
        var svg = d3.select(chart).append('svg')
            .attr('id', 'graph-svg')
            .attr('class', 'graph-item')
            .attr('width', full_width + 'px')
            .attr('height', full_height + 'px')
            .call(tip);

        return svg;
    };

    var remap_coordinates = function(data, type) {
        var max_x = 0;
        var max_y = 0;

        var x = 0;
        var y = 0;
        var i = 0;
        var point;

        if (type == 'regular') {
            var last = data.points[0].y;

            for (point of data.points) {
                if (point.y != last) {
                    if (x > max_x) max_x = x;
                    x = 0;
                    y++;
                    last = point.y;
                }
                point._x = x;
                point._y = y;
                point.id = i;

                x++;
                i++;
            }
            max_y = y;
        } else if (type == 'sorted') {
            var order = data.ordering.sorted;
            var width = data.points.length;
            width = Math.floor(Math.sqrt(width));

            for (i = 0; i < data.ordering.sorted.length; i++) {
                if (x >= width) {
                    x = 0;
                    y++;
                }
                point = data.points[order[i]];
                point._x = x;
                point._y = y;
                point.id = i;

                x++;
            }
            max_x = width;
            max_y = y;
        }

        data.width = max_x;
        data.height = max_y;

        return data;
    };

    /*****************************************************/

    /**
     * Add colors to each plotted point
     */
    var add_gradients = function(svg, data, stats) {
        axes = data.axes;
        var scales = {
            'a': genColorScale(stats.a, colormaps[axes.a]),
            'b': genColorScale(stats.b, colormaps[axes.b])
        };

        // var scales = {
        //     'a': genColorScale(stats.a, 'viridis'),
        //     'b': genColorScale(stats.b, 'viridis')
        // };

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
                return scales.b(d.b);
            });
        grads.append('stop')
            .attr('offset', '50%')
            .style('stop-color', function(d) {
                return scales.a(d.a);
            });
    };

    /**
     * Add the points to the plot
     */
    var add_points = function(svg, data, names) {
        console.log(data)

        circles = svg.append('g')
            .attr('transform', 'translate(' +
                  margin.left + ', ' + margin.top + ')');

        var gentext = function(d) {
            var text = `id ${d.id} `;
            var a = parseFloat(d.a).toFixed(8);
            var b = parseFloat(d.b).toFixed(8);
            text += `${axes.x}: ${d.x}, `;
            text += `${axes.y}: ${d.y}, `;
            text += `${axes.a}: ${a} ${axes.b}: ${b}`;
            return text;
        };

        circles.selectAll('circle')
            .data(data.points)
            .enter()
            .append('circle')
            .attr('r', '10' + 'px')
            .attr('cx', function(d) {return d._x * 20 + 10;})
            .attr('cy', function(d) {return d._y * 20 + 10;})
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
                 legend_dimens.offset + self.legend_count * legend_width(),
            'y': margin.top
        };

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

        legend.append('text')
            .attr('x', 0)
            .attr('y', -8)
            .text(axes[key])
            .attr('font-family', 'sans-serif')
            .attr('font-size', '15px');

        self.legend_count += 1;
    };

    /*****************************************************/

    init(node);

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

            dataa = {
                'plot': 0,
                'name': 'test',
                'points': [{'x': 0, 'y': 0, 'a': 1, 'b': 1}],
                'axes': {
                    'x': 'x',
                    'y': 'y',
                    'a': 'purity',
                    'b': 'completeness'},
                'type': 'test'
            };

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
    var data = [4, 8, 15, 16, 23, 42];
    var plotter = new aligned_plot_4d($('div#chart-wrapper'));
    get_data(plotter.init, 'random-500-p', 'sorted');

    return plotter;
};


$(document).ready(function() {
    plotter = run();
});
