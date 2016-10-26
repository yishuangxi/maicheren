import React, {Component} from 'react'
import {IndexLink, Link} from 'react-router'

import CSSModules from 'react-css-modules'
import style from './Header.scss'

class Header extends Component {
  render() {
    return (
      <div styleName="container">
        <div styleName="header">
          <img src="http://static.funshion.com/open/fis/img/v12/common/head/img/logo_5387b9cdcd.gif"/>

          <input styleName="search_input"/>
          <button styleName="search_btn">搜索</button>
        </div>
      </div>
    )
  }
}

export default CSSModules(Header, style)
