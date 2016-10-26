/**
 * Created by Yi on 13/10/2016.
 */

import React, {Component} from 'react'
import {IndexLink, Link} from 'react-router'

import CSSModules from 'react-css-modules'
import style, {active} from './NavBar.scss'


class NavBar extends Component {
  render() {
    return (
      <div styleName="container">
        <div styleName="content">
          <IndexLink to='/' activeClassName={active} styleName='nav'>
            推荐
          </IndexLink>
          <Link to='/result' activeClassName={active} styleName='nav'>
            最新
          </Link>
          <Link to='/share' activeClassName={active} styleName='nav'>
            最热
          </Link>
          <Link to='/user' activeClassName={active} styleName='nav'>
            集锦
          </Link>
        </div>
      </div>
    )
  }
}

export default CSSModules(NavBar, style)