/**
 * Created by Yi on 19/10/2016.
 */

export const fetchError = (err, dispatch, action) => {
  console.warn('fetchError: ', err)
  dispatch && actionCreator ? dispatch(action) : null
}

export const ifFetchFailure = (json, dispatch, actionCreator) => {
  if (json.code == 0) {
    return json
  } else {
    console.warn('fetchFailed: ', json)
    dispatch && actionCreator ? dispatch(action) : null
    return new Promise((resolve, reject)=> {
    })
  }
}