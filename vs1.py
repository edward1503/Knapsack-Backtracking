import plotly.graph_objs as go

colorall = {
    'bar': '#CDCDCD',
    'line': '#000000',
    'max': '#59DC3D',
    'xaxes' : '#000000'
}
def draw(data):
    max_val, best_set, best_weight, all_sets, all_values, all_weights = data

    stt1 = list()
    stt = list(range(1, len(all_values) + 1))

    fig = go.Figure()
    colors = list()

    # Find the maximum point on the charts
    for i in range(0, len(all_values)):
        if all_weights[i] == best_weight and all_values[i] == max_val:
            colors.append(colorall['max'])
        else:
            colors.append(colorall['bar'])
    #create xaxis based on valid set (all_sets)
    stt = [' '.join([str(y) for y in x]) for x in all_sets]

    #Bar chart show weight
    fig.add_trace(go.Bar(x=stt, y=all_weights, marker_color=colors,
                            name='Khối lượng', yaxis='y1'))
    #Line chart show value
    fig.add_trace(go.Scatter(x=stt, y=all_values, marker_color=colorall["line"], 
                                name='Giá trị', yaxis='y2'))
        
    # Update layout and show the figure
    fig.update_layout(
        title_text="Biểu đồ thay đổi khối lượng và giá trị",
        #template = 'plotly_dark',
        plot_bgcolor = '#E3ECF7',
        paper_bgcolor = '#FFFFFF',
        # xaxis_title="Bước",
        xaxis = dict(
                        title = 'Options',
                        gridwidth = 1,
                        color = colorall['xaxes'],
                        showticklabels = False
                    ),
        yaxis = dict(
        linecolor = colorall['bar'],
        linewidth = 2,
        title = 'Cumulative \n Sum of Weight',
        titlefont = dict(
            family = 'Arial, sans-serif',
            size = 10,
            color = colorall['bar'],
            
        ),
        showticklabels = True,
        tickangle = 45,
        tickfont = dict(
        family = 'Arial, sans-serif',
        size = 10,
        color = colorall['bar']
        ),
        tickmode = 'array',
        tick0 = 0.0,
        dtick = 5),

        # create second Y-axis
        yaxis2=dict(
            title='Cumulative \n Sum of Value',
            titlefont = dict(
            family = 'Arial, sans-serif',
            size = 10,
            color = colorall['line']),
            overlaying="y",
            side="right", color = colorall['line']),
        
        legend = dict(
            xanchor="left", yanchor="top", y = -0.1, x = 0.0
        )
    )
    return fig