/**
 * Created by Yi on 13/10/2016.
 */
import React, {Component, PropTypes} from 'react'
import {connect} from 'react-redux'

import Home from './Home'
import {fetchGoodsList,fetchBannerList,fetchMsgList} from './actions'

/*  Object of action creators (can also be function that returns object).
 Keys will be passed as props to presentational components. Here we are
 implementing our wrapper around increment; the component doesn't care   */

const mapDispatchToProps = {
  fetchGoodsList,
  fetchBannerList,
  fetchMsgList
}

const mapStateToProps = (state) => ({
  goodsList: state.home.goodsList || [],
  bannerList: state.home.bannerList || [],
  msgList: state.home.msgList || []
})

/*  Note: mapStateToProps is where you should use `reselect` to create selectors, ie:

 import { createSelector } from 'reselect'
 const counter = (state) => state.counter
 const tripleCount = createSelector(counter, (count) => count * 3)
 const mapStateToProps = (state) => ({
 counter: tripleCount(state)
 })

 Selectors can compute derived data, allowing Redux to store the minimal possible state.
 Selectors are efficient. A selector is not recomputed unless one of its arguments change.
 Selectors are composable. They can be used as input to other selectors.
 https://github.com/reactjs/reselect    */

export default connect(mapStateToProps, mapDispatchToProps)(Home)
