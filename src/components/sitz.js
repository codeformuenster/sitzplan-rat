import React from 'react'
import * as cn from 'classnames'
import Tippy from '@tippy.js/react'

import Img from 'react-image'

import 'tippy.js/dist/tippy.css'

const PARTYCOLORS = {
  gruene: 'green',
  spd: 'red',
  linke: 'red',
  cdu: 'black',
  piraten: 'orange',
  afd: 'blue',
  fdp: 'yellow'
}

const SitzPopup = React.memo(({ label, sitz_id, partei }) => (
  <>
    <h4>{label}</h4>
    <p>{partei}</p>
    <div>
      <Img
        src={`https://www.stadt-muenster.de/sessionnet/sessionnetbi/im/pe${sitz_id}.jpg`}
      />
    </div>
  </>
))

const Sitz = ({ col, row, url, partei, label, highlight }) => {
  let sitz_id
  if (typeof url === 'string') {
    sitz_id = url.split('__kpenr=')[1]
  }
  return (
    <Tippy
      arrow={true}
      content={<SitzPopup partei={partei} label={label} sitz_id={sitz_id} />}
    >
      <div className={cn('sitz', partei)} style={{
        gridColumnStart: col + 1,
        gridColumnEnd: col + 2,
        gridRowStart: row + 1,
        gridRowEnd: row + 2,
        backgroundColor: highlight ? PARTYCOLORS[partei] : 'grey'
      }}>
        <a
          className="sitz-link"
          href={url}
          target="_blank"
          rel="noopener noreferrer"
        >
          {label}
        </a>
        <a
          className="sitz-link-first"
          href={url}
          target="_blank"
          rel="noopener noreferrer"
        >
          {label.charAt(0)}
        </a>
      </div>
    </Tippy>
  )
}

export default Sitz
