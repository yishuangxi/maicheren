import React from 'react'
import CSSModules from 'react-css-modules'
import '../Styles/core.scss'
import style from './CoreLayout.scss'


export const CoreLayout = ({ children }) => (
  <div styleName='core-layout'>
   {children}
  </div>
)

CoreLayout.propTypes = {
  children : React.PropTypes.element.isRequired
}

export default CSSModules(CoreLayout, style)
