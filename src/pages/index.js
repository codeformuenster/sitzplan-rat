import React, { Component } from 'react'

import Layout from '../components/layout'
import SEO from '../components/seo'

export default class IndexPage extends Component {
  constructor(props) {
    super(props)
    this.state = {
      rows: 0,
      columns: 0,
    }
    this._handleColumns = this._handleColumns.bind(this)
    this._handleRows = this._handleRows.bind(this)
  }

  _handleRows(e) {
    this.setState({ rows: e.target.value })
  }

  _handleColumns(e) {
    this.setState({ columns: e.target.value })
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
        >
          <div>
            <h5>Rows</h5>
            <input type="number" onChange={this._handleRows} />
          </div>
          <div>
            <h5>Columns</h5>
            <input type="number" onChange={this._handleColumns} />
          </div>
        </div>
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
