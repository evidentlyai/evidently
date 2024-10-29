import Plotly, { type Template } from 'plotly.js-cartesian-dist-min'

import createPlotlyComponent from 'react-plotly.js/factory'

const Plot = createPlotlyComponent(Plotly)

export default Plot

export const darkPlotlyLayoutTemplate: Template = {
  data: {
    barpolar: [
      {
        marker: {
          line: { color: 'rgb(17,17,17)', width: 0.5 },
          pattern: { fillmode: 'overlay', size: 10, solidity: 0.2 }
        },
        type: 'barpolar'
      }
    ],
    bar: [
      {
        // @ts-ignore
        error_x: { color: '#f2f5fa' },
        // @ts-ignore
        error_y: { color: '#f2f5fa' },
        marker: {
          line: { color: 'rgb(17,17,17)', width: 0.5 },
          pattern: { fillmode: 'overlay', size: 10, solidity: 0.2 }
        },
        type: 'bar'
      }
    ],
    carpet: [
      {
        // @ts-ignore
        aaxis: {
          endlinecolor: '#A2B1C6',
          gridcolor: '#506784',
          linecolor: '#506784',
          minorgridcolor: '#506784',
          startlinecolor: '#A2B1C6'
        },
        baxis: {
          endlinecolor: '#A2B1C6',
          gridcolor: '#506784',
          linecolor: '#506784',
          minorgridcolor: '#506784',
          startlinecolor: '#A2B1C6'
        },
        type: 'carpet'
      }
    ],
    choropleth: [{ colorbar: { outlinewidth: 0, ticks: '' }, type: 'choropleth' }],
    contourcarpet: [{ colorbar: { outlinewidth: 0, ticks: '' }, type: 'contourcarpet' }],
    contour: [
      {
        colorbar: { outlinewidth: 0, ticks: '' },
        colorscale: [
          [0.0, '#0d0887'],
          [0.1111111111111111, '#46039f'],
          [0.2222222222222222, '#7201a8'],
          [0.3333333333333333, '#9c179e'],
          [0.4444444444444444, '#bd3786'],
          [0.5555555555555556, '#d8576b'],
          [0.6666666666666666, '#ed7953'],
          [0.7777777777777778, '#fb9f3a'],
          [0.8888888888888888, '#fdca26'],
          [1.0, '#f0f921']
        ],
        type: 'contour'
      }
    ],
    heatmapgl: [
      {
        colorbar: { outlinewidth: 0, ticks: '' },
        colorscale: [
          [0.0, '#0d0887'],
          [0.1111111111111111, '#46039f'],
          [0.2222222222222222, '#7201a8'],
          [0.3333333333333333, '#9c179e'],
          [0.4444444444444444, '#bd3786'],
          [0.5555555555555556, '#d8576b'],
          [0.6666666666666666, '#ed7953'],
          [0.7777777777777778, '#fb9f3a'],
          [0.8888888888888888, '#fdca26'],
          [1.0, '#f0f921']
        ],
        type: 'heatmapgl'
      }
    ],
    heatmap: [
      {
        colorbar: { outlinewidth: 0, ticks: '' },
        colorscale: [
          [0.0, '#0d0887'],
          [0.1111111111111111, '#46039f'],
          [0.2222222222222222, '#7201a8'],
          [0.3333333333333333, '#9c179e'],
          [0.4444444444444444, '#bd3786'],
          [0.5555555555555556, '#d8576b'],
          [0.6666666666666666, '#ed7953'],
          [0.7777777777777778, '#fb9f3a'],
          [0.8888888888888888, '#fdca26'],
          [1.0, '#f0f921']
        ],
        type: 'heatmap'
      }
    ],
    histogram2dcontour: [
      {
        colorbar: { outlinewidth: 0, ticks: '' },
        colorscale: [
          [0.0, '#0d0887'],
          [0.1111111111111111, '#46039f'],
          [0.2222222222222222, '#7201a8'],
          [0.3333333333333333, '#9c179e'],
          [0.4444444444444444, '#bd3786'],
          [0.5555555555555556, '#d8576b'],
          [0.6666666666666666, '#ed7953'],
          [0.7777777777777778, '#fb9f3a'],
          [0.8888888888888888, '#fdca26'],
          [1.0, '#f0f921']
        ],
        type: 'histogram2dcontour'
      }
    ],
    histogram2d: [
      {
        colorbar: { outlinewidth: 0, ticks: '' },
        colorscale: [
          [0.0, '#0d0887'],
          [0.1111111111111111, '#46039f'],
          [0.2222222222222222, '#7201a8'],
          [0.3333333333333333, '#9c179e'],
          [0.4444444444444444, '#bd3786'],
          [0.5555555555555556, '#d8576b'],
          [0.6666666666666666, '#ed7953'],
          [0.7777777777777778, '#fb9f3a'],
          [0.8888888888888888, '#fdca26'],
          [1.0, '#f0f921']
        ],
        type: 'histogram2d'
      }
    ],
    histogram: [
      { marker: { pattern: { fillmode: 'overlay', size: 10, solidity: 0.2 } }, type: 'histogram' }
    ],
    mesh3d: [{ colorbar: { outlinewidth: 0, ticks: '' }, type: 'mesh3d' }],
    parcoords: [
      {
        line: {
          // @ts-ignore
          colorbar: { outlinewidth: 0, ticks: '' }
        },
        type: 'parcoords'
      }
    ],
    pie: [{ automargin: true, type: 'pie' }],
    scatter3d: [
      {
        line: {
          // @ts-ignore
          colorbar: { outlinewidth: 0, ticks: '' }
        },
        marker: { colorbar: { outlinewidth: 0, ticks: '' } },
        type: 'scatter3d'
      }
    ],
    scattercarpet: [
      { marker: { colorbar: { outlinewidth: 0, ticks: '' } }, type: 'scattercarpet' }
    ],
    scattergeo: [{ marker: { colorbar: { outlinewidth: 0, ticks: '' } }, type: 'scattergeo' }],
    scattergl: [{ marker: { line: { color: '#283442' } }, type: 'scattergl' }],
    scattermapbox: [
      { marker: { colorbar: { outlinewidth: 0, ticks: '' } }, type: 'scattermapbox' }
    ],
    scatterpolargl: [
      { marker: { colorbar: { outlinewidth: 0, ticks: '' } }, type: 'scatterpolargl' }
    ],
    scatterpolar: [{ marker: { colorbar: { outlinewidth: 0, ticks: '' } }, type: 'scatterpolar' }],
    scatter: [{ marker: { line: { color: '#283442' } }, type: 'scatter' }],
    scatterternary: [
      { marker: { colorbar: { outlinewidth: 0, ticks: '' } }, type: 'scatterternary' }
    ],
    surface: [
      {
        colorbar: { outlinewidth: 0, ticks: '' },
        colorscale: [
          [0.0, '#0d0887'],
          [0.1111111111111111, '#46039f'],
          [0.2222222222222222, '#7201a8'],
          [0.3333333333333333, '#9c179e'],
          [0.4444444444444444, '#bd3786'],
          [0.5555555555555556, '#d8576b'],
          [0.6666666666666666, '#ed7953'],
          [0.7777777777777778, '#fb9f3a'],
          [0.8888888888888888, '#fdca26'],
          [1.0, '#f0f921']
        ],
        type: 'surface'
      }
    ],
    table: [
      {
        // @ts-ignore
        cells: { fill: { color: '#506784' }, line: { color: 'rgb(17,17,17)' } },
        header: { fill: { color: '#2a3f5f' }, line: { color: 'rgb(17,17,17)' } },
        type: 'table'
      }
    ]
  },
  layout: {
    // @ts-ignore
    annotationdefaults: { arrowcolor: '#f2f5fa', arrowhead: 0, arrowwidth: 1 },
    autotypenumbers: 'strict',
    coloraxis: { colorbar: { outlinewidth: 0, ticks: '' } },
    colorscale: {
      diverging: [
        [0, '#8e0152'],
        [0.1, '#c51b7d'],
        [0.2, '#de77ae'],
        [0.3, '#f1b6da'],
        [0.4, '#fde0ef'],
        [0.5, '#f7f7f7'],
        [0.6, '#e6f5d0'],
        [0.7, '#b8e186'],
        [0.8, '#7fbc41'],
        [0.9, '#4d9221'],
        [1, '#276419']
      ],
      sequential: [
        [0.0, '#0d0887'],
        [0.1111111111111111, '#46039f'],
        [0.2222222222222222, '#7201a8'],
        [0.3333333333333333, '#9c179e'],
        [0.4444444444444444, '#bd3786'],
        [0.5555555555555556, '#d8576b'],
        [0.6666666666666666, '#ed7953'],
        [0.7777777777777778, '#fb9f3a'],
        [0.8888888888888888, '#fdca26'],
        [1.0, '#f0f921']
      ],
      sequentialminus: [
        [0.0, '#0d0887'],
        [0.1111111111111111, '#46039f'],
        [0.2222222222222222, '#7201a8'],
        [0.3333333333333333, '#9c179e'],
        [0.4444444444444444, '#bd3786'],
        [0.5555555555555556, '#d8576b'],
        [0.6666666666666666, '#ed7953'],
        [0.7777777777777778, '#fb9f3a'],
        [0.8888888888888888, '#fdca26'],
        [1.0, '#f0f921']
      ]
    },
    colorway: [
      '#636efa',
      '#EF553B',
      '#00cc96',
      '#ab63fa',
      '#FFA15A',
      '#19d3f3',
      '#FF6692',
      '#B6E880',
      '#FF97FF',
      '#FECB52'
    ],
    font: { color: '#f2f5fa' },
    geo: {
      bgcolor: 'rgb(17,17,17)',
      lakecolor: 'rgb(17,17,17)',
      landcolor: 'rgb(17,17,17)',
      showlakes: true,
      showland: true,
      subunitcolor: '#506784'
    },
    hoverlabel: { align: 'left' },
    hovermode: 'closest',
    mapbox: { style: 'dark' },
    paper_bgcolor: 'rgb(17,17,17)',
    plot_bgcolor: 'rgb(17,17,17)',
    polar: {
      angularaxis: { gridcolor: '#506784', linecolor: '#506784', ticks: '' },
      bgcolor: 'rgb(17,17,17)',
      radialaxis: { gridcolor: '#506784', linecolor: '#506784', ticks: '' }
    },
    scene: {
      xaxis: {
        backgroundcolor: 'rgb(17,17,17)',
        gridcolor: '#506784',
        gridwidth: 2,
        linecolor: '#506784',
        showbackground: true,
        ticks: '',
        zerolinecolor: '#C8D4E3'
      },
      yaxis: {
        backgroundcolor: 'rgb(17,17,17)',
        gridcolor: '#506784',
        gridwidth: 2,
        linecolor: '#506784',
        showbackground: true,
        ticks: '',
        zerolinecolor: '#C8D4E3'
      },
      zaxis: {
        backgroundcolor: 'rgb(17,17,17)',
        gridcolor: '#506784',
        gridwidth: 2,
        linecolor: '#506784',
        showbackground: true,
        ticks: '',
        zerolinecolor: '#C8D4E3'
      }
    },
    shapedefaults: { line: { color: '#f2f5fa' } },
    sliderdefaults: {
      bgcolor: '#C8D4E3',
      bordercolor: 'rgb(17,17,17)',
      borderwidth: 1,
      tickwidth: 0
    },
    ternary: {
      aaxis: { gridcolor: '#506784', linecolor: '#506784', ticks: '' },
      baxis: { gridcolor: '#506784', linecolor: '#506784', ticks: '' },
      bgcolor: 'rgb(17,17,17)',
      caxis: { gridcolor: '#506784', linecolor: '#506784', ticks: '' }
    },
    title: { x: 0.05 },
    updatemenudefaults: { bgcolor: '#506784', borderwidth: 0, showactive: false },
    xaxis: {
      automargin: true,
      gridcolor: '#283442',
      linecolor: '#506784',
      ticks: '',
      title: { standoff: 15 },
      zerolinecolor: '#283442',
      zerolinewidth: 2
    },
    yaxis: {
      automargin: true,
      gridcolor: '#283442',
      linecolor: '#506784',
      ticks: '',
      title: { standoff: 15 },
      zerolinecolor: '#283442',
      zerolinewidth: 2
    }
  }
}
