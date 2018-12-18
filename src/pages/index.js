import React, { Component } from 'react'
import { graphql } from 'gatsby'

import Layout from '../components/layout'
import SEO from '../components/seo'

export default class IndexPage extends Component {
  constructor(props) {
    super(props)

    let maxRow = 0,
      maxCol = 0
    props.data.allSitzeYaml.edges.forEach(({ node: { row, column } }) => {
      if (row && row > maxRow) {
        maxRow = row
      }
      if (column && column > maxCol) {
        maxCol = column
      }
    })

    this.state = {
      rows: maxRow,
      columns: maxCol,
    }
    console.log(this.state)
  }

  _renderElements() {
    let num = Array.from(Array(this.state.rows * this.state.columns).keys())
    let elements = num.map((e, i) => (
      <div
        key={i}
        style={{
          backgroundColor: 'black',
          height: '30px',
          margin: '10px',
        }}
      />
    ))
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
          style={{
            display: 'grid',
            gridTemplateColumns: `repeat(${this.state.columns}, 1fr)`,
            gridTemplateRows: `repeat(${this.state.rows}, 1fr)`,
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
