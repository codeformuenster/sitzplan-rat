import React, { Component } from 'react'
import { graphql } from 'gatsby'

import Layout from '../components/layout'
import SEO from '../components/seo'
import './sitzplan.css'
import * as cn from 'classnames'

export default class IndexPage extends Component {
  constructor(props) {
    super(props)

    const grid = []
    let maxRow = 0,
      maxCol = 0
    props.data.allSitzeYaml.edges.forEach(({ node }) => {
      const { row, column } = node
      if (typeof row !== 'undefined') {
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
    }
  }

  _renderElements() {
    const elements = []
    for (let row = 0; row <= this.state.rows; row++) {
      for (let col = 0; col <= this.state.columns; col++) {
        if (this.state.grid[col] && this.state.grid[col][row]) {
          const sitz = this.state.grid[col][row]
          elements.push(
            <div
              key={`${row}-${col}`}
              className={cn({ sitz: sitz }, sitz.partei)}
            >
              {sitz.url ? (
                <a href={sitz.url} target="_blank" rel="noopener noreferrer">
                  {sitz.label}
                </a>
              ) : (
                sitz.label
              )}
            </div>
          )
        } else {
          elements.push(<div key={`${row}-${col}`} />)
        }
      }
    }
    return elements
  }

  render() {
    return (
      <Layout>
        <SEO title="Sitzplan Rat" keywords={['muenster', 'sitzplan', 'rat']} />
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
