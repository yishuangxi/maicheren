// import {connect} from 'react-redux'
// import Container from './container'
// import reducer from './reducers'
// import {injectReducer} from '../../store/reducers'
// export default (store) => {
//   /*  Add the reducer to the store on key 'about'  */
//   injectReducer(store, {key: 'videoDetail', reducer})
//   return {
//     path: 'goods/:goodsId',
//     component: Container
//   }
// }


import {connect} from 'react-redux'
import {injectReducer} from '../../store/reducers'

export default (store) => ({
  path: 'v/:vid',
  /*  Async getComponent is only invoked when route matches   */
  getComponent (nextState, cb) {
    /*  Webpack - use 'require.ensure' to create a split point
     and embed an async module loader (jsonp) when bundling   */
    require.ensure([], (require) => {
      /*  Webpack - use require callback to define
       dependencies for bundling   */
      const VideoDetail = require('./container').default
      const reducer = require('./reducers').default

      /*  Add the reducer to the store on key 'about'  */
      injectReducer(store, {key: 'videoDetail', reducer})

      /*  Return getComponent   */
      cb(null, VideoDetail)

      /* Webpack named bundle   */
    }, 'videoDetail')
  }
})
