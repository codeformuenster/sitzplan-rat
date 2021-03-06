import React, { Component } from 'react'
import { graphql } from 'gatsby'

import Sitz from '../components/sitz'
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
      if (row !== null && column !== null) {
        if (!Array.isArray(grid[column])) {
          grid[column] = []
        }

        if (node.url) {
          const img_url = node.url.split('__kpenr=')[1]
          if (img_url) {
            node.img_url_id = img_url
          }
        }

        const key = `${column}-${row}`

        grid[column][row] = {
          ...node,
          ...{
            showPopup: false,
            key,
            // onClick: () => this.onSitzClick(key),
          },
        }

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

  onSitzClick = sitzKey => {
    const newGrid = [...this.state.grid]
    debugger
    rowLoop: for (let row = 0; row <= this.state.rows; row++) {
      for (let col = 0; col <= this.state.columns; col++) {
        if (
          this.state.grid[col] &&
          this.state.grid[col][row] &&
          this.state.grid[col][row].key === sitzKey
        ) {
          const newColumn = [...newGrid[col]]
          newColumn[row] = {
            ...this.state.grid[col][row],
            ...{
              showPopup: !this.state.grid[col][row].showPopup,
            },
          }
          newGrid[col] = newColumn
          break rowLoop
        }
      }
    }
    this.setState({ grid: newGrid })
  }

  _renderElements() {
    const elements = []
    for (let row = 0; row <= this.state.rows; row++) {
      for (let col = 0; col <= this.state.columns; col++) {
        if (this.state.grid[col] && this.state.grid[col][row]) {
          const sitz = this.state.grid[col][row]
          elements.push(<Sitz {...sitz} />)
        } else {
          elements.push(<div key={`${col}-${row}`} />)
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
