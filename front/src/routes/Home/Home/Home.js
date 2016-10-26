/**
 * Created by Yi on 13/10/2016.
 */
import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import Header from '../../Common/Components/Header'
import NavBar from '../../Common/Components/NavBar'

import CSSModules from 'react-css-modules'
import style from './Home.scss'

class Home extends Component {

  componentWillMount() {
  }


  render() {
    return (
      <div styleName="container">
        <Header/>
        <NavBar/>
      </div>
    )
  }
}


export default CSSModules(Home, style)
