import React from 'react'
import * as cn from 'classnames'
import Tippy from '@tippy.js/react'

import Img from 'react-image'

import 'tippy.js/dist/tippy.css'

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

const Sitz = ({ url, partei, label }) => {
  let sitz_id
  if (typeof url === 'string') {
    sitz_id = url.split('__kpenr=')[1]
  }
  return (
    <Tippy
      arrow={true}
      content={<SitzPopup partei={partei} label={label} sitz_id={sitz_id} />}
    >
      <div className={cn('sitz', partei)}>
        <a
          className="sitz-link"
          href={url}
          target="_blank"
          rel="noopener noreferrer"
        >
          {label}
        </a>
      </div>
    </Tippy>
  )
}

export default Sitz
