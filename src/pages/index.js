import React, { Component } from 'react'
import { graphql } from 'gatsby'

import Layout from '../components/layout'
import SEO from '../components/seo'
import './sitzplan.css'

export default class IndexPage extends Component {
  constructor(props) {
    super(props)

    const grid = []
    let maxRow = 0,
      maxCol = 0
    props.data.allSitzeYaml.edges.forEach(({ node }) => {
      const { row, column } = node
      if (typeof row !== 'undefined') {
        console.log(node)
        if (!Array.isArray(grid[column])) {
          grid[column] = []
        }

        grid[column][row] = node

        if (row && row > maxRow) {
          maxRow = row
        }
        if (column && column > maxCol) {
          maxCol = column
        }
      }
    })

    this.state = {
      rows: maxRow,
      columns: maxCol,
      grid,
      seats: props.data.allSitzeYaml.edges,
    }
  }

  _renderElements() {
    // for (const row of
    let elements = []
    console.log(this.state.grid)
    for (let row = 0; row <= this.state.rows; row++) {
      for (let col = 0; col <= this.state.columns; col++) {
        let label = null
        if (this.state.grid[col] && this.state.grid[col][row]) {
          label = this.state.grid[col][row].label
        }
        elements.push(
          <div key={`${row}-${col}`} className={label ? 'sitz' : ''}>
            {label}
          </div>
        )
      }
    }
    return elements
  }

  render() {
    return (
      <Layout>
        <SEO title="Home" keywords={['gatsby', 'application', 'react']} />
        <div
          style={{
            display: 'flex',
          }}
        />
        <div
          className="sitze"
          style={{
            gridTemplateColumns: `repeat(${this.state.columns + 1}, 1fr)`,
            gridTemplateRows: `repeat(${this.state.rows + 1}, 1fr)`,
          }}
        >
          {this._renderElements()}
        </div>
      </Layout>
    )
  }
}

export const query = graphql`
  {
    allSitzeYaml {
      edges {
        node {
          label
          name
          url
          partei
          row
          column
        }
      }
    }
  }
`
