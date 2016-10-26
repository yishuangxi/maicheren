import {combineReducers} from 'redux'
import locationReducer from './location'
import homeReducer from '../routes/Home/reducers'
import UserReducer from '../routes/User/reducers'

export const makeRootReducer = (asyncReducers) => {
  return combineReducers({
    location: locationReducer,
    home: homeReducer,
    user:UserReducer,
    ...asyncReducers
  })
}

export const injectReducer = (store, {key, reducer}) => {
  store.asyncReducers[key] = reducer
  store.replaceReducer(makeRootReducer(store.asyncReducers))
}

export default makeRootReducer
